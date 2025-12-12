from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager
import speech_recognition as sr
from pydub import AudioSegment
from deepmultilingualpunctuation import PunctuationModel
import nltk
import shutil
import os
import uuid
import logging
import httpx # <--- REQUIRED: This allows Port 8000 to talk to Port 8001
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ml_models = {}

# --- CONFIG: Point to your Grading API (Port 8001) ---
EVALUATION_API_URL = "http://127.0.0.1:8001/evaluate_interview"

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading NLP Models...")
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
        nltk.download('punkt_tab')
    
    ml_models["punctuation"] = PunctuationModel()
    yield
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

# --- HELPER FUNCTIONS ---
def convert_to_wav(input_path: str, output_path: str):
    if input_path.endswith(".mp3"):
        AudioSegment.from_mp3(input_path).export(output_path, format="wav")
    elif input_path.endswith(".webm"):
        AudioSegment.from_file(input_path, format="webm").export(output_path, format="wav")
    else:
        AudioSegment.from_file(input_path).export(output_path, format="wav")

def transcribe_audio(wav_path: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except:
            return ""

def is_question(sentence: str) -> bool:
    starters = ["what", "how", "why", "can you", "tell me", "explain", "describe", "so the", "ok good", "next question"]
    s = sentence.lower().strip()
    return any(s.startswith(q) for q in starters) or s.endswith('?')

def process_qa(raw_text: str):
    model = ml_models["punctuation"]
    text = model.restore_punctuation(raw_text)
    sentences = nltk.sent_tokenize(text)
    
    qa_pairs = []
    current_q = None
    current_a = []

    for sent in sentences:
        if is_question(sent):
            if current_q:
                qa_pairs.append({"question": current_q, "answer": " ".join(current_a) if current_a else "..."})
                current_a = []
            current_q = sent
        else:
            if current_q: current_a.append(sent)

    if current_q:
        qa_pairs.append({"question": current_q, "answer": " ".join(current_a) if current_a else "..."})

    return text, qa_pairs

# --- MAIN ENDPOINT ---
@app.post("/process-interview")
async def process_interview(file: UploadFile = File(...)):
    unique_id = str(uuid.uuid4())
    temp_in = f"temp_{unique_id}.{file.filename.split('.')[-1]}"
    temp_wav = f"temp_{unique_id}.wav"

    try:
        # 1. Save & Convert
        with open(temp_in, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        convert_to_wav(temp_in, temp_wav)

        # 2. Transcribe
        logger.info("Transcribing...")
        raw_text = transcribe_audio(temp_wav)
        if not raw_text:
            return {"status": "failed", "transcript": "", "qa_pairs": [], "evaluation_report": None}

        # 3. NLP Extraction
        full_transcript, qa_pairs = process_qa(raw_text)

        # 4. CALL GRADING API (Port 8001)
        evaluation_report = None
        
        if qa_pairs:
            logger.info(f"Sending {len(qa_pairs)} pairs to Port 8001 for grading...")
            
            # Payload matching what Port 8001 expects
            payload = {
                "audioFile": file.filename,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "success",
                "full_transcript": full_transcript,
                "qa_pairs": qa_pairs
            }
            
            try:
                # We use a long timeout (120s) because Gemini takes time to grade
                async with httpx.AsyncClient(timeout=120.0) as client:
                    resp = await client.post(EVALUATION_API_URL, json=payload)
                    
                    if resp.status_code == 200:
                        evaluation_report = resp.json()
                        logger.info(f"Grading Report: {evaluation_report}")
                        logger.info("✅ Grading Complete! Report received.")
                    else:
                        logger.error(f"Grading API Error: {resp.status_code} - {resp.text}")
            except Exception as e:
                logger.error(f"❌ Could not connect to Grading API (Is api_server_v2.py running?): {e}")

        # 5. Return everything to Node.js (server.js)
        return {
            "status": "success",
            "full_transcript": full_transcript,
            "qa_pairs": qa_pairs,
            "evaluation_report": evaluation_report # <--- This is the key piece!
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_in): os.remove(temp_in)
        if os.path.exists(temp_wav): os.remove(temp_wav)
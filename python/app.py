import os
import json
import time
import uuid
import shutil
import logging
from datetime import datetime

import chromadb
import nltk
import speech_recognition as sr
from pydub import AudioSegment
from deepmultilingualpunctuation import PunctuationModel

import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager

import re

# ---------------- CONFIG ----------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Gemini
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("❌ GEMINI_API_KEY missing")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# ChromaDB
client = chromadb.PersistentClient(path="./interview_db")
collection = client.get_collection("cloud_engineer_questions")

ml_models = {}

# ---------------- LIFECYCLE ----------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading models...")

    try:
        nltk.data.find('tokenizers/punkt')
    except:
        nltk.download('punkt')

    ml_models["punctuation"] = PunctuationModel()
    yield
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

# ---------------- AUDIO + NLP ----------------

def convert_to_wav(input_path, output_path):
    if input_path.endswith(".webm"):
        AudioSegment.from_file(input_path, format="webm").export(output_path, format="wav")
    else:
        AudioSegment.from_file(input_path).export(output_path, format="wav")

def transcribe_audio(wav_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            return ""

def is_question(sentence):
    starters = ["what", "how", "why", "where", "when", "who", "which", "whose", "can you", "could you", "would you", "do you", "did you", "are you", "tell me"]
    s = sentence.lower().strip()
    return any(s.startswith(q) for q in starters) or s.endswith('?')

def process_qa(raw_text):
    model = ml_models["punctuation"]
    text = model.restore_punctuation(raw_text)
    sentences = nltk.sent_tokenize(text)

    qa_pairs = []
    current_q = None
    current_a = []

    for sent in sentences:
        if is_question(sent):
            if current_q:
                qa_pairs.append({
                    "question": current_q,
                    "answer": " ".join(current_a)
                })
                current_a = []
            current_q = sent
        else:
            if current_q:
                current_a.append(sent)

    if current_q:
        qa_pairs.append({
            "question": current_q,
            "answer": " ".join(current_a)
        })

    return text, qa_pairs

# ---------------- EVALUATION ----------------

SIMILARITY_THRESHOLD = 0.5  # tweak this later

import re

SIMILARITY_THRESHOLD = 0.5  # tweak this later


def clean_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return {"score": 0, "feedback": "Parsing error"}


def evaluate_single_pair(pair):
    results = collection.query(
        query_texts=[pair["question"]],
        n_results=1,
        include=["documents", "metadatas", "distances"]
    )

    if not results["documents"][0]:
        return fallback_evaluation(pair)

    matched_q = results["documents"][0][0]
    metadata = results["metadatas"][0][0]
    distance = results["distances"][0][0]

    print(f"🔍 Distance: {distance}")

    # 🔥 DECISION POINT
    if distance > SIMILARITY_THRESHOLD:
        print("⚠️ Low similarity → using fallback LLM evaluation")
        return fallback_evaluation(pair)

    # ✅ GOOD MATCH → DB-guided evaluation
    ideal = metadata.get("ideal_answer", "")
    keywords = metadata.get("keywords", "")
    difficulty = metadata.get("difficulty", "Unknown")
    topic = metadata.get("topic", "General")

    prompt = f"""
You are a strict technical interviewer.

DB Question:
{matched_q}

Candidate Question:
{pair["question"]}

Ideal Answer:
{ideal}

Keywords:
{keywords}

Candidate Answer:
{pair["answer"]}

Score based on correctness.

Return JSON:
{{
  "score": int,
  "feedback": "brief feedback"
}}
"""

    try:
        response = model.generate_content(prompt)
        data = clean_json(response.text)
    except Exception as e:
        data = {"score": 0, "feedback": str(e)}

    return {
        "difficulty": difficulty,
        "topic": topic,
        "matched_q": matched_q,
        "score": data.get("score", 0),
        "feedback": data.get("feedback", "")
    }

def fallback_evaluation(pair):
    """
    Used when DB match is irrelevant.
    LLM evaluates answer independently.
    """

    prompt = f"""
You are a technical interviewer.

Question:
{pair["question"]}

Candidate Answer:
{pair["answer"]}

Evaluate the answer independently.

Scoring:
- 90–100: Excellent
- 70–89: Good
- 50–69: Partial
- 0–49: Poor

Return JSON:
{{
  "score": int,
  "feedback": "clear technical feedback"
}}
"""

    try:
        response = model.generate_content(prompt)
        data = clean_json(response.text)
    except Exception as e:
        data = {"score": 0, "feedback": str(e)}

    return {
        "difficulty": "Dynamic",
        "topic": "General",
        "matched_q": "LLM-generated evaluation",
        "score": data.get("score", 0),
        "feedback": data.get("feedback", "")
    }

# ---------------- MAIN API ----------------

@app.post("/process-interview")
async def process_interview(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    temp_in = f"temp_{uid}"
    temp_wav = f"{temp_in}.wav"

    try:
        # Save file
        with open(temp_in, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        convert_to_wav(temp_in, temp_wav)

        # Transcribe
        raw_text = transcribe_audio(temp_wav)
        if not raw_text:
            return {"status": "failed"}

        # NLP
        full_text, qa_pairs = process_qa(raw_text)

        # Evaluate
        results = []
        total = 0

        for pair in qa_pairs:
            r = evaluate_single_pair(pair)
            results.append({
                "question": pair["question"],
                "candidate_answer": pair["answer"],
                **r
            })
            total += r["score"]
            time.sleep(1)

        avg = total / len(results) if results else 0

        return {
            "status": "success",
            "full_transcript": full_text,
            "qa_pairs": qa_pairs,
            "evaluation_report": {
                "total_score": avg,
                "results": results
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_in): os.remove(temp_in)
        if os.path.exists(temp_wav): os.remove(temp_wav)
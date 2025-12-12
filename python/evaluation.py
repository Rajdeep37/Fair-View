import chromadb
import os
import json
import time
import uvicorn
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

# --- 1. CONFIGURATION ---
load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = genai.GenerativeModel('gemini-2.5-flash')
print(f"🤖 API Initialized using Model: {MODEL_NAME}")
model = genai.GenerativeModel('gemini-2.5-flash')

# Connect to ChromaDB
DB_PATH = "./interview_db"
COLLECTION_NAME = "cloud_engineer_questions"
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(COLLECTION_NAME)

app = FastAPI(title="Interview Evaluation API", version="2.0")

# --- 2. INPUT DATA MODELS (Matching your JSON) ---

class QAPair(BaseModel):
    question: str
    answer: str

class InterviewInput(BaseModel):
    audioFile: Optional[str] = None
    timestamp: Optional[str] = None
    status: Optional[str] = None
    full_transcript: Optional[str] = None
    qa_pairs: List[QAPair]

# --- 3. OUTPUT DATA MODELS ---

class GradedQuestion(BaseModel):
    question: str
    candidate_answer: str
    # RAG Data
    difficulty: str     # <--- REQUESTED FIELD
    topic: str
    matched_db_question: str
    # LLM Eval
    score: int
    feedback: str

class EvaluationReport(BaseModel):
    audio_file: Optional[str]
    total_score: float
    results: List[GradedQuestion]

# --- 4. CORE LOGIC ---

def evaluate_single_pair(pair: QAPair):
    """
    Process a single Q&A pair:
    1. Retrieve 'Ideal Answer' & 'Difficulty' from DB.
    2. Grade using Gemini.
    """
    # A. Search Vector DB
    results = collection.query(
        query_texts=[pair.question],
        n_results=1
    )

    # Handle case where DB is empty or no match (Edge Case)
    if not results['documents'][0]:
        return {
            "difficulty": "Unknown",
            "topic": "Unknown",
            "matched_q": "No match found",
            "score": 0,
            "feedback": "Question not found in database."
        }

    # B. Extract Metadata
    # Note: Chromadb returns lists of lists. We access index [0][0]
    matched_q = results['documents'][0][0]
    metadata = results['metadatas'][0][0]
    
    difficulty = metadata.get('difficulty', 'Unknown')
    topic = metadata.get('topic', 'General')
    ideal_ans = metadata.get('ideal_answer', '')
    keywords = metadata.get('keywords', '')

    # C. LLM Evaluation Prompt
    prompt = f"""
    You are a Technical Interview Grader.
    
    ### GROUND TRUTH
    DB Question: "{matched_q}"
    Ideal Answer: "{ideal_ans}"
    Required Keywords: "{keywords}"
    Difficulty: {difficulty}
    
    ### CANDIDATE INPUT
    Question Asked: "{pair.question}"
    Candidate Answer: "{pair.answer}"

    ### TASK
    1. Check if the 'Question Asked' is semantically similar to 'DB Question'. 
       (If the user asks "Capital of India" but DB returns "AWS Regions", score it 0 as 'Irrelevant').
    2. Grade the Candidate Answer (0-100) based on the Ideal Answer.
    3. Return JSON: {{"score": int, "feedback": "string"}}
    """

    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        eval_data = json.loads(clean_text)
        
        return {
            "difficulty": difficulty,
            "topic": topic,
            "matched_q": matched_q,
            "score": eval_data.get("score", 0),
            "feedback": eval_data.get("feedback", "Error parsing feedback")
        }
    except Exception as e:
        return {
            "difficulty": difficulty,
            "topic": topic,
            "matched_q": matched_q,
            "score": 0,
            "feedback": f"LLM Error: {str(e)}"
        }

# --- 5. API ENDPOINT ---

@app.post("/evaluate_interview", response_model=EvaluationReport)
async def process_interview(data: InterviewInput):
    graded_results = []
    total_score_sum = 0
    
    print(f"📥 Processing interview: {data.audioFile}")

    for pair in data.qa_pairs:
        # Evaluate Logic
        result = evaluate_single_pair(pair)
        
        # Build Response Object
        graded_q = GradedQuestion(
            question=pair.question,
            candidate_answer=pair.answer,
            difficulty=result['difficulty'], # <--- Returning from DB
            topic=result['topic'],
            matched_db_question=result['matched_q'],
            score=result['score'],
            feedback=result['feedback']
        )
        
        graded_results.append(graded_q)
        total_score_sum += result['score']
        
        # Polite delay to avoid rate limits
        time.sleep(1)

    # Calculate Average
    avg_score = total_score_sum / len(data.qa_pairs) if data.qa_pairs else 0

    return EvaluationReport(
        audio_file=data.audioFile,
        total_score=round(avg_score, 2),
        results=graded_results
    )

# --- 6. START SERVER ---
if __name__ == "__main__":
    print("🚀 Server running on http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)
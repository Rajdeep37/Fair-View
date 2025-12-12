# integrated_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Import your Q&A extractor class
from mcp import QuestionAnswerExtractor

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="Q&A Extraction & Evaluation API")

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

# Initialize extractor
extractor = QuestionAnswerExtractor()

# Request & response models
class TextRequest(BaseModel):
    text: str

class EvaluatedQAPair(BaseModel):
    question: str
    answer: str
    score: float

class EvaluationResponse(BaseModel):
    evaluated_pairs: List[EvaluatedQAPair]

# Gemini evaluation function
def evaluate_correctness(question: str, answer: str) -> float:
    try:
        prompt = f'"Question: {question}" Answer: "{answer}". Provide a score from 0 (non-relevant) to 100 (perfectly relevant). Just return the number.'
        response = model.generate_content(prompt)
        score = float(response.text.strip())
        return score
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating response: {str(e)}")

# API endpoint
@app.post("/extract_and_evaluate", response_model=EvaluationResponse)
async def extract_and_evaluate(request: TextRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text field is empty")
    
    # Step 1: Extract Q&A pairs
    qa_pairs = extractor.extract_qa_pairs(request.text)
    if not qa_pairs:
        raise HTTPException(status_code=404, detail="No Q&A pairs found")
    
    # Step 2: Evaluate each Q&A pair
    evaluated_pairs = []
    for pair in qa_pairs:
        score = evaluate_correctness(pair["question"], pair["answer"])
        evaluated_pairs.append(
            EvaluatedQAPair(
                question=pair["question"],
                answer=pair["answer"],
                score=score
            )
        )
    
    return EvaluationResponse(evaluated_pairs=evaluated_pairs)

@app.get("/")
def root():
    return {"message": "Q&A Extraction & Evaluation API is running"}

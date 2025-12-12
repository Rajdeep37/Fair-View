from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Question Answer Evaluation API")

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

class QuestionAnswer(BaseModel):
    question: str
    answer: str

class EvaluationRequest(BaseModel):
    qa_pairs: List[QuestionAnswer]

class EvaluationResponse(BaseModel):
    scores: List[float]

def evaluate_correctness(question: str, answer: str) -> float:
    try:
        prompt = f'"Question: {question}" Answer: "{answer}".Provide a score from 0 (for non-relevancy) to 100 (for best relevancy). Just return a number,dont return any text.'
        response = model.generate_content(prompt)
        score = float(response.text.strip())
        return score
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating response: {str(e)}")

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_answers(request: EvaluationRequest):
    try:
        scores = []
        for qa_pair in request.qa_pairs:
            score = evaluate_correctness(qa_pair.question, qa_pair.answer)
            scores.append(score)
        return EvaluationResponse(scores=scores)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to Question Answer Evaluation API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 

#uvicorn app:app --reload
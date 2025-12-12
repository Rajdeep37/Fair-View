import chromadb
import os
import json
import time  # <--- CRITICAL IMPORT
import google.generativeai as genai
from dotenv import load_dotenv

# --- 1. CONFIGURATION & SETUP ---
load_dotenv() 

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# SWITCHED TO 1.5 FLASH (More stable free tier limits than 2.0)
model = genai.GenerativeModel('gemini-2.5-flash')

# Connect to ChromaDB
DB_PATH = "./interview_db"
COLLECTION_NAME = "cloud_engineer_questions"
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(COLLECTION_NAME)

print(f"✅ System Online. Connected to Vector DB ({collection.count()} records) & Gemini API.\n")

# --- 2. TEST SCENARIOS ---
test_scenarios = [
    {
        "id": 1,
        "question": "What is the difference between a Pod and a Deployment in Kubernetes?",
        "candidate_answer": "A Pod is just a container. A Deployment is like a manager that controls the pods and handles updates.",
        "quality_expected": "Good"
    },
    {
        "id": 2,
        "question": "What are the Shared Responsibility Model in AWS.",
        "candidate_answer": "Amazon takes care of the hardware and the data center security. The user is responsible for their own data, encryption, and patching the OS.",
        "quality_expected": "Good"
    },
    {
        "id": 3,
        "question": "What is a Terraform State file and why is it important?",
        "candidate_answer": "I think it's a file that stores your credentials? I usually delete it to reset terraform.",
        "quality_expected": "TERRIBLE (Destructive)"
    },
    {
        "id": 4,
        "question": "How do you troubleshoot high I/O wait time on Linux?",
        "candidate_answer": "I would check the CPU usage. If it's high, I'll add more cores.",
        "quality_expected": "Bad (Confused CPU with Disk I/O)"
    },
    {
        "id": 5,
        "question": "What is a 'Zombie Process'?",
        "candidate_answer": "It's a process that has finished executing but the parent hasn't read its exit code yet. It takes up a PID but no CPU.",
        "quality_expected": "Excellent"
    },
    {
        "id": 6,
        "question": "Explain the 4 Golden Signals of monitoring.",
        "candidate_answer": "Latency, Traffic, Errors, and... Saturation? Yeah, Saturation.",
        "quality_expected": "Good"
    },
    {
        "id": 7,
        "question": "What is BGP (Border Gateway Protocol)?",
        "candidate_answer": "It's a protocol for internal routing inside a VPC.",
        "quality_expected": "Wrong"
    },
    {
        "id": 8,
        "question": "When should you use AWS Fargate instead of standard EC2?",
        "candidate_answer": "When you don't want to manage servers. It's serverless for containers.",
        "quality_expected": "Good"
    },
    {
        "id": 9,
        "question": "What is ACID compliance in databases?",
        "candidate_answer": "Atomicity, Consistency, Isolation, and Durability. It ensures transactions are reliable.",
        "quality_expected": "Good"
    },
    {
        "id": 10,
        "question": "How do you reduce Data Transfer costs in AWS?",
        "candidate_answer": "Use a NAT Gateway for everything.",
        "quality_expected": "Bad"
    }
]

# --- 3. ROBUST EVALUATION FUNCTION (With Retry Logic) ---
def evaluate_with_retry(question_text, candidate_answer, max_retries=3):
    """
    Tries to evaluate. If rate limited, waits and retries automatically.
    """
    
    # RAG Retrieval
    results = collection.query(query_texts=[question_text], n_results=1)
    if not results['documents'][0]:
        return {"error": "Question not found in DB"}

    metadata = results['metadatas'][0][0]
    
    # Prompt Construction
    prompt = f"""
    You are an expert Technical Interviewer.
    
    ### GROUND TRUTH
    Question: "{results['documents'][0][0]}"
    Correct Answer: "{metadata['ideal_answer']}"
    Keywords: {metadata['keywords']}
    
    ### CANDIDATE ANSWER
    "{candidate_answer}"

    ### TASK
    Rate the answer 0-100 based on the Ground Truth.
    Return JSON: {{"score": int, "reasoning": "string"}}
    """

    # Retry Loop
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                wait_time = (attempt + 1) * 10  # Wait 10s, then 20s, then 30s
                print(f"      ⚠️  Rate Limit hit. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                return {"error": f"LLM Error: {error_msg}"}
    
    return {"error": "Max retries exceeded."}

# --- 4. RUN TEST SUITE ---
def run_test_suite():
    print("🚀 STARTING EVALUATION BATCH...\n")
    
    for i, scenario in enumerate(test_scenarios, 1):
        q = scenario['question']
        a = scenario['candidate_answer']
        expected = scenario['quality_expected']
        
        print(f"🔹 Scenario {i}/10")
        print(f"   Q: {q}")
        print(f"   A: \"{a}\"")
        
        result = evaluate_with_retry(q, a)
        
        if "error" in result:
            print(f"   ❌ FAILED: {result['error']}")
        else:
            score = result.get('score', 0)
            reason = result.get('reasoning', 'No reasoning provided')
            icon = "✅" if score > 60 else "⚠️" if score > 30 else "❌"
            
            print(f"   {icon} SCORE: {score}/100")
            print(f"   📝 FEEDBACK: {reason}")
            print(f"   👀 EXPECTED: {expected}")
        
        print("-" * 60)
        time.sleep(10) # Standard polite delay

if __name__ == "__main__":
    run_test_suite()
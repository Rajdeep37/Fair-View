import chromadb
from data.questions import serverless_finops_batch

client = chromadb.PersistentClient(path="./interview_db")

# Create OR get collection
collection = client.get_or_create_collection("cloud_engineer_questions")

documents = [item["q"] for item in serverless_finops_batch]
ids = [f"q_{i}" for i in range(len(serverless_finops_batch))]

metadatas = [{
    "role": "Cloud Engineer",
    "topic": item["topic"],
    "difficulty": item["diff"],
    "ideal_answer": item["ans"],
    "keywords": item["keys"]
} for item in serverless_finops_batch]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"✅ DB Ready. Count: {collection.count()}")
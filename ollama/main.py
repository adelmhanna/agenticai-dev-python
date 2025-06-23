from fastapi import FastAPI
from sentence_transformers import SentenceTransformer

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy"}

model = SentenceTransformer('all-MiniLM-L6-v2')

@app.post("/embed")
async def embed(text: dict):
    return {"embedding": model.encode(text["text"]).tolist()}
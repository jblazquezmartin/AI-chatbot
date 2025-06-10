from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import qdrant_client
from qdrant_client.http.models import Filter, SearchRequest
import requests

app = FastAPI()

model = SentenceTransformer("BAAI/bge-base-en-v1.5")
client = qdrant_client.QdrantClient(host="qdrant", port=6333)

COLLECTION_NAME = "docs"

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask(query: Query):
    question_embedding = model.encode(query.question).tolist()
    hits = client.search(
        collection_name=COLLECTION_NAME,
        search_request=SearchRequest(
            vector=question_embedding,
            limit=5,
            with_payload=True
        )
    )

     # Filtrar resultados por umbral de similitud (score)
    filtered_hits = [hit for hit in hits if hit.score and hit.score > 0.75]
    
    if not filtered_hits:
        return {"answer": "No tengo suficiente información para responder con contexto."}
        
    context = "\n".join([hit.payload["text"] for hit in hits if "text" in hit.payload])
    prompt = f"Contexto:\n{context}\n\nPregunta: {query.question}\nRespuesta:"

    response = requests.post("http://ollama:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })
    return {"answer": response.json().get("response", "").strip()}

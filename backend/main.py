# backend/main.py

import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import qdrant_client
from qdrant_client.http.models import SearchRequest
import requests

# --- INICIALIZACIÓN (sin cambios) ---
app = FastAPI()

try:
    print("Cargando modelo de embeddings BAAI/bge-base-en-v1.5...")
    model = SentenceTransformer("BAAI/bge-base-en-v1.5")
    print("Modelo cargado con éxito.")
except Exception as e:
    print(f"Error fatal al cargar el modelo de embeddings: {e}")
    model = None

try:
    client = qdrant_client.QdrantClient(host="qdrant", port=6333)
    print("Conectado a Qdrant.")
except Exception as e:
    print(f"Error fatal al conectar con Qdrant: {e}")
    client = None

COLLECTION_NAME = "my_collection"

class Query(BaseModel):
    question: str

# --- ENDPOINT /ask CORREGIDO ---
@app.post("/ask")
async def ask(query: Query):
    if not model or not client:
        raise HTTPException(status_code=500, detail="El servidor no está listo (modelo o cliente de DB no inicializado).")

    try:
        # 1. Crear el vector de la pregunta
        question_embedding = model.encode(query.question).tolist()

        # 2. Buscar en Qdrant
        hits = client.search(
            collection_name=COLLECTION_NAME,
            search_request=SearchRequest(
                vector=question_embedding,
                limit=5,
                with_payload=True
            )
        )
        print(f"Búsqueda en Qdrant encontró {len(hits)} resultados.")

        # 3. Filtrar resultados por umbral de similitud (TU LÓGICA REINSERTADA)
        # Solo consideramos resultados con un score mayor a 0.75
        filtered_hits = [hit for hit in hits if hit.score and hit.score > 0.75]
        print(f"Resultados después de filtrar por score > 0.75: {len(filtered_hits)}.")
        
        # 4. Comprobar si hay contexto relevante
        if not filtered_hits:
            return {"answer": "No tengo suficiente información en mi base de conocimiento para responder a esa pregunta."}
        
        # 5. Construir el contexto USANDO LOS RESULTADOS FILTRADOS
        context = "\n".join([hit.payload["text"] for hit in filtered_hits if "text" in hit.payload])
        print(f"Contexto construido para Ollama:\n---\n{context}\n---")

        # 6. Construir el prompt
        prompt = f"Usando únicamente el siguiente contexto, responde a la pregunta.\n\nContexto:\n{context}\n\nPregunta: {query.question}\nRespuesta:"

        # 7. Llamar a Ollama
        print("Enviando petición a Ollama...")
        response = requests.post(
            "http://ollama:11434/api/generate", 
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()

        # 8. Procesar y devolver la respuesta
        ollama_response = response.json().get("response", "").strip()
        print(f"Respuesta recibida de Ollama: {ollama_response}")
        
        return {"answer": ollama_response}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error de comunicación con Ollama: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno en la API: {e}")

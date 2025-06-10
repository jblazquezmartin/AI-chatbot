# backend/ingest/process.py - Versión corregida de tu código original

import os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
import uuid
from pathlib import Path

# --- CONFIGURACIÓN ---
QDRANT_HOST = "qdrant" # <-- ¡EL CAMBIO CLAVE! Usamos el nombre del servicio Docker.
QDRANT_PORT = 6333
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
COLLECTION_NAME = "my_collection" # Cambié el nombre para que coincida con el backend
DOCS_FOLDER = "/app/docs"

# --- LÓGICA DE INGESTA ---
if __name__ == "__main__":
    # 1. Conectar al cliente de Qdrant
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    print(f"Conectado a Qdrant en {QDRANT_HOST}:{QDRANT_PORT}")

    # 2. Cargar el modelo de embeddings
    print(f"Cargando el modelo de embeddings: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    embedding_size = model.get_sentence_embedding_dimension()
    print(f"Modelo cargado. Tamaño del vector: {embedding_size}")

    # 3. Crear la colección (método moderno y seguro)
    print(f"Asegurando que la colección '{COLLECTION_NAME}' exista...")
    
    collections_response = client.get_collections()
    existing_collections = [collection.name for collection in collections_response.collections]

    if COLLECTION_NAME in existing_collections:
        print(f"La colección '{COLLECTION_NAME}' ya existe. Borrándola para recrearla.")
        client.delete_collection(collection_name=COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=embedding_size, distance=models.Distance.COSINE),
    )
    print("Colección creada/recreada con éxito.")

    # 4. Leer archivos y dividirlos en trozos
    texts = []
    source_files = list(Path(DOCS_FOLDER).glob("*.txt"))
    print(f"Encontrados {len(source_files)} archivos .txt en la carpeta '{DOCS_FOLDER}'")

    for file_path in source_files:
        with open(file_path, "r") as f:
            content = f.read()
            # Dividir el contenido en trozos de 500 caracteres
            chunks = [content[i:i+500] for i in range(0, len(content), 500)]
            texts.extend(chunks)
    
    print(f"Contenido dividido en {len(texts)} trozos.")

    # 5. Crear los vectores (embeddings)
    print("Creando vectores para los trozos de texto...")
    vectors = model.encode(texts, show_progress_bar=True).tolist()

    # 6. Preparar los puntos para Qdrant
    points = [
        models.PointStruct(id=str(uuid.uuid4()), vector=vec, payload={"text": txt})
        for vec, txt in zip(vectors, texts)
    ]

    # 7. Subir los puntos a Qdrant
    print(f"Subiendo {len(points)} puntos a Qdrant...")
    client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)

    print("\n¡Ingesta de datos completada con éxito!")

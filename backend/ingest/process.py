import os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
import uuid

from pathlib import Path

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer("BAAI/bge-base-en-v1.5")
COLLECTION_NAME = "docs"

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)

texts = []
for file_path in Path("docs").glob("*.txt"):
    with open(file_path, "r") as f:
        content = f.read()
        chunks = [content[i:i+500] for i in range(0, len(content), 500)]
        texts.extend(chunks)

vectors = model.encode(texts).tolist()

points = [
    PointStruct(id=str(uuid.uuid4()), vector=vec, payload={"text": txt})
    for vec, txt in zip(vectors, texts)
]

client.upsert(collection_name=COLLECTION_NAME, points=points)

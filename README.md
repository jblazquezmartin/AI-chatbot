# RAG POC - Mistral 7B + Qdrant + Streamlit + Ollama

## Cómo usar
1. Instala Docker y Docker Compose
2. Ejecuta:
   ```bash
   docker compose -f docker/docker-compose.yml up --build
   ```

3. Abre:
   - `http://localhost:7860` → UI
   - `http://localhost:8000/ask` → API POST

## Ingesta
Coloca archivos `.txt` en la carpeta `docs/` y ejecuta:

```bash
docker exec -it <api-container> python ingest/process.py
```

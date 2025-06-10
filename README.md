# RAG POC - Mistral 7B + Qdrant + Streamlit + Ollama

## Cómo usar
1. Instala Docker y Docker Compose
2. Ejecuta:
   ```bash
   docker compose -f docker/docker-compose.yml up --build
   ```
3. Descarga el modelo de LLM:
```bash
docker-compose -f docker/docker-compose.yml exec ollama ollama pull mistral
```
Nota: Solo necesitas hacer esto la primera vez. El modelo se guardará en un volumen persistente y estará disponible en futuros inicios.

5. Abre:
   - `http://localhost:7860` → UI
   - `http://localhost:8000/ask` → API POST

## Ingesta
Coloca archivos `.txt` en la carpeta `docs/` y ejecuta:

```bash
docker exec -it <api-container> python ingest/process.py
```

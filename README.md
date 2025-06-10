# RAG POC - Mistral 7B + Qdrant + Streamlit + Ollama

## Cómo usar
1. Instala Docker y Docker Compose
2. Ejecuta:
   ```bash
   docker compose -f docker/docker-compose.yml up --build
   ```
3. El contenedor de Ollama se inicia vacío. Para que la aplicación funcione, necesitas descargar un modelo. El proyecto está configurado para usar **`mistral`** por defecto.
   Descarga el modelo de LLM:
```bash
docker-compose -f docker/docker-compose.yml exec ollama ollama pull mistral
```
Nota: Solo necesitas hacer esto la primera vez. El modelo se guardará en un volumen persistente y estará disponible en futuros inicios.

o Puedes usar el script de ayuda proporcionado para descargar el modelo:

   3.1.  **Dar permisos de ejecución al script** (solo la primera vez):
    ```bash
    chmod +x llm/download_model.sh
    ```

   3.2.  **Ejecutar el script para descargar `mistral`**:
    ```bash
    ./llm/download_model.sh
    ```

Este comando descargará el modelo `mistral` y lo guardará en un volumen persistente, por lo que solo necesitas hacerlo una vez.

¿Quieres usar un modelo diferente (ej: Llama 3)

Puedes descargar cualquier otro modelo de Ollama ejecutando el script con el nombre del modelo. Por ejemplo:

```bash
./llm/download_model.sh llama3
 ```

¡Importante! Si eliges un modelo que no sea mistral, debes actualizar el código fuente para que la API lo utilice. Edita el archivo backend/main.py y modifica la variable donde se define el nombre del modelo.

4. Abre:
   - `http://localhost:7860` → UI
   - `http://localhost:8000/ask` → API POST

## Ingesta
Coloca archivos `.txt` en la carpeta `docs/` y ejecuta:

```bash
docker-compose -f docker/docker-compose.yml exec api python ingest/process.py
```

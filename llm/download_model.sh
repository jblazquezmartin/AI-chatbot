#!/bin/bash

# Script de ayuda para descargar un modelo de lenguaje en el servicio de Ollama en ejecución.
# Uso:
#   ./llm/download_model.sh                   (Descarga 'mistral' por defecto)
#   ./llm/download_model.sh llama3            (Descarga el modelo 'llama3')

# -----------------------------------------------------------------------------

# Se usa el primer argumento como nombre del modelo. Si no se proporciona, se usa 'mistral' por defecto.
MODEL_NAME=${1:-mistral}

echo "INFO: Intentando descargar el modelo '$MODEL_NAME' en el servicio 'ollama'..."

# Ejecuta el comando 'pull' dentro del contenedor de Ollama
docker-compose -f docker/docker-compose.yml exec ollama ollama pull "$MODEL_NAME"

echo "INFO: Proceso finalizado."

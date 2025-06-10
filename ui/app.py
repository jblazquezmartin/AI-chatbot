# ui/app.py

import streamlit as st
import requests

st.title("🤖 RAG POC Chat")

query = st.text_input("Haz tu pregunta:")

if query:
    try:
        # Usamos 'api' como el nombre del host, que es el nombre del servicio en docker-compose
        response = requests.post("http://api:8000/ask", json={"question": query})
        
        if response.status_code == 200:
            st.write("Respuesta de la API:")
            st.write(response.json())
        else:
            st.error(f"Error de la API: {response.status_code}")
            st.error(response.text)

    except requests.exceptions.ConnectionError as e:
        st.error("Error de Conexión: No se pudo conectar con el servicio de la API.")
        st.error("Asegúrate de que el contenedor 'api' esté corriendo correctamente.")
        st.error(f"Detalles: {e}")

import streamlit as st
import requests

st.title("RAG POC - Mistral")

query = st.text_input("Pregunta:")
if query:
    response = requests.post("http://api:8000/ask", json={"question": query})
    st.markdown("### Respuesta:")
    st.write(response.json()["answer"])

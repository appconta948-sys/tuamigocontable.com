import streamlit as st
import streamlit.components.v1 as components

# Leer tu archivo HTML
with open("templates/index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# Renderizar el HTML en la app de Streamlit
components.html(html_code, height=600, scrolling=True)

# Aquí puedes añadir la lógica de tu Agente de IA con botones de Streamlit
pregunta = st.text_input("Habla con el Agente:")
if pregunta:
    st.write("El agente está pensando...")
    # Aquí conectarías con la API de OpenAI/Gemini

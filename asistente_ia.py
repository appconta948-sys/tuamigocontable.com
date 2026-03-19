import os
import streamlit as st

class ContaIA:
    def __init__(self):
        self.nombre = "Conta IA"
        self.empresa = "tuamigocontable.com"

    def analizar_archivos_locales(self):
        # Esta función escanea tus carpetas de GitHub
        carpetas = ['fiscal', 'contabilidad-general', 'libro-de-registro-de-contabilidad']
        resumen = {}
        for c in carpetas:
            try:
                resumen[c] = os.listdir(c)
            except:
                resumen[c] = []
        return resumen

    def responder(self, consulta, datos_dashboard):
        # Aquí es donde la IA "piensa"
        consulta = consulta.lower()
        
        if "balance" in consulta:
            return f"Tu balance actual es de {datos_dashboard['balance']}. Revisando tus libros, el flujo es estable."
        
        if "archivos" in consulta or "libros" in consulta:
            archivos = self.analizar_archivos_locales()
            return f"He detectado archivos en tus libros: {archivos.get('libro-de-registro-de-contabilidad', 'Ninguno')}."
            
        return "Soy tu asistente contable. Puedo ayudarte a interpretar tus balances o buscar documentos en tus carpetas fiscales."

import streamlit as st
from asistente_ia import ContaIA  # <--- Importamos el archivo aparte

# Iniciamos el cerebro una sola vez para no gastar memoria
if "cerebro_ia" not in st.session_state:
    st.session_state.cerebro_ia = ContaIA()

# ... (Aquí va todo tu código de los cuadros de colores y reportes) ...

# SECCIÓN DEL ASISTENTE APARTE
st.markdown("---")
with st.container():
    st.subheader("💬 Habla con el Asistente Contable")
    
    if "historial" not in st.session_state:
        st.session_state.historial = []

    # Chat nativo de Streamlit
    for m in st.session_state.historial:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    if prompt := st.chat_input("¿Qué quieres consultar hoy?"):
        st.session_state.historial.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # LE PEDIMOS LA RESPUESTA AL ARCHIVO APARTE
        datos_actuales = {"balance": "$470.00"} # Esto lo puedes traer de tus variables
        respuesta = st.session_state.cerebro_ia.responder(prompt, datos_actuales)
        
        with st.chat_message("assistant"):
            st.write(respuesta)
        st.session_state.historial.append({"role": "assistant", "content": respuesta})


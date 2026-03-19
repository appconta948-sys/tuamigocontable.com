import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN (Debe ser lo primero siempre)
st.set_page_config(page_title="tuamigocontable.com", layout="wide")

# 2. ESTILO VISUAL (Basado en tus fotos)
st.markdown("""
    <style>
    .header-blue { background-color: #46637f; color: white; padding: 20px; border-radius: 10px; text-align: center; }
    .card-balance { background: white; padding: 15px; border-radius: 10px; border-top: 5px solid #46637f; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 3. ASISTENTE EN EL LATERAL (Aseguramos que aparezca)
with st.sidebar:
    st.title("🤖 CONTA IA")
    st.write("Estoy listo para analizar tus carpetas.")
    
    if "chat" not in st.session_state:
        st.session_state.chat = []

    # Mostrar mensajes previos
    for m in st.session_state.chat:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    # Entrada de texto
    if prompt := st.chat_input("¿Qué quieres saber?"):
        st.session_state.chat.append({"role": "user", "content": prompt})
        # Respuesta rápida para evitar que se quede "Connecting"
        res = f"Analizando tus datos... (Recuerda configurar tu API Key en Secrets)"
        st.session_state.chat.append({"role": "assistant", "content": res})
        st.rerun()

# 4. CUERPO PRINCIPAL (Dashboard)
st.markdown('<div class="header-blue"><h1>MIRA TU BALANCE AQUÍ</h1></div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Métricas rápidas
c1, c2, c3 = st.columns(3)
with c1: st.markdown('<div class="card-balance">💵<br>Ingresos<br><b>$5,450.00</b></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="card-balance">💳<br>Egresos<br><b>$4,980.00</b></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="card-balance">⚖️<br>Balance<br><b>$470.00</b></div>', unsafe_allow_html=True)

st.markdown("---")

# 5. SECCIÓN DE REPORTES (Lo que se veía en tu foto)
st.subheader("📊 Reportes y Exportación")
col_a, col_b = st.columns(2)
with col_a:
    st.button("📈 Generar Balance General")
with col_b:
    st.button("📥 Descargar Reporte Mes (Excel)")

# 6. LECTURA DE CARPETAS (La parte inteligente)
st.subheader("📋 Últimos Registros")
st.write("Archivos detectados en tus carpetas de GitHub:")

# Intentamos listar archivos de una de tus carpetas
try:
    archivos = os.listdir("libro-de-registro-de-contabilidad")
    st.info(f"Archivos encontrados: {', '.join(archivos)}")
except:
    st.warning("Carpeta de registros no detectada todavía.")

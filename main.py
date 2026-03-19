import streamlit as st
import pandas as pd
from datetime import datetime

# ============================================
# 1. CONFIGURACIÓN Y ESTILO (Look Profesional)
# ============================================
st.set_page_config(page_title="tuamigocontable.com", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# 2. NAVEGACIÓN (Control de Páginas)
# ============================================
if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

def ir_a(nombre_pagina):
    st.session_state.pagina = nombre_pagina

# ============================================
# 3. MEMORIA DEL CHAT (Asistente)
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Soy tu asistente de tuamigocontable.com. ¿En qué te ayudo hoy?"}]

# ============================================
# 4. BARRA LATERAL (Menú)
# ============================================
with st.sidebar:
    st.title("📂 Menú Principal")
    if st.button("🏠 Inicio", use_container_width=True): ir_a("Inicio")
    if st.button("📄 Facturación", use_container_width=True): ir_a("Factura")
    if st.button("📦 Inventario", use_container_width=True): ir_a("Inventario")
    if st.button("🤖 Asistente IA", use_container_width=True): ir_a("IA")
    st.markdown("---")
    st.info("tuamigocontable.com v1.0")

# ============================================
# 5. LÓGICA DE PÁGINAS
# ============================================

if st.session_state.pagina == "Inicio":
    st.title("📊 Resumen Financiero")
    
    # Métricas principales
    c1, c2, c3 = st.columns(3)
    c1.metric("Ingresos", "$1.500.000", "+12%")
    c2.metric("Egresos", "$500.000", "-5%")
    c3.metric("Saldo Neto", "$1.000.000", delta_color="normal")

    st.subheader("📋 Últimos Movimientos")
    # Tabla de ejemplo
    df_ejemplo = pd.DataFrame({
        "Fecha": ["2024-03-20", "2024-03-19"],
        "Detalle": ["Venta de Servicios", "Pago de Arriendo"],
        "Monto": ["$500.000", "$200.000"],
        "Tipo": ["Ingreso", "Egreso"]
    })
    st.table(df_ejemplo)

elif st.session_state.pagina == "Factura":
    st.title("📄 Módulo de Facturación")
    st.write("Aquí podrás generar tus facturas en PDF próximamente.")
    if st.button("← Volver"): ir_a("Inicio")

elif st.session_state.pagina == "Inventario":
    st.title("📦 Control de Inventario")
    st.write("Gestión de existencias y costos.")
    if st.button("← Volver"): ir_a("Inicio")

elif st.session_state.pagina == "IA":
    st.title("🤖 Asistente Contable Inteligente")
    st.caption("Consulta tus saldos y dudas legales aquí.")

    # Mostrar historial
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    if prompt := st.chat_input("Escribe tu duda contable..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Respuesta simulada (Aquí conectarás tu API Key después)
        respuesta = "Estoy analizando tus datos... (Conecta tu API Key en Secrets para respuestas reales)."
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        st.chat_message("assistant").write(respuesta)

# ============================================
# 6. FOOTER
# ============================================
st.markdown("---")
st.caption("© 2024 tuamigocontable.com | Contabilidad Inteligente")

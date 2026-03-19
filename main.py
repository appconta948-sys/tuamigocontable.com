import streamlit as st
import pandas as pd
from datetime import datetime

# ============================================
# 1. CONFIGURACIÓN Y PALETA DE COLORES (TU IMAGEN)
# ============================================
st.set_page_config(page_title="Tu Amigo Contable", layout="wide", initial_sidebar_state="collapsed")

# Colores extraídos de tu imagen de referencia
COLOR_PRIMARIO = "#345470"  # Azul petróleo del banner
COLOR_FONDO = "#e1e8ee"    # Gris azulado de fondo
COLOR_TEXTO = "#1a1a1a"
COLOR_VERDE = "#92c83e"    # Verde de los títulos en el banner

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Roboto', sans-serif;
        background-color: {COLOR_FONDO};
    }}

    /* Estilo del Header Principal */
    .main-header {{
        background-color: {COLOR_PRIMARIO};
        padding: 40px 20px;
        color: {COLOR_VERDE};
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
    }}
    .main-header h1 {{ font-size: 35px; font-weight: 700; color: {COLOR_VERDE} !important; }}

    /* Tarjetas del Dashboard */
    .card {{
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 15px;
    }}
    .card h2 {{ color: {COLOR_PRIMARIO}; font-size: 18px; }}
    .card p {{ font-size: 24px; font-weight: 700; color: {COLOR_TEXTO}; }}

    /* Botones estilo SHEIN / Global */
    .stButton>button {{
        background-color: {COLOR_PRIMARIO} !important;
        color: white !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-weight: 700 !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# 2. NAVEGACIÓN Y LOGIN
# ============================================
if 'login' not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown(f"<h1 style='text-align:center; color:{COLOR_PRIMARIO}'>Tu Amigo Contable</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.info("Ingresa con tu cuenta de Google para gestionar tu contabilidad.")
        if st.button("🔴 Entrar con Google"):
            st.session_state.login = True
            st.rerun()
    st.stop()

# Menú de Navegación
menu = st.sidebar.selectbox("Ir a:", [
    "🏠 Dashboard", 
    "📈 Reportes y Facturas", 
    "🏢 Nuestra Empresa", 
    "💳 Suscripción (Global)", 
    "📞 Contáctanos", 
    "⚖️ Legal y Seguridad"
])

# ============================================
# 3. PÁGINAS DEL SISTEMA
# ============================================

# --- DASHBOARD ---
if menu == "🏠 Dashboard":
    st.markdown(f"<div class='main-header'><h1>MIRA TU BALANCE AQUÍ</h1><p style='color:white'>Tu resumen financiero inteligente</p></div>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='card'><h2>Balance Actual</h2><p>$470.00</p></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='card'><h2>Consumo Mes</h2><p>$4,980.00</p></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='card'><h2>Reportes</h2><p>12 Listos</p></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='card'><h2>IA Tips</h2><p>5 Pendientes</p></div>", unsafe_allow_html=True)
    
    st.subheader("📝 Registro Diario")
    st.table(pd.DataFrame({
        "Fecha": ["2026-03-18", "2026-03-19"],
        "Detalle": ["Pago Nómina", "Venta Software"],
        "Monto": ["$500.00", "$1.200.00"]
    }))

# --- REPORTES Y FACTURAS ---
elif menu == "📈 Reportes y Facturas":
    st.header("📄 Gestión de Documentos")
    st.write("Genera facturas profesionales y descarga plantillas desde tu carpeta 'tabla'.")
    st.button("📥 Descargar Balance (Excel)")
    st.button("📂 Exportar Plantilla Profesional")

# --- NUESTRA EMPRESA ---
elif menu == "🏢 Nuestra Empresa":
    st.header("About Tu Amigo Contable")
    st.write("**Misión:** Facilitar la contabilidad de cada hogar y empresa.")
    st.write("**Visión:** Ser el líder global en asistencia contable por IA.")
    st.write("**Objetivos:** Seguridad, Rapidez y Transparencia.")

# --- SUSCRIPCIÓN ---
elif menu == "💳 Suscripción (Global)":
    st.header("💳 Planes y Pagos")
    st.success("7 días de prueba GRATIS habilitados")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='card'><h3>Mensual</h3><p>$10 USD</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Mensual")
    with col2:
        st.markdown("<div class='card'><h3>Trimestral</h3><p>$25 USD</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Trimestral")
    with col3:
        st.markdown("<div class='card'><h3>Anual</h3><p>$99 USD</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Anual")
    st.caption("Los pagos se convierten automáticamente a tu moneda local al procesar.")

# --- CONTACTO ---
elif menu == "📞 Contáctanos":
    st.header("📍 Ubicación y Contacto")
    st.write("Cedritos, Bogotá, Colombia")
    st.map(pd.DataFrame({'lat': [4.7228], 'lon': [-74.0450]}))

# --- LEGAL ---
elif menu == "⚖️ Legal y Seguridad":
    st.header("🔐 Seguridad y Legalidad")
    st.warning("Sistema protegido con Seguro Antihacker 24/7")
    st.write("© 2026 Tu Amigo Contable - Copy Write")
    with st.expander("Términos y Condiciones"):
        st.write("Detalles del servicio...")
    with st.expander("Política de Privacidad"):
        st.write("Tus datos están seguros...")

# ============================================
# 4. BOTÓN FLOTANTE IA
# ============================================
st.markdown(f"""
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 100;">
        <button style="border-radius: 50%; width: 60px; height: 60px; background-color: {COLOR_PRIMARIO}; color: white; border: none; font-size: 30px; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
            🤖
        </button>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ============================================
# 1. CONFIGURACIÓN Y PALETA DE COLORES
# ============================================
st.set_page_config(page_title="Tu Amigo Contable", layout="wide", initial_sidebar_state="collapsed")

# Colores extraídos de las imágenes de referencia
COLOR_PRIMARIO = "#345470"      # Azul petróleo (banner)
COLOR_FONDO = "#e1e8ee"         # Gris azulado de fondo
COLOR_TEXTO = "#1a1a1a"
COLOR_VERDE = "#92c83e"         # Verde para títulos y positivo
COLOR_ROJO = "#d9534f"          # Rojo para negativo (añadido)

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Roboto', sans-serif;
        background-color: {COLOR_FONDO};
    }}

    /* Encabezado principal con logo */
    .main-header {{
        background-color: {COLOR_PRIMARIO};
        padding: 30px 20px;
        color: white;
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
    }}
    .main-header .small-logo {{
        color: {COLOR_VERDE};
        font-size: 16px;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }}
    .main-header .big-logo {{
        color: {COLOR_VERDE};
        font-size: 36px;
        font-weight: 700;
        line-height: 1.2;
    }}
    .main-header .tagline {{
        color: white;
        font-size: 18px;
        margin-top: 5px;
    }}

    /* Tarjetas del dashboard */
    .card {{
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 15px;
    }}
    .card h2 {{
        color: {COLOR_PRIMARIO};
        font-size: 18px;
        margin-bottom: 5px;
    }}
    .card .valor {{
        font-size: 32px;
        font-weight: 700;
        color: {COLOR_TEXTO};
    }}
    .card .variacion {{
        font-size: 16px;
        font-weight: 500;
    }}
    .variacion.positiva {{ color: {COLOR_VERDE}; }}
    .variacion.negativa {{ color: {COLOR_ROJO}; }}

    /* Tabla de movimientos */
    .movimientos-titulo {{
        font-size: 24px;
        font-weight: 700;
        color: {COLOR_PRIMARIO};
        margin: 30px 0 15px 0;
        border-left: 5px solid {COLOR_VERDE};
        padding-left: 15px;
    }}

    /* Botones estilo global */
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

# Menú de navegación
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
    # Encabezado con logo
    st.markdown(f"""
    <div class='main-header'>
        <div class='small-logo'>igocontable.com</div>
        <div class='big-logo'>tuamigocontable.com</div>
        <div class='tagline'>Tu asistente contable inteligente</div>
    </div>
    """, unsafe_allow_html=True)

    # Tarjetas de resumen (INGRESOS, EGRESOS, BALANCE)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='card'>
            <h2>INGRESOS</h2>
            <div class='valor'>$1,500,000</div>
            <div class='variacion positiva'>+12%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='card'>
            <h2>EGRESOS</h2>
            <div class='valor'>$0</div>
            <div class='variacion negativa'>-5%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='card'>
            <h2>BALANCE</h2>
            <div class='valor'>$1,500,000</div>
            <div class='variacion positiva'>Positivo</div>
        </div>
        """, unsafe_allow_html=True)

    # Título de la tabla
    st.markdown("<div class='movimientos-titulo'>ÚLTIMOS MOVIMIENTOS</div>", unsafe_allow_html=True)

    # Tabla con los movimientos exactos de la imagen
    movimientos = pd.DataFrame({
        "Fecha": ["2024-03-15", "2024-03-15", "2024-03-15", "2024-03-20", "2024-03-20"],
        "Comprobante": ["FV-001", "FV-001", "FV-001", "FV-002", "FV-002"],
        "Cuenta": ["CLIENTES", "VENTAS", "IMPUESTOS POR PAGAR", "CAJA", "VENTAS"],
        "Detalle": ["Cliente", "Ventas", "IVA", "Efectivo", "Ventas"],
        "Débito": ["$1,190,000", "-", "-", "$500,000", "-"],
        "Crédito": ["-", "$1,000,000", "$190,000", "-", "$500,000"],
        "Tercero": ["Cliente A", "Cliente A", "Cliente A", "Cliente B", "Cliente B"]
    })
    st.table(movimientos)

    # Gráfico de crecimiento de usuarios (segunda imagen)
    st.markdown("<div class='movimientos-titulo'>CRECIMIENTO DE USUARIOS</div>", unsafe_allow_html=True)
    
    # Datos de la segunda imagen: Mes 2, Mes 6, Año 1 (12 meses)
    data_usuarios = pd.DataFrame({
        "Periodo": ["Mes 2", "Mes 6", "Año 1 (12)"],
        "Usuarios": [50, 500, 1000]
    })
    
    # Mostrar como gráfico de barras
    st.bar_chart(data_usuarios.set_index("Periodo"))
    
    # Opcional: mostrar los números en texto
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.metric("Mes 2", "50 Usuarios")
    with col_b: st.metric("Mes 6", "500 Usuarios")
    with col_c: st.metric("Año 1", "1000 Usuarios")

# --- OTRAS PÁGINAS (sin cambios importantes) ---
elif menu == "📈 Reportes y Facturas":
    st.header("📄 Gestión de Documentos")
    st.write("Genera facturas profesionales y descarga plantillas desde tu carpeta 'tabla'.")
    st.button("📥 Descargar Balance (Excel)")
    st.button("📂 Exportar Plantilla Profesional")

elif menu == "🏢 Nuestra Empresa":
    st.header("Acerca de Tu Amigo Contable")
    st.write("**Misión:** Facilitar la contabilidad de cada hogar y empresa.")
    st.write("**Visión:** Ser el líder global en asistencia contable por IA.")
    st.write("**Objetivos:** Seguridad, Rapidez y Transparencia.")

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

elif menu == "📞 Contáctanos":
    st.header("📍 Ubicación y Contacto")
    st.write("Cedritos, Bogotá, Colombia")
    st.map(pd.DataFrame({'lat': [4.7228], 'lon': [-74.0450]}))

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
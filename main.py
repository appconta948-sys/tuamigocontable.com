import streamlit as st
import pandas as pd

# ============================================
# 1. CONFIGURACIÓN Y PALETA DE COLORES
# ============================================
st.set_page_config(page_title="Tu Amigo Contable", layout="wide", initial_sidebar_state="collapsed")

# Colores de tu imagen
COLOR_PRIMARIO = "#345470"  # Azul petróleo
COLOR_FONDO = "#e1e8ee"     # Gris azulado
COLOR_TEXTO = "#1a1a1a"
COLOR_VERDE = "#92c83e"      # Verde de los títulos

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Roboto', sans-serif;
        background-color: {COLOR_FONDO};
    }}

    .main-header {{
        background-color: {COLOR_PRIMARIO};
        padding: 40px 20px;
        color: {COLOR_VERDE};
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
    }}
    .main-header h1 {{ font-size: 35px; font-weight: 700; color: {COLOR_VERDE} !important; }}

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
# 2. LOGIN SIMULADO (solo botón de Google)
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

# ============================================
# 3. MENÚ DE NAVEGACIÓN
# ============================================
menu = st.sidebar.selectbox("Ir a:", [
    "🏠 Dashboard", 
    "📈 Reportes y Facturas", 
    "🏢 Nuestra Empresa", 
    "💳 Suscripción (Global)", 
    "📞 Contáctanos", 
    "⚖️ Legal y Seguridad"
])

# ============================================
# 4. DASHBOARD (como en tu primera imagen)
# ============================================
if menu == "🏠 Dashboard":
    st.markdown(f"<div class='main-header'><h1>MIRA TU BALANCE AQUÍ</h1><p style='color:white'>Tu resumen financiero inteligente</p></div>", unsafe_allow_html=True)
    
    # Cuatro tarjetas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='card'><h2>Balance Actual</h2><p>$470.00</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><h2>Consumo Mes</h2><p>$4,980.00</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'><h2>Reportes</h2><p>12 Listos</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='card'><h2>IA Tips</h2><p>5 Pendientes</p></div>", unsafe_allow_html=True)
    
    # Registro diario
    st.subheader("📝 Registro Diario")
    st.table(pd.DataFrame({
        "Fecha": ["2026-03-18", "2026-03-19", "2026-03-20"],
        "Detalle": ["Pago Nómina", "Venta Software", "Compra Insumos"],
        "Monto": ["$500.00", "$1,200.00", "$300.00"]
    }))

# ============================================
# 5. OTRAS PÁGINAS (simples)
# ============================================
elif menu == "📈 Reportes y Facturas":
    st.header("📄 Gestión de Documentos")
    st.write("Aquí irían los reportes y facturas.")
    st.button("📥 Descargar Balance (Excel)")
    st.button("📂 Exportar Plantilla Profesional")

elif menu == "🏢 Nuestra Empresa":
    st.header("Acerca de Tu Amigo Contable")
    st.write("**Misión:** Facilitar la contabilidad de cada hogar y empresa.")
    st.write("**Visión:** Ser el líder global en asistencia contable por IA.")

elif menu == "💳 Suscripción (Global)":
    st.header("💳 Planes y Pagos")
    st.success("7 días de prueba GRATIS habilitados")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='card'><h3>Mensual</h3><p>$10 USD</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Mensual", key="men")
    with col2:
        st.markdown("<div class='card'><h3>Trimestral</h3><p>$25 USD</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Trimestral", key="tri")
    with col3:
        st.markdown("<div class='card'><h3>Anual</h3><p>$99 USD</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Anual", key="an")
    st.caption("Los pagos se convierten a tu moneda local.")

elif menu == "📞 Contáctanos":
    st.header("📍 Ubicación y Contacto")
    st.write("Cedritos, Bogotá, Colombia")
    st.map(pd.DataFrame({'lat': [4.7228], 'lon': [-74.0450]}))

elif menu == "⚖️ Legal y Seguridad":
    st.header("🔐 Seguridad y Legalidad")
    st.warning("Sistema protegido con Seguro Antihacker 24/7")
    st.write("© 2026 Tu Amigo Contable - Todos los derechos reservados.")
    with st.expander("Términos y Condiciones"):
        st.write("Términos del servicio...")
    with st.expander("Política de Privacidad"):
        st.write("Privacidad de datos...")

# ============================================
# 6. BOTÓN FLOTANTE IA (opcional)
# ============================================
st.markdown(f"""
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 100;">
        <button style="border-radius: 50%; width: 60px; height: 60px; background-color: {COLOR_PRIMARIO}; color: white; border: none; font-size: 30px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
            🤖
        </button>
    </div>
""", unsafe_allow_html=True)

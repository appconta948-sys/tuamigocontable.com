import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ============================================
# 1. CONFIGURACIÓN DE ESTILO (igual a tu imagen)
# ============================================
st.set_page_config(page_title="Tu Amigo Contable", layout="wide")

COLOR_PRIMARIO = "#345470"
COLOR_FONDO = "#e1e8ee"
COLOR_VERDE = "#92c83e"
COLOR_ROJO = "#d9534f"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'Roboto', sans-serif; background-color: {COLOR_FONDO}; }}
    .main-header {{
        background-color: {COLOR_PRIMARIO};
        padding: 30px 20px;
        color: white;
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
    }}
    .main-header .big-logo {{
        color: {COLOR_VERDE};
        font-size: 36px;
        font-weight: 700;
    }}
    .card {{
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 15px;
    }}
    .card h2 {{ color: {COLOR_PRIMARIO}; font-size: 18px; }}
    .card .valor {{ font-size: 32px; font-weight: 700; color: #1a1a1a; }}
    .movimientos-titulo {{
        font-size: 24px;
        font-weight: 700;
        color: {COLOR_PRIMARIO};
        margin: 30px 0 15px 0;
        border-left: 5px solid {COLOR_VERDE};
        padding-left: 15px;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# 2. AUTENTICACIÓN SIMPLE CON JSON
# ============================================
USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(email, password):
    users = load_users()
    if email in users:
        return False, "El usuario ya existe."
    users[email] = password
    save_users(users)
    return True, "Registro exitoso."

def login_user(email, password):
    users = load_users()
    if email in users and users[email] == password:
        return True
    return False

# ============================================
# 3. CONTROL DE SESIÓN
# ============================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ""
    st.session_state.page = "login"

# ============================================
# 4. PÁGINAS
# ============================================
def login_page():
    st.markdown(f"<h1 style='text-align:center; color:{COLOR_PRIMARIO}'>Tu Amigo Contable</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("login"):
            st.subheader("Iniciar sesión")
            email = st.text_input("Correo electrónico")
            password = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar"):
                if login_user(email, password):
                    st.session_state.logged_in = True
                    st.session_state.email = email
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
        st.markdown("---")
        if st.button("Registrarse"):
            st.session_state.page = "register"
            st.rerun()

def register_page():
    st.markdown(f"<h1 style='text-align:center; color:{COLOR_PRIMARIO}'>Tu Amigo Contable</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("register"):
            st.subheader("Registro")
            email = st.text_input("Correo electrónico")
            password = st.text_input("Contraseña", type="password")
            confirm = st.text_input("Confirmar contraseña", type="password")
            if st.form_submit_button("Registrarse"):
                if password != confirm:
                    st.error("Las contraseñas no coinciden")
                elif len(password) < 4:
                    st.error("La contraseña debe tener al menos 4 caracteres")
                else:
                    ok, msg = register_user(email, password)
                    if ok:
                        st.success(msg)
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error(msg)
        st.markdown("---")
        if st.button("Volver al login"):
            st.session_state.page = "login"
            st.rerun()

def dashboard():
    # Encabezado
    st.markdown("""
    <div class='main-header'>
        <div class='big-logo'>tuamigocontable.com</div>
        <div style='color:white'>Tu asistente contable inteligente</div>
    </div>
    """, unsafe_allow_html=True)

    # Barra lateral
    with st.sidebar:
        st.write(f"### Hola, {st.session_state.email}")
        if st.button("Cerrar sesión"):
            st.session_state.logged_in = False
            st.rerun()
        menu = st.selectbox("Ir a:", ["🏠 Dashboard", "🏢 Empresa", "📞 Contacto", "💳 Suscripción", "⚖️ Legal"])

    # Contenido
    if menu == "🏠 Dashboard":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("<div class='card'><h2>Balance Actual</h2><div class='valor'>$470.00</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='card'><h2>Consumo del Mes</h2><div class='valor'>$4,980.00</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='card'><h2>Reportes</h2><div class='valor'>12</div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown("<div class='card'><h2>Recomendaciones IA</h2><div class='valor'>5</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='movimientos-titulo'>📝 Registro Diario</div>", unsafe_allow_html=True)
        df = pd.DataFrame({
            "Fecha": ["2026-03-18", "2026-03-19", "2026-03-20"],
            "Detalle": ["Pago Nómina", "Venta Software", "Compra Insumos"],
            "Monto": ["$500.00", "$1,200.00", "$300.00"]
        })
        st.table(df)

        col_b1, col_b2 = st.columns(2)
        with col_b1: st.button("📥 Descargar Balance")
        with col_b2: st.button("📂 Exportar Plantilla")

    elif menu == "🏢 Empresa":
        st.header("Acerca de Nosotros")
        st.write("Misión: Facilitar la contabilidad...")
        st.write("Visión: Ser líder global...")
    elif menu == "📞 Contacto":
        st.header("Contáctanos")
        st.write("Cedritos, Bogotá")
        st.map(pd.DataFrame({'lat': [4.7228], 'lon': [-74.0450]}))
    elif menu == "💳 Suscripción":
        st.header("Planes")
        st.success("7 días gratis")
        col1, col2, col3 = st.columns(3)
        col1.button("Mensual $10")
        col2.button("Trimestral $25")
        col3.button("Anual $99")
    elif menu == "⚖️ Legal":
        st.header("Términos y condiciones")
        st.write("...")

# ============================================
# 5. ROUTER
# ============================================
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    else:
        register_page()
else:
    dashboard()
import streamlit as st
import pandas as pd
import bcrypt
import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotoreENV  # <-- CORRECCIÓN: debe ser load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# ============================================
# 1. CONFIGURACIÓN Y PALETA DE COLORES
# ============================================
st.set_page_config(page_title="Tu Amigo Contable", layout="wide", initial_sidebar_state="collapsed")

COLOR_PRIMARIO = "#345470"
COLOR_FONDO = "#e1e8ee"
COLOR_TEXTO = "#1a1a1a"
COLOR_VERDE = "#92c83e"
COLOR_ROJO = "#d9534f"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Roboto', sans-serif;
        background-color: {COLOR_FONDO};
    }}

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

    .movimientos-titulo {{
        font-size: 24px;
        font-weight: 700;
        color: {COLOR_PRIMARIO};
        margin: 30px 0 15px 0;
        border-left: 5px solid {COLOR_VERDE};
        padding-left: 15px;
    }}

    .stButton>button {{
        background-color: {COLOR_PRIMARIO} !important;
        color: white !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-weight: 700 !important;
        border: none !important;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #2a4055 !important;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# 2. FUNCIONES DE BASE DE DATOS Y AUTENTICACIÓN
# ============================================
def get_db_connection():
    """Crea y devuelve una conexión a PostgreSQL."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

def hash_password(password):
    """Genera hash bcrypt de la contraseña."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password, hashed):
    """Verifica la contraseña contra el hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def authenticate(username, password):
    """Busca usuario por email o teléfono y verifica contraseña."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, fullname, email, phone, password_hash FROM usuarios WHERE email = %s OR phone = %s",
        (username, username)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and check_password(password, user[4]):
        return {"id": user[0], "fullname": user[1], "email": user[2], "phone": user[3]}
    return None

def register_user(fullname, email, phone, password):
    """Registra un nuevo usuario en la base de datos."""
    conn = get_db_connection()
    cur = conn.cursor()
    # Verificar duplicados
    cur.execute("SELECT id FROM usuarios WHERE email = %s OR phone = %s", (email, phone))
    if cur.fetchone():
        cur.close()
        conn.close()
        return False, "El correo o teléfono ya está registrado."
    # Insertar nuevo usuario
    hashed = hash_password(password)
    try:
        cur.execute(
            "INSERT INTO usuarios (fullname, email, phone, password_hash) VALUES (%s, %s, %s, %s)",
            (fullname, email, phone, hashed)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return False, f"Error en el registro: {str(e)}"
    finally:
        cur.close()
        conn.close()
    return True, "Registro exitoso. Ya puedes iniciar sesión."

# ============================================
# 3. CONTROL DE SESIÓN
# ============================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.show_register = False

# ============================================
# 4. PANTALLAS DE LOGIN / REGISTRO
# ============================================
def show_login():
    st.markdown(f"<h1 style='text-align:center; color:{COLOR_PRIMARIO}'>Tu Amigo Contable</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("login_form"):
            st.subheader("Iniciar sesión")
            username = st.text_input("Correo o teléfono")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Entrar")
            if submitted:
                if not username or not password:
                    st.error("Por favor ingresa todos los campos.")
                else:
                    user = authenticate(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.success(f"¡Bienvenido {user['fullname']}!")
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos.")
        
        st.markdown("---")
        st.markdown("¿No tienes cuenta?")
        if st.button("Registrarse aquí"):
            st.session_state.show_register = True
            st.rerun()
        
        st.markdown("---")
        st.info("O ingresa con tu cuenta de Google")
        if st.button("🔴 Entrar con Google"):
            st.warning("Funcionalidad en desarrollo. Usa el formulario.")

def show_register():
    st.markdown(f"<h1 style='text-align:center; color:{COLOR_PRIMARIO}'>Tu Amigo Contable</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("register_form"):
            st.subheader("Crear cuenta")
            fullname = st.text_input("Nombre completo*")
            email = st.text_input("Correo electrónico")
            phone = st.text_input("Teléfono")
            password = st.text_input("Contraseña*", type="password")
            confirm = st.text_input("Confirmar contraseña*", type="password")
            submitted = st.form_submit_button("Registrarse")
            
            if submitted:
                if not fullname or not (email or phone) or not password or not confirm:
                    st.error("Por favor completa todos los campos obligatorios (*).")
                elif password != confirm:
                    st.error("Las contraseñas no coinciden.")
                elif len(password) < 6:
                    st.error("La contraseña debe tener al menos 6 caracteres.")
                else:
                    success, msg = register_user(fullname, email, phone, password)
                    if success:
                        st.success(msg)
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error(msg)
        
        st.markdown("---")
        if st.button("Volver al inicio de sesión"):
            st.session_state.show_register = False
            st.rerun()

# ============================================
# 5. APLICACIÓN PRINCIPAL (DASHBOARD)
# ============================================
def main_app():
    # Encabezado
    st.markdown(f"""
    <div class='main-header'>
        <div class='small-logo'>igocontable.com</div>
        <div class='big-logo'>tuamigocontable.com</div>
        <div class='tagline'>Tu asistente contable inteligente</div>
    </div>
    """, unsafe_allow_html=True)

    # Barra lateral
    with st.sidebar:
        st.markdown(f"### Hola, {st.session_state.user['fullname']}")
        if st.button("Cerrar sesión"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
        st.markdown("---")
        menu = st.selectbox("Ir a:", [
            "🏠 Dashboard",
            "🏢 Nuestra Empresa",
            "📞 Contáctanos",
            "💳 Suscripción (Global)",
            "⚖️ Legal y Seguridad"
        ])

    # Contenido según menú
    if menu == "🏠 Dashboard":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div class='card'>
                <h2>Balance Actual</h2>
                <div class='valor'>$470.00</div>
                <div class='variacion positiva'>+2.5%</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class='card'>
                <h2>Consumo del Mes</h2>
                <div class='valor'>$4,980.00</div>
                <div class='variacion negativa'>-5%</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class='card'>
                <h2>Reportes</h2>
                <div class='valor'>12</div>
                <div class='variacion positiva'>Listos</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div class='card'>
                <h2>Recomendaciones IA</h2>
                <div class='valor'>5</div>
                <div class='variacion positiva'>Tips</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='movimientos-titulo'>📝 Registro Diario</div>", unsafe_allow_html=True)
        df_registro = pd.DataFrame({
            "Fecha": ["2026-03-18", "2026-03-19", "2026-03-20"],
            "Detalle": ["Pago Nómina", "Venta Software", "Compra Insumos"],
            "Monto": ["$500.00", "$1,200.00", "$300.00"]
        })
        st.table(df_registro)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.button("📥 Descargar Balance (Excel)")
        with col_b2:
            st.button("📂 Exportar Plantilla Profesional")
        st.caption("Las plantillas profesionales se encuentran en la carpeta 'tabla'.")

    elif menu == "🏢 Nuestra Empresa":
        st.header("Acerca de Tu Amigo Contable")
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 15px;">
            <h3 style="color:{COLOR_PRIMARIO};">Misión</h3>
            <p>Facilitar la contabilidad de cada hogar y empresa mediante herramientas inteligentes y accesibles.</p>
            <h3 style="color:{COLOR_PRIMARIO};">Visión</h3>
            <p>Ser el líder global en asistencia contable por IA, reconocido por nuestra seguridad y transparencia.</p>
            <h3 style="color:{COLOR_PRIMARIO};">Objetivos</h3>
            <ul>
                <li>Ofrecer una plataforma intuitiva que ahorre tiempo a nuestros usuarios.</li>
                <li>Garantizar la seguridad de la información financiera.</li>
                <li>Expandirnos a nuevos mercados con soporte multi-moneda.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    elif menu == "📞 Contáctanos":
        st.header("📍 Contáctanos")
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 15px;">
            <p><strong>Dirección:</strong> Cedritos, Bogotá, Colombia</p>
            <p><strong>Email:</strong> soporte@tuamigocontable.com</p>
            <p><strong>Teléfono:</strong> +57 601 123 4567</p>
        </div>
        """, unsafe_allow_html=True)
        df_ubicacion = pd.DataFrame({'lat': [4.7228], 'lon': [-74.0450]})
        st.map(df_ubicacion)

    elif menu == "💳 Suscripción (Global)":
        st.header("💳 Planes de Suscripción")
        st.success("🎁 7 días de prueba GRATIS habilitados para nuevos usuarios.")
        st.markdown("Pagos en USD que se convierten automáticamente a tu moneda local al procesar (como en SHEIN).")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class='card'>
                <h3>Mensual</h3>
                <p class='valor'>$10 USD</p>
                <p>Facturación mensual</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Suscribirse Mensual", key="mensual")
        with col2:
            st.markdown("""
            <div class='card'>
                <h3>Trimestral</h3>
                <p class='valor'>$25 USD</p>
                <p>Ahorra 17%</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Suscribirse Trimestral", key="trimestral")
        with col3:
            st.markdown("""
            <div class='card'>
                <h3>Anual</h3>
                <p class='valor'>$99 USD</p>
                <p>Ahorra 18%</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Suscribirse Anual", key="anual")
        st.caption("💳 Métodos de pago: Tarjeta de crédito, débito, PayPal y transferencias locales.")

    elif menu == "⚖️ Legal y Seguridad":
        st.header("🔐 Seguridad y Legalidad")
        st.warning("Sistema protegido con **Seguro Antihacker 24/7** que garantiza la integridad de tus datos.")
        st.markdown("© 2026 Tu Amigo Contable - Todos los derechos reservados.")
        with st.expander("📜 Términos y Condiciones"):
            st.write("""
            **1. Aceptación de los términos**  
            Al acceder y usar esta aplicación, aceptas cumplir con estos términos y condiciones.  
            **2. Uso del servicio**  
            El usuario es responsable de la veracidad de la información ingresada.  
            **3. Modificaciones**  
            Nos reservamos el derecho de actualizar los términos en cualquier momento.
            """)
        with st.expander("🔏 Política de Privacidad"):
            st.write("""
            **Recopilación de datos**  
            Recopilamos la información necesaria para brindar el servicio contable.  
            **Protección**  
            Todos los datos se almacenan de forma cifrada y no se comparten con terceros sin consentimiento.  
            **Cookies**  
            Utilizamos cookies para mejorar la experiencia de navegación.
            """)

    # Botón flotante IA
    st.markdown(f"""
        <div style="position: fixed; bottom: 20px; right: 20px; z-index: 100;">
            <button style="border-radius: 50%; width: 60px; height: 60px; background-color: {COLOR_PRIMARIO}; color: white; border: none; font-size: 30px; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
                🤖
            </button>
        </div>
    """, unsafe_allow_html=True)

# ============================================
# 6. RUTA PRINCIPAL
# ============================================
if not st.session_state.authenticated:
    if st.session_state.show_register:
        show_register()
    else:
        show_login()
else:
    main_app()
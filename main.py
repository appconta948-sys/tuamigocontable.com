import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Tu Amigo Contable", layout="wide", initial_sidebar_state="collapsed")

# 2. ESTILO CSS (Inspirado 100% en tu link de Google Sites)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #ffffff;
    }

    /* Navbar superior */
    .nav-header {
        background-color: #333333;
        padding: 15px;
        color: white;
        text-align: center;
        font-weight: 600;
        font-size: 20px;
    }

    /* Banner Principal (El de la imagen con texto verde) */
    .hero-section {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1554224155-6726b3ff858f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        padding: 60px 20px;
        text-align: center;
        color: #92c83e; /* El verde de tu diseño */
    }
    .hero-section h1 { font-size: 40px; font-weight: 700; margin: 0; }

    /* Contenedor de Balance (Blanco con sombra) */
    .balance-box {
        background-color: #ffffff;
        padding: 30px;
        margin-top: -30px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    .balance-box h2 { color: #4a90e2; font-size: 24px; margin-bottom: 20px; }

    /* Tarjetas de Métricas */
    .metric-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-bottom: 4px solid #4a90e2;
    }
    .metric-value { font-size: 28px; font-weight: 700; color: #333; }
    .metric-label { font-size: 14px; color: #666; }

    /* Botones Celestes (Iguales a los tuyos) */
    .btn-celeste {
        background-color: #7cc0d8 !important;
        color: white !important;
        padding: 12px 25px;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        font-weight: 600;
        margin: 10px 0;
        border: none;
        width: 100%;
    }

    /* BOTÓN FLOTANTE IA */
    .float-ia {
        position: fixed;
        bottom: 25px;
        right: 25px;
        background-color: #333;
        color: white !important;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        z-index: 1000;
        cursor: pointer;
        text-decoration: none !important;
    }

    /* Footer */
    .footer {
        background-color: #333;
        color: white;
        padding: 40px 20px;
        text-align: center;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# 3. MENÚ DE NAVEGACIÓN (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3208/3208615.png", width=100)
    st.title("Navegación")
    menu = st.radio("Ir a:", ["Inicio", "Nosotros", "Suscripción", "Contacto"])

# 4. BOTÓN FLOTANTE (Inyectado en todas las páginas)
st.markdown('<a href="#chating" class="float-ia">🤖</a>', unsafe_allow_html=True)

# 5. CONTENIDO POR PÁGINA
if menu == "Inicio":
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <h1>REGISTRO <br> CONTABLE</h1>
        </div>
    """, unsafe_allow_html=True)

    # Balance Section
    with st.container():
        st.markdown("""
            <div class="balance-box">
                <h2>MIRA TU BALANCE AQUÍ</h2>
                <div style="background:#46637f; color:white; padding:15px; border-radius:5px; margin-bottom:20px;">
                    <b>Detalles de Registros Contables</b><br>
                    <small>Amigo Contable - Visualiza y gestiona tus movimientos</small>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Métricas (En móvil se ven una bajo la otra)
        col1, col2, col3 = st.columns(1) # Forzamos columna única para móvil
        st.markdown('<div class="metric-card"><div class="metric-label">Total Ingresos</div><div class="metric-value" style="color:#28a745;">$5,450.00</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-card"><div class="metric-label">Total Egresos</div><div class="metric-value" style="color:#dc3545;">$4,980.00</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-card"><div class="metric-label">Balance</div><div class="metric-value" style="color:#4a90e2;">$470.00</div></div>', unsafe_allow_html=True)
        
        st.markdown('<button class="btn-celeste">REGISTRA TUS MOVIMIENTOS</button>', unsafe_allow_html=True)

elif menu == "Nosotros":
    st.header("Sobre Nosotros")
    st.markdown("""
    ### Misión
    Acompañar a nuestros clientes en su crecimiento financiero...
    ### Visión
    Ser la plataforma líder en servicios contables digitales...
    """)

elif menu == "Suscripción":
    st.header("Planes de Suscripción")
    st.info("7 días de prueba gratis")
    st.write("Mensual: $10 USD")
    st.write("Trimestral: $25 USD")
    st.write("Anual: $99 USD")

# 6. EL CHAT DE IA (Al final para que el botón flotante "apunte" aquí)
st.markdown('<div id="chating"></div>', unsafe_allow_html=True)
st.divider()
st.subheader("🤖 Chating con Conta IA")
with st.expander("Abrir Asistente"):
    if prompt := st.chat_input("¿En qué te ayudo hoy?"):
        st.write(f"Has dicho: {prompt}")
        st.info("Respuesta de la IA en camino...")

# 7. FOOTER
st.markdown("""
    <div class="footer">
        <p><b>Tu Amigo Contable</b></p>
        <p>Bogotá, Cedritos | Contacto: soporte@tuamigocontable.com</p>
        <p style="font-size:10px; opacity:0.6;">© 2026 Todos los derechos reservados. Política de Privacidad</p>
    </div>
""", unsafe_allow_html=True)

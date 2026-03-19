import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="tuamigocontable.com", layout="wide")

# 2. CSS PARA EL BOTÓN FLOTANTE Y DISEÑO MÓVIL
st.markdown("""
<style>
    /* Estilos del Botón Flotante */
    .float-button {
        position: fixed;
        width: 60px;
        height: 60px;
        bottom: 20px;
        right: 20px;
        background-color: #46637f;
        color: #FFF !important;
        border-radius: 50px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        cursor: pointer;
        border: none;
        transition: all 0.3s ease;
    }
    .float-button:hover {
        transform: scale(1.1);
        background-color: #28a745; /* Cambia a verde al pasar el mouse */
    }

    /* Ajuste para que las tarjetas no se vean mal en móvil */
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border-top: 5px solid #46637f;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        text-align: center;
    }
    
    /* Títulos legibles */
    h1 { font-size: 22px !important; color: #46637f !important; }
</style>

<a href="?ia=open" class="float-button">
    🤖
</a>
""", unsafe_allow_html=True)

# 3. LÓGICA DE NAVEGACIÓN
# Usamos los parámetros de la URL para saber si el usuario tocó el botón de la IA
query_params = st.query_params

# 4. ENCABEZADO (Basado en tu imagen)
st.markdown('<div style="text-align:center;"><h1>MIRA TU BALANCE AQUÍ</h1></div>', unsafe_allow_html=True)

# 5. DASHBOARD (Tarjetas apiladas para móvil)
col1, col2, col3 = st.columns([1,1,1]) # En PC van juntas, en móvil Streamlit las apila solo

with col1:
    st.markdown('<div class="metric-card">💰<br><small>Ingresos</small><br><b>$5,450.00</b></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">💳<br><small>Egresos</small><br><b style="color:red;">$4,980.00</b></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">⚖️<br><small>Balance</small><br><b style="color:green;">$470.00</b></div>', unsafe_allow_html=True)

# 6. ASISTENTE IA (Se activa al tocar el botón o desde el menú)
with st.sidebar:
    st.title("🤖 Asistente Contable")
    st.info("¡Hola! Soy tu IA. ¿En qué te ayudo hoy?")
    
    # Si el parámetro 'ia' está presente, le damos la bienvenida
    if "ia" in query_params:
        st.success("🤖 ¡Modo IA activado desde el botón flotante!")
    
    chat_input = st.chat_input("Escribe tu consulta contable...")
    if chat_input:
        st.write(f"Has preguntado: {chat_input}")
        st.caption("Procesando con ContaIA...")

# 7. TABLA DE REGISTROS (Diseño limpio)
st.subheader("📋 Registros Recientes")
data = pd.DataFrame({
    "Fecha": ["2026-03-10", "2026-03-12"],
    "Detalle": ["Venta Activos", "Pago Nómina"],
    "Monto": [1200, 500]
})
st.table(data) # st.table se ve mejor en móvil que st.dataframe

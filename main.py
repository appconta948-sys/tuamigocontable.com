# ============================================
# CONFIGURACIÓN DE ESTILOS - PALETA PERSONALIZADA
# ROJO, AZUL, VERDE NEÓN, AMARILLO, BLANCO, NEGRO
# ============================================
st.markdown("""
<style>
    /* Estilos generales */
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        color: white;
    }
    
    /* Tarjetas de métricas - ESTILO NEÓN */
    .metric-card {
        background: #111111;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
        border: 2px solid #00ff00;
        transition: all 0.3s ease;
        text-align: center;
        margin: 10px 0;
    }
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 0 30px #00ff00;
        border-color: #00ff00;
    }
    .metric-card.rojo {
        border-color: #ff0000;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
    }
    .metric-card.rojo:hover {
        box-shadow: 0 0 30px #ff0000;
    }
    .metric-card.azul {
        border-color: #0000ff;
        box-shadow: 0 0 20px rgba(0, 0, 255, 0.3);
    }
    .metric-card.azul:hover {
        box-shadow: 0 0 30px #0000ff;
    }
    .metric-card.amarillo {
        border-color: #ffff00;
        box-shadow: 0 0 20px rgba(255, 255, 0, 0.3);
    }
    .metric-card.amarillo:hover {
        box-shadow: 0 0 30px #ffff00;
    }
    .metric-title {
        color: #ffffff;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 36px;
        font-weight: bold;
        margin: 10px 0;
        text-shadow: 0 0 10px currentColor;
    }
    .metric-icon {
        font-size: 50px;
        margin-bottom: 10px;
        filter: drop-shadow(0 0 10px currentColor);
    }
    
    /* Botones de acción - ESTILO VIBRANTE */
    .action-button {
        background: linear-gradient(135deg, #ff0000, #0000ff, #00ff00, #ffff00);
        background-size: 300% 300%;
        animation: gradient 5s ease infinite;
        color: white;
        padding: 15px 25px;
        border: none;
        border-radius: 15px;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        margin: 5px;
        box-shadow: 0 0 20px rgba(255,255,255,0.3);
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .action-button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255,255,255,0.5);
    }
    
    /* Tabla de movimientos - ESTILO NEÓN */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.2);
        border: 2px solid #00ff00;
    }
    .dataframe th {
        background: linear-gradient(135deg, #000000, #1a1a1a);
        color: #00ff00;
        font-weight: bold;
        padding: 15px !important;
        font-size: 16px;
        border-bottom: 2px solid #00ff00;
    }
    .dataframe td {
        padding: 12px !important;
        border-bottom: 1px solid #333;
        color: white;
    }
    .dataframe tr:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    /* Chat - ESTILO NEÓN */
    .chat-container {
        background: #111111;
        border-radius: 20px;
        padding: 25px;
        margin-top: 30px;
        border: 2px solid #00ff00;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.2);
    }
    .chat-title {
        color: #00ff00 !important;
        font-size: 24px;
        margin-bottom: 20px;
        text-shadow: 0 0 10px #00ff00;
    }
    
    /* Títulos y textos */
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 0 0 10px #00ff00;
    }
    h1 {
        font-size: 48px !important;
        background: linear-gradient(135deg, #ff0000, #0000ff, #00ff00, #ffff00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 5s ease infinite;
        background-size: 300% 300%;
    }
    
    /* Inputs y selects */
    .stTextInput input, .stSelectbox select {
        background: #111111 !important;
        color: white !important;
        border: 2px solid #00ff00 !important;
        border-radius: 10px !important;
    }
    .stTextInput input:focus, .stSelectbox select:focus {
        box-shadow: 0 0 20px #00ff00 !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        margin-top: 50px;
        color: rgba(255,255,255,0.7);
        border-top: 2px solid #00ff00;
        background: #111111;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# ENCABEZADO CON EFECTO NEÓN
# ============================================
st.markdown("""
<div style="text-align: center; padding: 30px 0;">
    <h1>📊 TUAMIGOCONTABLE.COM</h1>
    <p style="color: #00ff00; font-size: 20px; text-shadow: 0 0 10px #00ff00;">
        ⚡ Tu asistente contable inteligente ⚡
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# MÉTRICAS EN TARJETAS DE COLORES
# ============================================
ingresos = st.session_state.libro.obtener_ingresos_mes()
egresos = st.session_state.libro.obtener_egresos_mes()
balance = ingresos - egresos

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card verde">
        <div class="metric-icon">🟢</div>
        <div class="metric-title">INGRESOS DEL MES</div>
        <div class="metric-value" style="color: #00ff00;">${ingresos:,.0f}</div>
        <div style="color: #00ff00;">↑ +12%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card rojo">
        <div class="metric-icon">🔴</div>
        <div class="metric-title">EGRESOS DEL MES</div>
        <div class="metric-value" style="color: #ff0000;">${egresos:,.0f}</div>
        <div style="color: #ff0000;">↓ -5%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card azul">
        <div class="metric-icon">🔵</div>
        <div class="metric-title">BALANCE DEL MES</div>
        <div class="metric-value" style="color: #0000ff;">${balance:,.0f}</div>
        <div style="color: #0000ff;">⚖️ Positivo</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# BOTONES DE ACCIÓN (CON ESTILO GRADIENTE)
# ============================================
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("""
    <div class="action-button" onclick="alert('Factura en desarrollo')">
        📄 FACTURA
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="action-button" onclick="alert('Inventario en desarrollo')">
        📦 INVENTARIO
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="action-button" onclick="alert('Balance en desarrollo')">
        ⚖️ BALANCE
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="action-button" onclick="alert('IA en desarrollo')">
        🤖 IA
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="action-button" onclick="document.getElementById('export-btn').click()">
        📥 EXPORTAR
    </div>
    """, unsafe_allow_html=True)

# Botón oculto para exportar (funcional)
json_str = json.dumps(st.session_state.libro.asientos, indent=2, default=str)
st.download_button(
    label="Descargar",
    data=json_str,
    file_name=f"asientos_{datetime.now().strftime('%Y%m%d')}.json",
    mime="application/json",
    key="export-btn"
)

# ============================================
# TABLA DE MOVIMIENTOS (ESTILO NEÓN)
# ============================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<h2 style="color: #00ff00;">📋 ÚLTIMOS MOVIMIENTOS</h2>', unsafe_allow_html=True)

data = []
for a in st.session_state.libro.asientos[-10:]:
    for m in a["movimientos"]:
        # Determinar icono según tipo
        icono = "🔴" if m["debito"] > 0 else "🟢"
        data.append({
            " ": icono,
            "Fecha": a["fecha"],
            "Comprobante": a["comprobante"],
            "Cuenta": m["nombre"],
            "Detalle": m["detalle"][:30] if m["detalle"] else "-",
            "Débito": f"${m['debito']:,.0f}" if m['debito'] > 0 else "-",
            "Crédito": f"${m['credito']:,.0f}" if m['credito'] > 0 else "-",
            "Tercero": a["tercero"][:15] if a["tercero"] else "-"
        })

df = pd.DataFrame(data)

# Aplicar estilos a la tabla
styled_df = df.style.applymap(
    lambda x: 'color: #00ff00' if x == '🟢' else ('color: #ff0000' if x == '🔴' else 'color: #ffffff'),
    subset=[' ']
)

st.dataframe(styled_df, use_container_width=True, height=400)

# ============================================
# CHAT CON ESTILO AMARILLO
# ============================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="chat-container">
    <h2 class="chat-title">🤖 ASISTENTE IA - CHATGPT</h2>
""", unsafe_allow_html=True)

mensaje = st.chat_input("💬 Escribe tu consulta contable aquí...")
if mensaje:
    st.info("⚡ Funcionalidad IA en desarrollo - Pronto estará disponible")

st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# FOOTER CON COLORES
# ============================================
st.markdown("""
<div class="footer">
    <p style="font-size: 16px; margin-bottom: 10px;">
        <span style="color: #ff0000;">❤️</span> 
        <span style="color: #0000ff;">💙</span> 
        <span style="color: #00ff00;">💚</span> 
        <span style="color: #ffff00;">💛</span>
    </p>
    <p>© 2024 tuamigocontable.com - Todos los derechos reservados</p>
    <p style="font-size: 12px; color: #00ff00;">⚡ Modo Neón Activado ⚡</p>
</div>
""", unsafe_allow_html=True)

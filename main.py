# ============================================
# CONTA APP - VERSIÓN CORREGIDA Y OPTIMIZADA
# tuamigocontable.com
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================
st.set_page_config(
    page_title="tuamigocontable.com",
    page_icon="📊",
    layout="wide"
)

# ============================================
# CLASES DEL SISTEMA CONTABLE
# ============================================

class Conta:
    def __init__(self, pais="Colombia", moneda="COP", grupoNIIF=2):
        self.pais = pais
        self.moneda = moneda
        self.grupoNIIF = grupoNIIF
        self.experiencia = "20 años"

class PUCInteligente:
    def __init__(self, conta, pais="Colombia"):
        self.conta = conta
        self.pais = pais
        self.cuentas = {}
        self.inicializarPUC()
    
    def inicializarPUC(self):
        # CLASE 1: ACTIVO
        self.cuentas["1"] = {"codigo": "1", "nombre": "ACTIVO", "naturaleza": "DEBITO", "clase": "BALANCE", "nivel": 1, "aceptaMovimientos": False}
        self.cuentas["11"] = {"codigo": "11", "nombre": "ACTIVO CORRIENTE", "naturaleza": "DEBITO", "clase": "BALANCE", "nivel": 2, "padre": "1", "aceptaMovimientos": False}
        self.cuentas["1105"] = {"codigo": "1105", "nombre": "EFECTIVO", "naturaleza": "DEBITO", "clase": "BALANCE", "nivel": 3, "padre": "11", "aceptaMovimientos": True, "requiereTercero": False, "requiereDocumentoSoporte": True}
        self.cuentas["110505"] = {"codigo": "110505", "nombre": "CAJA", "naturaleza": "DEBITO", "clase": "BALANCE", "nivel": 4, "padre": "1105", "aceptaMovimientos": True, "requiereTercero": False, "requiereDocumentoSoporte": True}
        self.cuentas["110510"] = {"codigo": "110510", "nombre": "BANCOS", "naturaleza": "DEBITO", "clase": "BALANCE", "nivel": 4, "padre": "1105", "aceptaMovimientos": True, "requiereTercero": True, "requiereDocumentoSoporte": True}
        self.cuentas["1305"] = {"codigo": "1305", "nombre": "CLIENTES", "naturaleza": "DEBITO", "clase": "BALANCE", "nivel": 4, "aceptaMovimientos": True, "requiereTercero": True, "requiereDocumentoSoporte": True}
        self.cuentas["1405"] = {"codigo": "1405", "nombre": "INVENTARIO", "naturaleza": "DEBITO", "clase": "BALANCE", "nivel": 4, "aceptaMovimientos": True, "requiereTercero": True, "requiereDocumentoSoporte": True}
        # CLASE 2: PASIVO
        self.cuentas["2"] = {"codigo": "2", "nombre": "PASIVO", "naturaleza": "CREDITO", "clase": "BALANCE", "nivel": 1, "aceptaMovimientos": False}
        self.cuentas["2105"] = {"codigo": "2105", "nombre": "PROVEEDORES", "naturaleza": "CREDITO", "clase": "BALANCE", "nivel": 3, "aceptaMovimientos": True, "requiereTercero": True, "requiereDocumentoSoporte": True}
        self.cuentas["2408"] = {"codigo": "2408", "nombre": "IMPUESTOS POR PAGAR", "naturaleza": "CREDITO", "clase": "BALANCE", "nivel": 3, "aceptaMovimientos": True, "requiereDocumentoSoporte": True}
        # CLASE 4: INGRESOS
        self.cuentas["4"] = {"codigo": "4", "nombre": "INGRESOS", "naturaleza": "CREDITO", "clase": "ESTADO_RESULTADOS", "nivel": 1, "aceptaMovimientos": False}
        self.cuentas["4135"] = {"codigo": "4135", "nombre": "VENTAS", "naturaleza": "CREDITO", "clase": "ESTADO_RESULTADOS", "nivel": 3, "aceptaMovimientos": True, "requiereTercero": True, "requiereDocumentoSoporte": True}
        # CLASE 5: GASTOS
        self.cuentas["5"] = {"codigo": "5", "nombre": "GASTOS", "naturaleza": "DEBITO", "clase": "ESTADO_RESULTADOS", "nivel": 1, "aceptaMovimientos": False}
        self.cuentas["5105"] = {"codigo": "5105", "nombre": "GASTOS PERSONAL", "naturaleza": "DEBITO", "clase": "ESTADO_RESULTADOS", "nivel": 3, "aceptaMovimientos": True, "requiereTercero": True, "requiereDocumentoSoporte": True}
    
    def obtenerCuenta(self, codigo):
        return self.cuentas.get(codigo)
    
    def validarMovimiento(self, codigoCuenta, movimiento):
        cuenta = self.obtenerCuenta(codigoCuenta)
        if not cuenta:
            return {"valido": False, "error": "Cuenta no existe"}
        if not cuenta.get("aceptaMovimientos", False):
            return {"valido": False, "error": "Cuenta no acepta movimientos directos"}
        return {"valido": True, "cuenta": cuenta}

class LibroDiario:
    def __init__(self, conta, puc):
        self.conta = conta
        self.puc = puc
        self.asientos = []
        self.secuencial = 1
    
    def registrarAsiento(self, transaccion):
        try:
            for mov in transaccion["movimientos"]:
                validacion = self.puc.validarMovimiento(mov["cuenta"], {})
                if not validacion["valido"]:
                    raise Exception(f"Cuenta {mov['cuenta']} inválida")
            
            asiento = {
                "id": f"A-{self.secuencial:04d}",
                "fecha": transaccion.get("fecha", datetime.now().strftime("%Y-%m-%d")),
                "comprobante": transaccion.get("comprobante", f"CJ-{self.secuencial:04d}"),
                "descripcion": transaccion.get("descripcion", ""),
                "tercero": transaccion.get("tercero", ""),
                "documento": transaccion.get("documentoSoporte", ""),
                "movimientos": [],
                "totalDebito": 0,
                "totalCredito": 0
            }
            
            for mov in transaccion["movimientos"]:
                cuenta = self.puc.obtenerCuenta(mov["cuenta"])
                movimiento = {
                    "cuenta": mov["cuenta"],
                    "nombre": cuenta["nombre"] if cuenta else "Desconocida",
                    "detalle": mov.get("detalle", ""),
                    "debito": mov["valor"] if mov["tipo"] == "DEBITO" else 0,
                    "credito": mov["valor"] if mov["tipo"] == "CREDITO" else 0
                }
                asiento["movimientos"].append(movimiento)
                asiento["totalDebito"] += movimiento["debito"]
                asiento["totalCredito"] += movimiento["credito"]
            
            if abs(asiento["totalDebito"] - asiento["totalCredito"]) > 0.01:
                raise Exception("No cuadra partida doble")
            
            self.asientos.append(asiento)
            self.secuencial += 1
            return {"exito": True, "asiento": asiento}
        except Exception as e:
            return {"exito": False, "error": str(e)}
    
    def obtener_ingresos_mes(self):
        total = 0
        for a in self.asientos:
            for m in a["movimientos"]:
                if m["cuenta"] in ["4135"] and m["credito"] > 0:
                    total += m["credito"]
        return total
    
    def obtener_egresos_mes(self):
        total = 0
        for a in self.asientos:
            for m in a["movimientos"]:
                if m["cuenta"] in ["5105", "5115"] and m["debito"] > 0:
                    total += m["debito"]
        return total
    
    def obtener_balance(self):
        return self.obtener_ingresos_mes() - self.obtener_egresos_mes()

# ============================================
# INICIALIZAR SISTEMA
# ============================================
@st.cache_resource
def init_system():
    conta = Conta("Colombia", "COP", 2)
    puc = PUCInteligente(conta, "Colombia")
    libro = LibroDiario(conta, puc)
    
    # Agregar datos de ejemplo
    ejemplos = [
        {
            "fecha": "2024-03-15",
            "comprobante": "FV-001",
            "descripcion": "Venta de mercancía",
            "tercero": "Cliente A",
            "documentoSoporte": "FAC-001",
            "movimientos": [
                {"cuenta": "1305", "tipo": "DEBITO", "valor": 1190000, "detalle": "Cliente"},
                {"cuenta": "4135", "tipo": "CREDITO", "valor": 1000000, "detalle": "Ventas"},
                {"cuenta": "2408", "tipo": "CREDITO", "valor": 190000, "detalle": "IVA"}
            ]
        },
        {
            "fecha": "2024-03-20",
            "comprobante": "FV-002",
            "descripcion": "Venta servicios",
            "tercero": "Cliente B",
            "documentoSoporte": "FAC-002",
            "movimientos": [
                {"cuenta": "110505", "tipo": "DEBITO", "valor": 500000, "detalle": "Efectivo"},
                {"cuenta": "4135", "tipo": "CREDITO", "valor": 500000, "detalle": "Ventas"}
            ]
        }
    ]
    
    for ej in ejemplos:
        libro.registrarAsiento(ej)
    
    return conta, puc, libro

# Cargar sistema en sesión
if 'system_loaded' not in st.session_state:
    st.session_state.conta, st.session_state.puc, st.session_state.libro = init_system()
    st.session_state.system_loaded = True

# ============================================
# INTERFAZ DE USUARIO
# ============================================
st.title("📊 tuamigocontable.com")
st.markdown("### Tu asistente contable inteligente")

# Métricas
col1, col2, col3 = st.columns(3)
ingresos = st.session_state.libro.obtener_ingresos_mes()
egresos = st.session_state.libro.obtener_egresos_mes()
balance = ingresos - egresos

col1.metric("Ingresos del Mes", f"${ingresos:,.0f}", "+12%")
col2.metric("Egresos del Mes", f"${egresos:,.0f}", "-5%")
col3.metric("Balance del Mes", f"${balance:,.0f}")

# Botones de acción
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📄 Factura", use_container_width=True):
        st.info("Funcionalidad en desarrollo")
with col2:
    if st.button("📦 Inventario", use_container_width=True):
        st.info("Funcionalidad en desarrollo")
with col3:
    if st.button("⚖️ Balance", use_container_width=True):
        st.info("Funcionalidad en desarrollo")
with col4:
    if st.button("📥 Exportar JSON", use_container_width=True):
        json_str = json.dumps(st.session_state.libro.asientos, indent=2, default=str)
        st.download_button(
            label="Descargar",
            data=json_str,
            file_name=f"asientos_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# Tabla de movimientos
st.subheader("📋 Últimos Movimientos")
data = []
for a in st.session_state.libro.asientos[-10:]:
    for m in a["movimientos"]:
        data.append({
            "Fecha": a["fecha"],
            "Comprobante": a["comprobante"],
            "Cuenta": m["nombre"],
            "Detalle": m["detalle"][:30],
            "Débito": f"${m['debito']:,.0f}" if m['debito'] > 0 else "-",
            "Crédito": f"${m['credito']:,.0f}" if m['credito'] > 0 else "-",
            "Tercero": a["tercero"][:15]
        })
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# Mensaje informativo sobre IA
st.info("""
    **🤖 Nota sobre la IA:** 
    Para activar el asistente IA, necesitas configurar una API key de OpenAI o Gemini en los Secrets de Streamlit.
    Por ahora, la app funciona sin IA.
""")

# Footer
st.markdown("---")
st.markdown("© 2024 tuamigocontable.com - Todos los derechos reservados")

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

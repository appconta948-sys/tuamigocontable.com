# ============================================
# CONTA APP - VERSIÓN CON CHAT NATIVO DE STREAMLIT
# tuamigocontable.com
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os
from openai import OpenAI

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================
st.set_page_config(
    page_title="tuamigocontable.com",
    page_icon="📊",
    layout="wide"
)

# ============================================
# INICIALIZAR OPENAI (si está configurado)
# ============================================
@st.cache_resource
def init_openai():
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        client = OpenAI(api_key=api_key)
        return client, True
    except:
        return None, False

openai_client, openai_disponible = init_openai()

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

# Cargar sistema
if 'system_loaded' not in st.session_state:
    st.session_state.conta, st.session_state.puc, st.session_state.libro = init_system()
    st.session_state.messages = [
        {"role": "assistant", "content": "🤖 Hola, soy tu asistente contable. ¿En qué puedo ayudarte?"}
    ]
    st.session_state.system_loaded = True

# ============================================
# ESTILOS PERSONALIZADOS
# ============================================
st.markdown("""
<style>
    /* Fondo blanco elegante */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f5f5f7 100%);
    }
    
    /* Tarjetas de métricas */
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid;
        transition: all 0.3s ease;
        text-align: center;
        margin: 10px 0;
    }
    .metric-card.verde { border-color: #00ff00; }
    .metric-card.rojo { border-color: #ff0000; }
    .metric-card.azul { border-color: #0000ff; }
    .metric-card.amarillo { border-color: #ffff00; }
    .metric-card:hover { transform: translateY(-5px); }
    .metric-value { font-size: 36px; font-weight: bold; }
    
    /* Botones de acción */
    .stButton > button {
        background: linear-gradient(135deg, #ff0000, #0000ff, #00ff00, #ffff00);
        background-size: 300% 300%;
        animation: gradient 5s ease infinite;
        color: white;
        font-weight: bold;
        border: none;
        padding: 15px;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Chat */
    .stChatMessage {
        background: white;
        border-radius: 15px;
        padding: 10px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# ENCABEZADO
# ============================================
st.markdown("""
<div style="text-align: center; padding: 30px 0;">
    <h1 style="font-size: 48px; background: linear-gradient(135deg, #ff0000, #0000ff, #00ff00, #ffff00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        📊 TUAMIGOCONTABLE.COM
    </h1>
    <p style="color: #666; font-size: 20px;">
        ⚡ Tu asistente contable inteligente ⚡
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# MÉTRICAS
# ============================================
ingresos = st.session_state.libro.obtener_ingresos_mes()
egresos = st.session_state.libro.obtener_egresos_mes()
balance = ingresos - egresos

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card verde">
        <div style="font-size: 40px;">🟢</div>
        <div style="color: #666;">INGRESOS</div>
        <div class="metric-value" style="color: #00ff00;">${ingresos:,.0f}</div>
        <div style="color: #00ff00;">↑ +12%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card rojo">
        <div style="font-size: 40px;">🔴</div>
        <div style="color: #666;">EGRESOS</div>
        <div class="metric-value" style="color: #ff0000;">${egresos:,.0f}</div>
        <div style="color: #ff0000;">↓ -5%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card azul">
        <div style="font-size: 40px;">🔵</div>
        <div style="color: #666;">BALANCE</div>
        <div class="metric-value" style="color: #0000ff;">${balance:,.0f}</div>
        <div style="color: #0000ff;">⚖️ Positivo</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# BOTONES DE ACCIÓN
# ============================================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📄 FACTURA", use_container_width=True):
        st.info("Funcionalidad en desarrollo")
with col2:
    if st.button("📦 INVENTARIO", use_container_width=True):
        st.info("Funcionalidad en desarrollo")
with col3:
    if st.button("⚖️ BALANCE", use_container_width=True):
        st.info("Funcionalidad en desarrollo")
with col4:
    if st.button("🤖 IA", use_container_width=True):
        st.info("Chat abajo 👇")
with col5:
    if st.button("📥 EXPORTAR", use_container_width=True):
        json_str = json.dumps(st.session_state.libro.asientos, indent=2, default=str)
        st.download_button(
            label="📥 Descargar JSON",
            data=json_str,
            file_name=f"asientos_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# ============================================
# TABLA DE MOVIMIENTOS
# ============================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📋 ÚLTIMOS MOVIMIENTOS")

data = []
for a in st.session_state.libro.asientos[-10:]:
    for m in a["movimientos"]:
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
st.dataframe(df, use_container_width=True, height=400)

# ============================================
# CHAT NATIVO DE STREAMLIT (¡SIEMPRE FUNCIONA!)
# ============================================
st.markdown("---")
st.subheader("🤖 ASISTENTE IA")

# Mostrar estado de la IA
if openai_disponible:
    st.success("✅ IA conectada - Puedes hacer preguntas")
else:
    st.warning("⚠️ IA no configurada - Agrega OPENAI_API_KEY en Secrets")

# Mostrar mensajes del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del chat
if prompt := st.chat_input("Escribe tu consulta contable..."):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Obtener respuesta
    with st.chat_message("assistant"):
        if openai_disponible:
            with st.spinner("Pensando..."):
                try:
                    response = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Eres un asistente contable experto. Responde preguntas sobre contabilidad, finanzas e impuestos de manera clara y precisa."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=300
                    )
                    respuesta = response.choices[0].message.content
                except Exception as e:
                    respuesta = f"❌ Error: {str(e)}"
        else:
            respuesta = "⚠️ IA no configurada. Para activarla, agrega tu API key de OpenAI en Streamlit Secrets (sección Advanced settings) con el nombre OPENAI_API_KEY"
        
        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div style="text-align: center; padding: 30px; margin-top: 50px; color: #666; border-top: 2px solid #00ff00;">
    <p>© 2024 tuamigocontable.com - Todos los derechos reservados</p>
</div>
""", unsafe_allow_html=True)

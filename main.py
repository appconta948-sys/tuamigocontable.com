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
# CONFIGURACIÓN DE ESTILOS Y CHAT FLOTANTE
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
    .metric-value { font-size: 36px; font-weight: bold; }
    
    /* BOTÓN FLOTANTE DE IA - SIEMPRE VISIBLE */
    .ia-float-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #00ff00, #0000ff);
        border-radius: 50%;
        border: 3px solid #ffff00;
        box-shadow: 0 10px 30px rgba(0, 255, 0, 0.3);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 35px;
        transition: all 0.3s ease;
        z-index: 9999;
        color: white;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .ia-float-button:hover {
        transform: scale(1.1);
        box-shadow: 0 20px 40px rgba(0, 255, 0, 0.5);
    }
    
    /* VENTANA FLOTANTE DE IA */
    .ia-window {
        position: fixed;
        bottom: 120px;
        right: 30px;
        width: 350px;
        height: 500px;
        background: white;
        border: 3px solid #00ff00;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 255, 0, 0.2);
        display: none;
        z-index: 9998;
        overflow: hidden;
    }
    .ia-window.show {
        display: block !important;
    }
    .ia-header {
        background: linear-gradient(135deg, #00ff00, #0000ff);
        padding: 15px;
        color: white;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .ia-close {
        cursor: pointer;
        font-size: 24px;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: rgba(255,255,255,0.2);
    }
    .ia-close:hover {
        background: rgba(255,0,0,0.5);
    }
    .ia-content {
        padding: 20px;
        height: calc(100% - 60px);
        overflow-y: auto;
    }
    
    /* Botones de acción */
    .action-button {
        background: linear-gradient(135deg, #ff0000, #0000ff, #00ff00, #ffff00);
        background-size: 300% 300%;
        animation: gradient 5s ease infinite;
        color: white;
        padding: 15px 25px;
        border: none;
        border-radius: 15px;
        font-weight: bold;
        cursor: pointer;
        width: 100%;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        margin-top: 50px;
        color: #666;
        border-top: 2px solid #00ff00;
        background: white;
        border-radius: 15px;
    }
</style>

<!-- BOTÓN FLOTANTE -->
<div id="ia-button" class="ia-float-button" onclick="toggleIA()">
    🤖
</div>

<!-- VENTANA DE CHAT -->
<div id="ia-window" class="ia-window">
    <div class="ia-header">
        <span>🤖 ASISTENTE IA</span>
        <span class="ia-close" onclick="toggleIA()">✖</span>
    </div>
    <div class="ia-content">
        <div id="chat-messages" style="height: 300px; overflow-y: auto; margin-bottom: 20px; padding: 10px; background: #f5f5f5; border-radius: 10px;">
            <div style="color: #00ff00; margin-bottom: 10px;">
                🤖 IA: Hola, soy tu asistente contable. ¿En qué puedo ayudarte?
            </div>
        </div>
        <div style="display: flex; gap: 10px;">
            <input type="text" id="user-input" placeholder="Escribe tu consulta..." 
                   style="flex: 1; padding: 12px; border: 2px solid #00ff00; background: white; border-radius: 10px;">
            <button onclick="sendMessage()" style="background: #00ff00; color: white; border: none; padding: 12px 20px; border-radius: 10px; cursor: pointer;">➤</button>
        </div>
    </div>
</div>

<script>
// Función para abrir/cerrar el chat
function toggleIA() {
    var chatWindow = document.getElementById('ia-window');
    if (chatWindow.classList.contains('show')) {
        chatWindow.classList.remove('show');
    } else {
        chatWindow.classList.add('show');
    }
}

// Función para enviar mensajes
function sendMessage() {
    var input = document.getElementById('user-input');
    var message = input.value.trim();
    if (message === '') return;
    
    var chat = document.getElementById('chat-messages');
    
    // Agregar mensaje del usuario
    chat.innerHTML += '<div style="color: #0000ff; text-align: right; margin: 10px 0;">👤 Tú: ' + message + '</div>';
    
    // Simular respuesta
    setTimeout(function() {
        chat.innerHTML += '<div style="color: #00ff00; margin: 10px 0;">🤖 IA: Procesando consulta: "' + message + '".</div>';
        chat.scrollTop = chat.scrollHeight;
    }, 1000);
    
    input.value = '';
    chat.scrollTop = chat.scrollHeight;
}

// Abrir chat con el botón del menú
function openIAFromMenu() {
    document.getElementById('ia-window').classList.add('show');
}
</script>
""", unsafe_allow_html=True)
with col4:
    if st.button("🤖 IA", use_container_width=True):
        st.markdown("<script>openIAFromMenu();</script>", unsafe_allow_html=True)

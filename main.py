import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# ============================================
# CONFIGURACIÓN Y ESTILOS
# ============================================
st.set_page_config(
    page_title="Conta - Tu Amigo Contable",
    page_icon="🧔",
    layout="wide"
)

COLORES = {
    "primario": "#345470",
    "fondo": "#e1e8ee",
    "verde": "#92c83e",
    "rojo": "#d9534f",
    "blanco": "#ffffff"
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    * {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background-color: {COLORES['fondo']}; }}
    
    .main-header {{
        background: linear-gradient(135deg, {COLORES['primario']} 0%, #1e3a5f 100%);
        padding: 2rem;
        border-radius: 0 0 30px 30px;
        margin-bottom: 2rem;
        text-align: center;
    }}
    .main-header .big-logo {{
        color: {COLORES['verde']};
        font-size: 2.5rem;
        font-weight: 800;
    }}
    .main-header .tagline {{
        color: white;
        font-size: 1.1rem;
    }}
    
    .card {{
        background: {COLORES['blanco']};
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1rem;
    }}
    .card .valor {{
        font-size: 2rem;
        font-weight: 700;
    }}
    
    .section-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {COLORES['primario']};
        margin: 2rem 0 1rem 0;
        border-left: 5px solid {COLORES['verde']};
        padding-left: 1rem;
    }}
    
    .conta-card {{
        background: linear-gradient(135deg, {COLORES['primario']} 0%, #1e3a5f 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin-bottom: 1rem;
    }}
    
    .chat-user {{
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 0.5rem;
        text-align: right;
    }}
    .chat-conta {{
        background: #f0f7e8;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 0.5rem;
        border-left: 4px solid {COLORES['verde']};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# DICCIONARIO DE TRADUCCIÓN
# ============================================
DICCIONARIO = {
    "me fiaron": {"cuenta": "2101", "nombre": "PROVEEDORES", "tipo": "CREDITO", "accion": "Aumenta Pasivo"},
    "me debe": {"cuenta": "1205", "nombre": "CUENTAS POR COBRAR", "tipo": "DEBITO", "accion": "Aumenta Activo"},
    "agarré de la caja": {"cuenta": "3105", "nombre": "RETIROS PERSONAL", "tipo": "DEBITO", "accion": "Aumenta Retiro"},
    "soltó los que debía": {"cuenta": "1101", "nombre": "CAJA", "tipo": "DEBITO", "accion": "Entra Cash"},
    "pagó el de la luz": {"cuenta": "6201", "nombre": "GASTO ELECTRICIDAD", "tipo": "DEBITO", "accion": "Aumenta Gasto"},
    "vendí": {"cuenta": "4135", "nombre": "VENTAS", "tipo": "CREDITO", "accion": "Aumenta Ingreso"},
    "compré": {"cuenta": "1405", "nombre": "INVENTARIO", "tipo": "DEBITO", "accion": "Aumenta Activo"}
}

# ============================================
# CLASE LIBRO DIARIO
# ============================================
class LibroDiario:
    def __init__(self, usuario_id="el_lento"):
        self.usuario_id = usuario_id
        self.asientos = []
        self.cargar_datos()
    
    def cargar_datos(self):
        archivo = f"asientos_{self.usuario_id}.json"
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r') as f:
                    data = json.load(f)
                    self.asientos = data.get('asientos', [])
            except:
                self.asientos = []
    
    def guardar_datos(self):
        archivo = f"asientos_{self.usuario_id}.json"
        with open(archivo, 'w') as f:
            json.dump({'asientos': self.asientos}, f)
    
    def registrar(self, descripcion, tercero, movimientos):
        asiento = {
            "id": len(self.asientos) + 1,
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "descripcion": descripcion,
            "tercero": tercero,
            "movimientos": movimientos,
            "total_debito": sum(m["valor"] for m in movimientos if m["tipo"] == "DEBITO"),
            "total_credito": sum(m["valor"] for m in movimientos if m["tipo"] == "CREDITO")
        }
        self.asientos.append(asiento)
        self.guardar_datos()
        return asiento
    
    def obtener_ingresos(self):
        total = 0
        for a in self.asientos:
            for m in a["movimientos"]:
                if m["tipo"] == "CREDITO" and "VENTAS" in m.get("cuenta_nombre", ""):
                    total += m["valor"]
        return total
    
    def obtener_gastos(self):
        total = 0
        for a in self.asientos:
            for m in a["movimientos"]:
                if m["tipo"] == "DEBITO" and "GASTO" in m.get("cuenta_nombre", ""):
                    total += m["valor"]
        return total
    
    def obtener_balance(self):
        return self.obtener_ingresos() - self.obtener_gastos()
    
    def obtener_movimientos(self, n=10):
        return self.asientos[-n:][::-1]

# ============================================
# FUNCIONES
# ============================================
def traducir(texto):
    texto_lower = texto.lower()
    for clave, info in DICCIONARIO.items():
        if clave in texto_lower:
            return info
    return None

def registrar_con_ia(mensaje, libro):
    info = traducir(mensaje)
    if info:
        import re
        numeros = re.findall(r'\d+', mensaje)
        valor = int(numeros[0]) if numeros else 10000
        
        movimientos = [
            {"cuenta": info["cuenta"], "tipo": info["tipo"], "valor": valor, "cuenta_nombre": info["nombre"], "detalle": mensaje}
        ]
        
        resultado = libro.registrar(mensaje, "cliente", movimientos)
        return resultado, info
    return None, None

# ============================================
# INICIALIZACIÓN
# ============================================
if "libro" not in st.session_state:
    st.session_state.libro = LibroDiario("el_lento")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ============================================
# LOGIN
# ============================================
if not st.session_state.logged_in:
    st.markdown("""
    <div style='text-align: center; padding: 3rem;'>
        <h1 style='color: #345470;'>🧔 Conta</h1>
        <p style='font-size: 1.2rem;'>"Traduciendo el lenguaje del barrio a balances millonarios."</p>
        <p>20 años cuadrando cajas en Latam</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🔴 Empezar a cuadrar", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# ============================================
# APP PRINCIPAL
# ============================================
st.markdown("""
<div class='main-header'>
    <div class='big-logo'>🧔 tuamigocontable.com</div>
    <div class='tagline'>"Traduciendo el lenguaje del barrio a balances millonarios."</div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🧔 Conta")
    st.markdown("*20 años cuadrando cajas en Latam*")
    st.markdown("---")
    
    menu = st.radio("📊 Menú", ["🏠 Dashboard", "💬 Hablar con Conta", "📖 Diccionario"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"**👤 El lento:** el_lento")
    
    if st.button("🚪 Salir", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ============================================
# DASHBOARD
# ============================================
if menu == "🏠 Dashboard":
    ingresos = st.session_state.libro.obtener_ingresos()
    gastos = st.session_state.libro.obtener_gastos()
    balance = ingresos - gastos
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='card'>
            <h3>💰 INGRESOS</h3>
            <div class='valor'>${ingresos:,.0f}</div>
            <div style='color: green;'>Lo que ha entrado</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='card'>
            <h3>💸 GASTOS</h3>
            <div class='valor'>${gastos:,.0f}</div>
            <div style='color: red;'>Lo que ha salido</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        color = "green" if balance >= 0 else "red"
        st.markdown(f"""
        <div class='card'>
            <h3>⚖️ BALANCE</h3>
            <div class='valor'>${balance:,.0f}</div>
            <div style='color: {color};'>{'Ganancia' if balance >= 0 else 'Pérdida'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-title'>📋 Últimos Movimientos</div>", unsafe_allow_html=True)
    movimientos = st.session_state.libro.obtener_movimientos()
    if movimientos:
        data = []
        for m in movimientos:
            for mov in m["movimientos"]:
                data.append({
                    "Fecha": m["fecha"],
                    "Descripción": m["descripcion"],
                    "Cuenta": mov.get("cuenta_nombre", mov.get("cuenta", "")),
                    "Monto": f"${mov['valor']:,.0f}",
                    "Tipo": mov["tipo"]
                })
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    else:
        st.info("📝 Aún no hay movimientos. Dile a Conta: 'Vendí algo' o 'Compré mercancía'")

# ============================================
# HABLAR CON CONTA
# ============================================
elif menu == "💬 Hablar con Conta":
    st.markdown("<div class='section-title'>💬 Habla con Conta</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='conta-card'>
        🧔 <strong>Conta:</strong><br>
        "Cuéntame cómo va la movida. Si te fiaron, si te deben, si agarraste de la caja... 
        Yo traduzco eso a números."
    </div>
    """, unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'><strong>El lento:</strong> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-conta'>{msg['content']}</div>", unsafe_allow_html=True)
    
    mensaje = st.text_input("Dile algo a Conta:", placeholder="Ej: 'Me fiaron 4 leches' o 'Vendí un pan en $10,000'")
    
    if st.button("Enviar", use_container_width=True):
        if mensaje:
            st.session_state.chat_history.append({"role": "user", "content": mensaje})
            
            resultado, info = registrar_con_ia(mensaje, st.session_state.libro)
            if resultado:
                respuesta = f"🧔 **Conta:** 'Listo, ya quedó anotado. {mensaje} por ${resultado['total_debito']:,.0f}. Sigue así, que el negocio va tomando forma.'"
            else:
                respuesta = f"🧔 **Conta:** 'Anótalo bien, que después no digas que no te avisé. {mensaje}... ¿cuánto fue?'"
            
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
            st.rerun()
    
    st.markdown("### 📌 Pregúntale a Conta:")
    cols = st.columns(4)
    sugerencias = ["Me fiaron 4 leches", "Me debe un pan", "Agarré $10 de la caja", "Vendí un pan en $10,000"]
    for i, sug in enumerate(sugerencias):
        with cols[i]:
            if st.button(sug, use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": sug})
                resultado, info = registrar_con_ia(sug, st.session_state.libro)
                if resultado:
                    respuesta = f"🧔 **Conta:** 'Listo, quedó anotado {sug} por ${resultado['total_debito']:,.0f}'"
                else:
                    respuesta = f"🧔 **Conta:** '¿Cuánto fue?'"
                st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
                st.rerun()

# ============================================
# DICCIONARIO
# ============================================
elif menu == "📖 Diccionario":
    st.markdown("<div class='section-title'>📖 Diccionario Callejero → Contabilidad</div>", unsafe_allow_html=True)
    
    df = pd.DataFrame([
        {"Lenguaje de Barrio": "Me fiaron 4 leches", "Conta entiende": "PROVEEDORES (2101)", "Acción": "Aumenta Pasivo"},
        {"Lenguaje de Barrio": "Me debe un pan", "Conta entiende": "CUENTAS POR COBRAR (1205)", "Acción": "Aumenta Activo"},
        {"Lenguaje de Barrio": "Agarré $10 de la caja", "Conta entiende": "RETIROS PERSONAL (3105)", "Acción": "Aumenta Retiro"},
        {"Lenguaje de Barrio": "Vendí un pan", "Conta entiende": "VENTAS (4135)", "Acción": "Aumenta Ingreso"}
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.info("📌 **Regla de Oro:** 'No importa si fue un peso o un millón, si se mueve, se anota.'")

# ============================================
# BOTÓN FLOTANTE
# ============================================
st.markdown(f"""
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
    <button onclick="window.location.href='#hablar-con-conta'" 
        style="width: 60px; height: 60px; border-radius: 50%; 
               background: {COLORES['verde']};
               color: white; border: none; font-size: 30px; cursor: pointer;">
        💬
    </button>
</div>
""", unsafe_allow_html=True)
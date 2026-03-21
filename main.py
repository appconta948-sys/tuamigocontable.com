import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from openai import OpenAI
import plotly.graph_objects as go
import plotly.express as px

# ============================================
# CONFIGURACIÓN Y ESTILOS
# ============================================
st.set_page_config(
    page_title="Conta - Tu Amigo Contable",
    page_icon="🧔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colores de tu imagen
COLORES = {
    "primario": "#345470",
    "fondo": "#e1e8ee", 
    "texto": "#1a1a1a",
    "verde": "#92c83e",
    "rojo": "#d9534f",
    "blanco": "#ffffff",
    "amarillo": "#f0ad4e"
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
    .main-header .small-logo {{ color: {COLORES['verde']}; font-size: 1rem; letter-spacing: 2px; }}
    .main-header .big-logo {{ color: {COLORES['verde']}; font-size: 3rem; font-weight: 800; }}
    .main-header .tagline {{ color: white; font-size: 1.2rem; }}
    
    .card {{
        background: {COLORES['blanco']};
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.3s;
        margin-bottom: 1rem;
    }}
    .card:hover {{ transform: translateY(-5px); }}
    .card h3 {{ color: {COLORES['primario']}; font-size: 1.1rem; margin-bottom: 1rem; }}
    .card .valor {{ font-size: 2rem; font-weight: 700; color: {COLORES['texto']}; }}
    
    .section-title {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {COLORES['primario']};
        margin: 2rem 0 1.5rem 0;
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
    
    .chat-message-user {{
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 0.5rem;
        text-align: right;
    }}
    .chat-message-conta {{
        background: #f0f7e8;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 0.5rem;
        border-left: 4px solid {COLORES['verde']};
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {COLORES['primario']} 0%, #1e3a5f 100%);
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# DICCIONARIO DE TRADUCCIÓN (lenguaje callejero → contabilidad)
# ============================================
DICCIONARIO = {
    "me fiaron": {"cuenta": "2101", "nombre": "PROVEEDORES", "tipo": "CREDITO", "accion": "Aumenta Pasivo"},
    "me debe": {"cuenta": "1205", "nombre": "CUENTAS POR COBRAR", "tipo": "DEBITO", "accion": "Aumenta Activo"},
    "agarré de la caja": {"cuenta": "3105", "nombre": "RETIROS PERSONAL", "tipo": "DEBITO", "accion": "Aumenta Retiro"},
    "soltó los que debía": {"cuenta": "1101", "nombre": "CAJA", "tipo": "DEBITO", "accion": "Entra Cash, Baja Deuda"},
    "pagó el de la luz": {"cuenta": "6201", "nombre": "GASTO ELECTRICIDAD", "tipo": "DEBITO", "accion": "Aumenta Gasto"},
    "me bajaron por feo": {"cuenta": "4105", "nombre": "DESCUENTO EN VENTAS", "tipo": "DEBITO", "accion": "Resta al Ingreso"},
    "vendí": {"cuenta": "4135", "nombre": "VENTAS", "tipo": "CREDITO", "accion": "Aumenta Ingreso"},
    "compré": {"cuenta": "1405", "nombre": "INVENTARIO", "tipo": "DEBITO", "accion": "Aumenta Activo"},
    "le pagué al proveedor": {"cuenta": "2101", "nombre": "PROVEEDORES", "tipo": "DEBITO", "accion": "Disminuye Pasivo"}
}

# ============================================
# CONFIGURACIÓN DE IA (OPENAI)
# ============================================
def configurar_openai():
    try:
        api_key = None
        if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
        else:
            api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Error configurando OpenAI: {e}")
    return None

# ============================================
# CLASE CONTA (Contador con 20 años de experiencia)
# ============================================
class Conta:
    def __init__(self):
        self.nombre = "Conta"
        self.experiencia = "20 años cuadrando cajas en Latam"
        self.mision = "Que 'el lento' no quiebre por no anotar los 'mandados'"
        self.especialidad = "Contabilidad de Calle (Street Accounting)"
    
    def traducir(self, texto):
        """Traduce lenguaje callejero a términos contables"""
        texto_lower = texto.lower()
        for clave, valor in DICCIONARIO.items():
            if clave in texto_lower:
                return valor
        return None
    
    def hablar(self, mensaje):
        """Responde como Conta, el contador de barrio"""
        return f"🧔 **Conta (20 años de experiencia):** {mensaje}"

# ============================================
# CLASE CATALOGO DE CUENTAS (PUC)
# ============================================
class CatalogoCuentas:
    def __init__(self):
        self.cuentas = {
            # ACTIVOS (Débito +)
            "1101": {"codigo": "1101", "nombre": "CAJA GENERAL", "naturaleza": "DEBITO", "clase": "ACTIVO"},
            "1102": {"codigo": "1102", "nombre": "BANCOS", "naturaleza": "DEBITO", "clase": "ACTIVO"},
            "1201": {"codigo": "1201", "nombre": "INVENTARIO", "naturaleza": "DEBITO", "clase": "ACTIVO"},
            "1205": {"codigo": "1205", "nombre": "CUENTAS POR COBRAR", "naturaleza": "DEBITO", "clase": "ACTIVO"},
            "1301": {"codigo": "1301", "nombre": "EQUIPO DE OFICINA", "naturaleza": "DEBITO", "clase": "ACTIVO"},
            # PASIVOS (Crédito +)
            "2101": {"codigo": "2101", "nombre": "PROVEEDORES", "naturaleza": "CREDITO", "clase": "PASIVO"},
            "2105": {"codigo": "2105", "nombre": "ITBMS POR PAGAR", "naturaleza": "CREDITO", "clase": "PASIVO"},
            "2201": {"codigo": "2201", "nombre": "PRÉSTAMOS BANCARIOS", "naturaleza": "CREDITO", "clase": "PASIVO"},
            # PATRIMONIO (Crédito +)
            "3101": {"codigo": "3101", "nombre": "CAPITAL SOCIAL", "naturaleza": "CREDITO", "clase": "PATRIMONIO"},
            "3105": {"codigo": "3105", "nombre": "RETIROS PERSONAL", "naturaleza": "DEBITO", "clase": "PATRIMONIO"},
            "3701": {"codigo": "3701", "nombre": "UTILIDADES RETENIDAS", "naturaleza": "CREDITO", "clase": "PATRIMONIO"},
            # INGRESOS (Crédito +)
            "4135": {"codigo": "4135", "nombre": "VENTAS", "naturaleza": "CREDITO", "clase": "INGRESO"},
            "4105": {"codigo": "4105", "nombre": "DESCUENTOS EN VENTAS", "naturaleza": "DEBITO", "clase": "INGRESO"},
            # GASTOS (Débito +)
            "5105": {"codigo": "5105", "nombre": "GASTOS OPERACIONALES", "naturaleza": "DEBITO", "clase": "GASTO"},
            "6201": {"codigo": "6201", "nombre": "GASTOS SERVICIOS", "naturaleza": "DEBITO", "clase": "GASTO"}
        }
    
    def obtener_cuenta(self, codigo):
        return self.cuentas.get(codigo)
    
    def listar_activos(self):
        return [c for c in self.cuentas.values() if c["clase"] == "ACTIVO"]
    
    def listar_pasivos(self):
        return [c for c in self.cuentas.values() if c["clase"] == "PASIVO"]
    
    def listar_patrimonio(self):
        return [c for c in self.cuentas.values() if c["clase"] == "PATRIMONIO"]
    
    def listar_ingresos(self):
        return [c for c in self.cuentas.values() if c["clase"] == "INGRESO"]
    
    def listar_gastos(self):
        return [c for c in self.cuentas.values() if c["clase"] == "GASTO"]

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
    
    def obtener_ingresos(self, periodo="mes"):
        hoy = datetime.now()
        if periodo == "mes":
            fecha_inicio = hoy.replace(day=1)
        else:
            fecha_inicio = hoy - timedelta(days=30)
        
        total = 0
        for a in self.asientos:
            fecha_a = datetime.strptime(a["fecha"], "%Y-%m-%d")
            if fecha_a >= fecha_inicio:
                for m in a["movimientos"]:
                    if m["tipo"] == "CREDITO" and "VENTAS" in m.get("cuenta_nombre", ""):
                        total += m["valor"]
        return total
    
    def obtener_gastos(self, periodo="mes"):
        hoy = datetime.now()
        if periodo == "mes":
            fecha_inicio = hoy.replace(day=1)
        else:
            fecha_inicio = hoy - timedelta(days=30)
        
        total = 0
        for a in self.asientos:
            fecha_a = datetime.strptime(a["fecha"], "%Y-%m-%d")
            if fecha_a >= fecha_inicio:
                for m in a["movimientos"]:
                    if m["tipo"] == "DEBITO" and "GASTO" in m.get("cuenta_nombre", ""):
                        total += m["valor"]
        return total
    
    def obtener_balance(self):
        return self.obtener_ingresos() - self.obtener_gastos()
    
    def obtener_movimientos_recientes(self, n=10):
        return self.asientos[-n:][::-1]
    
    def obtener_estadisticas(self):
        meses = []
        ingresos_mensuales = []
        gastos_mensuales = []
        
        for i in range(6):
            fecha = datetime.now().replace(day=1) - timedelta(days=30*i)
            mes_nombre = fecha.strftime("%B")
            meses.insert(0, mes_nombre[:3])
            
            inicio = fecha.replace(day=1)
            fin = (inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            ing = 0
            gas = 0
            for a in self.asientos:
                fecha_a = datetime.strptime(a["fecha"], "%Y-%m-%d")
                if inicio <= fecha_a <= fin:
                    for m in a["movimientos"]:
                        if m["tipo"] == "CREDITO" and "VENTAS" in m.get("cuenta_nombre", ""):
                            ing += m["valor"]
                        if m["tipo"] == "DEBITO" and "GASTO" in m.get("cuenta_nombre", ""):
                            gas += m["valor"]
            ingresos_mensuales.insert(0, ing)
            gastos_mensuales.insert(0, gas)
        
        return {"meses": meses, "ingresos": ingresos_mensuales, "gastos": gastos_mensuales}

# ============================================
# ASISTENTE CONTA (IA)
# ============================================
class AsistenteConta:
    def __init__(self, openai_client, libro, catalogo):
        self.client = openai_client
        self.libro = libro
        self.catalogo = catalogo
        self.conta = Conta()
    
    def interpretar(self, mensaje):
        """Interpreta lenguaje callejero y devuelve transacción"""
        if not self.client:
            return self.interpretar_sin_ia(mensaje)
        
        # Diccionario de cuentas para la IA
        cuentas_str = ", ".join([f"{c['codigo']}:{c['nombre']}" for c in self.catalogo.cuentas.values()])
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"""Eres "Conta", un contador con 20 años de experiencia en Latinoamérica.
                    
                    Traduces lenguaje callejero a contabilidad formal.
                    
                    Diccionario de traducción:
                    - "me fiaron" → PROVEEDORES (2101) CREDITO
                    - "me debe" → CUENTAS POR COBRAR (1205) DEBITO  
                    - "agarré de la caja" → RETIROS PERSONAL (3105) DEBITO
                    - "soltó los que debía" → CAJA (1101) DEBITO
                    - "vendí" → VENTAS (4135) CREDITO
                    - "compré" → INVENTARIO (1405) DEBITO
                    
                    Cuentas disponibles: {cuentas_str}
                    
                    Devuelve SOLO JSON con:
                    {{
                        "descripcion": "descripción clara",
                        "tercero": "nombre del cliente/proveedor",
                        "movimientos": [
                            {{"cuenta": "codigo", "tipo": "DEBITO/CREDITO", "valor": número, "detalle": "detalle"}}
                        ]
                    }}
                    """},
                    {"role": "user", "content": mensaje}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            import re
            text = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            st.error(f"Error IA: {e}")
        
        return self.interpretar_sin_ia(mensaje)
    
    def interpretar_sin_ia(self, mensaje):
        """Interpretación básica sin IA usando el diccionario"""
        mensaje_lower = mensaje.lower()
        
        for palabra, info in DICCIONARIO.items():
            if palabra in mensaje_lower:
                # Buscar números
                import re
                numeros = re.findall(r'\d+', mensaje)
                valor = int(numeros[0]) if numeros else 0
                
                return {
                    "descripcion": mensaje,
                    "tercero": "cliente" if "vendí" in mensaje else "proveedor",
                    "movimientos": [
                        {"cuenta": info["cuenta"], "tipo": info["tipo"], "valor": valor, "detalle": mensaje}
                    ]
                }
        return None
    
    def hablar(self, mensaje):
        """Conta responde como el contador de barrio"""
        if not self.client:
            return f"🧔 **Conta:** {self.conta.hablar('Cuéntame más, ¿cuánto fue y a quién?')}"
        
        ingresos = self.libro.obtener_ingresos()
        gastos = self.libro.obtener_gastos()
        balance = ingresos - gastos
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"""Eres "Conta", un contador con 20 años de experiencia en Latinoamérica.
                    
                    Personalidad:
                    - Hablas como un contador de barrio, con confianza y sabiduría
                    - Usas términos como "el lento" (cliente), "mandados" (transacciones)
                    - Das consejos prácticos y honestos
                    
                    Datos del negocio:
                    - Ingresos: ${ingresos:,.0f}
                    - Gastos: ${gastos:,.0f}
                    - Balance: ${balance:,.0f}
                    
                    Responde de forma cálida y práctica."""},
                    {"role": "user", "content": mensaje}
                ],
                temperature=0.7,
                max_tokens=250
            )
            return f"🧔 **Conta:** {response.choices[0].message.content}"
        except:
            return f"🧔 **Conta:** {self.conta.hablar('Anótalo bien, que después no digas que no te avisé.')}"

# ============================================
# FUNCIONES DEL DASHBOARD
# ============================================
def mostrar_dashboard(libro, catalogo):
    ingresos = libro.obtener_ingresos()
    gastos = libro.obtener_gastos()
    balance = ingresos - gastos
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='card'>
            <h3>💰 INGRESOS</h3>
            <div class='valor'>${ingresos:,.0f}</div>
            <div style='color: {COLORES["verde"]};'>Lo que ha entrado</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='card'>
            <h3>💸 GASTOS</h3>
            <div class='valor'>${gastos:,.0f}</div>
            <div style='color: {COLORES["rojo"]};'>Lo que ha salido</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        color = COLORES["verde"] if balance >= 0 else COLORES["rojo"]
        st.markdown(f"""
        <div class='card'>
            <h3>⚖️ BALANCE</h3>
            <div class='valor'>${balance:,.0f}</div>
            <div style='color: {color};'>{'Ganancia' if balance >= 0 else 'Pérdida'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico
    stats = libro.obtener_estadisticas()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=stats["meses"], y=stats["ingresos"], name="Ingresos", marker_color=COLORES["verde"]))
    fig.add_trace(go.Bar(x=stats["meses"], y=stats["gastos"], name="Gastos", marker_color=COLORES["rojo"]))
    fig.update_layout(
        title="Evolución de Ingresos vs Gastos",
        plot_bgcolor='white',
        paper_bgcolor='white',
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de movimientos
    st.markdown("<div class='section-title'>📋 Últimos Movimientos</div>", unsafe_allow_html=True)
    movimientos = libro.obtener_movimientos_recientes(10)
    if movimientos:
        data = []
        for m in movimientos:
            for mov in m["movimientos"]:
                data.append({
                    "Fecha": m["fecha"],
                    "Descripción": m["descripcion"],
                    "Tercero": m["tercero"],
                    "Cuenta": mov.get("cuenta_nombre", mov.get("cuenta", "")),
                    "Débito": f"${mov['valor']:,.0f}" if mov["tipo"] == "DEBITO" else "-",
                    "Crédito": f"${mov['valor']:,.0f}" if mov["tipo"] == "CREDITO" else "-"
                })
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    else:
        st.info("📝 Aún no hay movimientos. Dile a Conta: 'Vendí algo' o 'Compré mercancía'")

def mostrar_catalogo(catalogo):
    st.markdown("<div class='section-title'>📚 Catálogo de Cuentas (PUC)</div>", unsafe_allow_html=True)
    
    tabs = st.tabs(["🏦 ACTIVOS", "💳 PASIVOS", "👥 PATRIMONIO", "💰 INGRESOS", "📉 GASTOS"])
    
    with tabs[0]:
        df = pd.DataFrame(catalogo.listar_activos())
        st.dataframe(df, use_container_width=True, hide_index=True)
    with tabs[1]:
        df = pd.DataFrame(catalogo.listar_pasivos())
        st.dataframe(df, use_container_width=True, hide_index=True)
    with tabs[2]:
        df = pd.DataFrame(catalogo.listar_patrimonio())
        st.dataframe(df, use_container_width=True, hide_index=True)
    with tabs[3]:
        df = pd.DataFrame(catalogo.listar_ingresos())
        st.dataframe(df, use_container_width=True, hide_index=True)
    with tabs[4]:
        df = pd.DataFrame(catalogo.listar_gastos())
        st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================
# INICIALIZACIÓN
# ============================================
def inicializar():
    if "usuario_id" not in st.session_state:
        st.session_state.usuario_id = "el_lento"
    if "catalogo" not in st.session_state:
        st.session_state.catalogo = CatalogoCuentas()
    if "libro" not in st.session_state:
        st.session_state.libro = LibroDiario(st.session_state.usuario_id)
    if "openai_client" not in st.session_state:
        st.session_state.openai_client = configurar_openai()
    if "asistente" not in st.session_state:
        st.session_state.asistente = AsistenteConta(
            st.session_state.openai_client,
            st.session_state.libro,
            st.session_state.catalogo
        )
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

inicializar()

# ============================================
# LOGIN
# ============================================
if not st.session_state.logged_in:
    st.markdown("""
    <div style='text-align: center; padding: 3rem;'>
        <h1 style='color: #345470;'>🧔 Conta</h1>
        <p style='font-size: 1.2rem; color: #666;'>"Traduciendo el lenguaje del barrio a balances millonarios."</p>
        <p style='font-size: 1rem; color: #888;'>20 años cuadrando cajas en Latam</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🔴 Empezar a cuadrar", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# ============================================
# APLICACIÓN PRINCIPAL
# ============================================
st.markdown("""
<div class='main-header'>
    <div class='small-logo'>igocontable.com</div>
    <div class='big-logo'>tuamigocontable.com</div>
    <div class='tagline'>"Traduciendo el lenguaje del barrio a balances millonarios."</div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🧔 Conta")
    st.markdown("*20 años cuadrando cajas en Latam*")
    st.markdown("---")
    
    menu = st.radio(
        "📊 Navegación",
        ["🏠 Dashboard", "📚 Catálogo de Cuentas", "💬 Hablar con Conta", "✍️ Registrar Manual", "📖 Diccionario"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    
    if st.session_state.openai_client:
        st.success("✅ Conta conectado")
    else:
        st.warning("⚠️ Conta en modo básico")
    
    st.markdown(f"**👤 El lento:** {st.session_state.usuario_id}")
    
    if st.button("🚪 Salir", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ============================================
# DASHBOARD
# ============================================
if menu == "🏠 Dashboard":
    mostrar_dashboard(st.session_state.libro, st.session_state.catalogo)

# ============================================
# CATÁLOGO DE CUENTAS
# ============================================
elif menu == "📚 Catálogo de Cuentas":
    mostrar_catalogo(st.session_state.catalogo)

# ============================================
# HABLAR CON CONTA
# ============================================
elif menu == "💬 Hablar con Conta":
    st.markdown("<div class='section-title'>💬 Habla con Conta</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='conta-card'>
        🧔 <strong>Conta (20 años de experiencia):</strong><br>
        "Cuéntame cómo va la movida. Si te fiaron, si te deben, si agarraste de la caja... 
        Yo traduzco eso a números que no duelen."
    </div>
    """, unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-message-user'><strong>El lento:</strong> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-message-conta'>{msg['content']}</div>", unsafe_allow_html=True)
    
    mensaje = st.text_input("Dile algo a Conta:", placeholder="Ej: 'Me fiaron 4 leches' o 'Vendí un pan en $10,000'")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("Enviar", use_container_width=True):
            if mensaje:
                st.session_state.chat_history.append({"role": "user", "content": mensaje})
                
                with st.spinner("Conta está revisando sus libros..."):
                    # Verificar si es una transacción
                    transaccion = st.session_state.asistente.interpretar(mensaje)
                    if transaccion and transaccion.get("movimientos"):
                        resultado = st.session_state.libro.registrar(
                            descripcion=transaccion.get("descripcion", mensaje),
                            tercero=transaccion.get("tercero", ""),
                            movimientos=transaccion["movimientos"]
                        )
                        if resultado:
                            respuesta = f"🧔 **Conta:** 'Listo, ya quedó anotado. {mensaje} por ${sum(m['valor'] for m in transaccion['movimientos']):,.0f}. Sigue así, que el negocio va tomando forma.'"
                        else:
                            respuesta = f"🧔 **Conta:** 'Algo no cuadra. ¿Me explicas mejor cuánto fue y a quién?'"
                    else:
                        respuesta = st.session_state.asistente.hablar(mensaje)
                    
                    st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
                    st.rerun()
    
    with col2:
        if st.button("Limpiar", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Sugerencias
    st.markdown("### 📌 Pregúntale a Conta:")
    cols = st.columns(4)
    sugerencias = ["Me fiaron 4 leches", "Me debe un pan", "Agarré $10 de la caja", "Soltó los $20 que debía"]
    for i, sug in enumerate(sugerencias):
        with cols[i]:
            if st.button(sug, use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": sug})
                transaccion = st.session_state.asistente.interpretar(sug)
                if transaccion and transaccion.get("movimientos"):
                    resultado = st.session_state.libro.registrar(
                        descripcion=transaccion.get("descripcion", sug),
                        tercero=transaccion.get("tercero", ""),
                        movimientos=transaccion["movimientos"]
                    )
                respuesta = st.session_state.asistente.hablar(sug)
                st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
                st.rerun()

# ============================================
# REGISTRAR MANUAL
# ============================================
elif menu == "✍️ Registrar Manual":
    st.markdown("<div class='section-title'>✍️ Registrar Manual</div>", unsafe_allow_html=True)
    
    with st.form("registro_manual"):
        col1, col2 = st.columns(2)
        with col1:
            descripcion = st.text_input("Descripción", placeholder="Ej: Venta de producto")
            tercero = st.text_input("Cliente/Proveedor")
            fecha = st.date_input("Fecha", datetime.now())
        with col2:
            tipo = st.selectbox("Tipo", ["Ingreso (Venta)", "Gasto"])
            cuenta = st.selectbox("Cuenta", [
                "1101 - CAJA GENERAL",
                "1102 - BANCOS",
                "1205 - CUENTAS POR COBRAR",
                "2101 - PROVEEDORES",
                "4135 - VENTAS",
                "5105 - GASTOS OPERACIONALES"
            ])
            monto = st.number_input("Monto", min_value=0.0, step=10000.0)
        
        submit = st.form_submit_button("Registrar", use_container_width=True)
        
        if submit and monto > 0:
            codigo = cuenta.split(" - ")[0]
            if tipo == "Ingreso (Venta)":
                movimientos = [
                    {"cuenta": codigo, "tipo": "DEBITO", "valor": monto, "cuenta_nombre": cuenta.split(" - ")[1]},
                    {"cuenta": "4135", "tipo": "CREDITO", "valor": monto, "cuenta_nombre": "VENTAS"}
                ]
            else:
                movimientos = [
                    {"cuenta": "5105", "tipo": "DEBITO", "valor": monto, "cuenta_nombre": "GASTOS OPERACIONALES"},
                    {"cuenta": codigo, "tipo": "CREDITO", "valor": monto, "cuenta_nombre": cuenta.split(" - ")[1]}
                ]
            
            resultado = st.session_state.libro.registrar(descripcion, tercero, movimientos)
            if resultado:
                st.success("✅ Movimiento registrado")

# ============================================
# DICCIONARIO
# ============================================
elif menu == "📖 Diccionario":
    st.markdown("<div class='section-title'>📖 Diccionario Callejero → Contabilidad</div>", unsafe_allow_html=True)
    
    df_diccionario = pd.DataFrame([
        {"Lenguaje de Barrio": "Me fiaron 4 leches", "Conta entiende": "PROVEEDORES (2101)", "Acción": "Aumenta Pasivo (CR)"},
        {"Lenguaje de Barrio": "Me debe un pan", "Conta entiende": "CUENTAS POR COBRAR (1205)", "Acción": "Aumenta Activo (DB)"},
        {"Lenguaje de Barrio": "Agarré $10 de la caja", "Conta entiende": "RETIROS PERSONAL (3105)", "Acción": "Aumenta Retiro (DB)"},
        {"Lenguaje de Barrio": "Soltó los $20 que debía", "Conta entiende": "CAJA (1101) / CxC (1205)", "Acción": "Entra Cash, Baja Deuda"},
        {"Lenguaje de Barrio": "Le pagué al de la luz", "Conta entiende": "GASTO SERVICIOS (6201)", "Acción": "Aumenta Gasto (DB)"},
        {"Lenguaje de Barrio": "Me bajaron $5 por feo", "Conta entiende": "DESCUENTO VENTAS (4105)", "Acción": "Resta al Ingreso (DB)"}
    ])
    st.dataframe(df_diccionario, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 📌 Regla de Oro")
    st.info("**'No importa si fue un peso o un millón, si se mueve, se anota.'**")

# ============================================
# BOTÓN FLOTANTE
# ============================================
st.markdown(f"""
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
    <button onclick="window.location.href='#hablar-con-conta'" 
        style="width: 60px; height: 60px; border-radius: 50%; 
               background: linear-gradient(135deg, {COLORES['verde']} 0%, #6aa84f 100%);
               color: white; border: none; font-size: 30px; cursor: pointer;
               box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        💬
    </button>
</div>
""", unsafe_allow_html=True)
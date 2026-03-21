import streamlit as st
import pandas as pd
import json
import os
import hashlib
from datetime import datetime
from openai import OpenAI

# ============================================
# CONFIGURACIÓN Y ESTILOS
# ============================================
st.set_page_config(
    page_title="Tu Amigo Contable",
    page_icon="💰",
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
    .main-header .small-logo {{
        color: {COLORES['verde']};
        font-size: 1rem;
        letter-spacing: 2px;
    }}
    .main-header .big-logo {{
        color: {COLORES['verde']};
        font-size: 3rem;
        font-weight: 800;
    }}
    .main-header .tagline {{
        color: white;
        font-size: 1.2rem;
    }}
    
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
    
    .ia-card {{
        background: linear-gradient(135deg, {COLORES['verde']} 0%, #6aa84f 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin-bottom: 1rem;
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
# CONFIGURACIÓN DE IA (OPENAI)
# ============================================
def configurar_openai():
    """Configura OpenAI con API key"""
    try:
        # Buscar API key en secrets o variable de entorno
        api_key = None
        if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
        else:
            api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key:
            client = OpenAI(api_key=api_key)
            return client
    except Exception as e:
        st.error(f"Error configurando OpenAI: {e}")
    return None

# ============================================
# CLASES CONTABLES (DE TU NOTEBOOK)
# ============================================
class Conta:
    def __init__(self, pais="Colombia", moneda="COP", grupoNIIF=2):
        self.pais = pais
        self.moneda = moneda
        self.grupoNIIF = grupoNIIF
        self.experiencia = "20 años"
        self.objetivos = {
            "general": "Pensar como contador con 20 años de experiencia",
            "especificos": [
                "Definir qué es contabilidad",
                "Conocer las áreas de la contabilidad",
                "Identificar objetivos de contabilidad financiera y administrativa",
                "Conocer ley que regula la profesión contable",
                "Identificar finalidad real de la contabilidad",
                "Conocer principios básicos y NIIF"
            ]
        }
        self.areas = {
            "financiera": {
                "activa": True,
                "proposito": "Recopilar, clasificar y registrar eventos económicos",
                "productos": ["Balance General", "Estado de Resultados", "Estado de Patrimonio", "Flujo de Efectivo"]
            },
            "administrativa": {
                "activa": True,
                "proposito": "Interpretar información para toma de decisiones",
                "indices": ["Rotación Inventario", "Cuentas por Cobrar", "Apalancamiento", "Razón Corriente", "Prueba Ácido"]
            },
            "impositiva": {
                "activa": True,
                "proposito": "Manejar aspectos fiscales",
                "impuestos": ["Renta", "IVA/ITBMS", "Licencia comercial", "Dividendos"]
            }
        }
        self.finalidad = {
            "revision": {"descripcion": "Examinar información antes de registrar", "documentos": ["facturas", "recibos", "cheques"]},
            "clasificacion": {"descripcion": "Asignar código PUC", "regla": "Identificar cuentas débito/crédito"},
            "anotacion": {"descripcion": "Registrar en libros oficiales", "tipo": "asientos contables"},
            "informacion": {"descripcion": "Presentar en estados financieros", "productos": ["Balance", "PyG", "Patrimonio", "Flujo"]},
            "interpretacion": {"descripcion": "Analizar con índices", "objetivo": "Toma de decisiones"}
        }
        self.principios = {
            "enteEconomico": "La empresa es distinta de sus dueños",
            "continuidad": "Se asume que la empresa seguirá operando",
            "unidadMedida": "Moneda local",
            "valuacion": "Costo histórico",
            "esenciaSobreForma": "Realidad económica sobre forma legal",
            "realizacion": "Registro cuando ocurre, no cuando se paga/cobra",
            "asociacion": "Ingresos y gastos en mismo período",
            "revelacionSuficiente": "Información completa para decisiones"
        }
    
    def explicar_concepto(self, concepto):
        """Explica un concepto contable en lenguaje simple"""
        explicaciones = {
            "contabilidad": "📊 La contabilidad es como un diario de tu negocio. Anotas todo lo que entra (ingresos) y todo lo que sale (gastos) para saber si estás ganando o perdiendo dinero.",
            "balance": "⚖️ El balance es una foto de tu negocio en un momento específico. Te muestra lo que tienes (activos), lo que debes (pasivos) y lo que realmente es tuyo (patrimonio).",
            "iva": "💰 El IVA es un impuesto que cobras por tus ventas y luego pagas al gobierno. Es dinero que pasa por tu negocio, no es ganancia tuya.",
            "puc": "📋 El PUC (Plan Único de Cuentas) es como un código de colores para organizar tu dinero. Cada cuenta tiene un número único.",
            "depreciacion": "📉 La depreciación es cuando algo que compraste (como un computador) pierde valor con el tiempo. La contabilidad lo reconoce como un gasto gradual."
        }
        return explicaciones.get(concepto.lower(), f"🤔 {concepto} es un término contable. Pregúntame con más detalle y te explico.")

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
        self.cuentas["1105"] = {"codigo": "1105", "nombre": "EFECTIVO", "naturaleza": "DEBITO", "clase": "BALANCE", "nivel": 3, "padre": "11", "aceptaMovimientos": True}
        self.cuentas["110505"] = {"codigo": "110505", "nombre": "CAJA", "naturaleza": "DEBITO", "clase": "BALANCE", "nivel": 4, "padre": "1105", "aceptaMovimientos": True}
        self.cuentas["110510"] = {"codigo": "110510", "nombre": "BANCOS", "naturaleza": "DEBITO", "clase": "BALANCE", "nivel": 4, "padre": "1105", "aceptaMovimientos": True}
        self.cuentas["1305"] = {"codigo": "1305", "nombre": "CLIENTES", "naturaleza": "DEBITO", "clase": "BALANCE", "nivel": 4, "aceptaMovimientos": True}
        # CLASE 2: PASIVO
        self.cuentas["2"] = {"codigo": "2", "nombre": "PASIVO", "naturaleza": "CREDITO", "clase": "BALANCE", "nivel": 1, "aceptaMovimientos": False}
        self.cuentas["2105"] = {"codigo": "2105", "nombre": "PROVEEDORES", "naturaleza": "CREDITO", "clase": "BALANCE", "nivel": 3, "aceptaMovimientos": True}
        self.cuentas["2408"] = {"codigo": "2408", "nombre": "IMPUESTOS POR PAGAR", "naturaleza": "CREDITO", "clase": "BALANCE", "nivel": 3, "aceptaMovimientos": True}
        # CLASE 4: INGRESOS
        self.cuentas["4"] = {"codigo": "4", "nombre": "INGRESOS", "naturaleza": "CREDITO", "clase": "ESTADO_RESULTADOS", "nivel": 1, "aceptaMovimientos": False}
        self.cuentas["4135"] = {"codigo": "4135", "nombre": "VENTAS", "naturaleza": "CREDITO", "clase": "ESTADO_RESULTADOS", "nivel": 3, "aceptaMovimientos": True}
        # CLASE 5: GASTOS
        self.cuentas["5"] = {"codigo": "5", "nombre": "GASTOS", "naturaleza": "DEBITO", "clase": "ESTADO_RESULTADOS", "nivel": 1, "aceptaMovimientos": False}
        self.cuentas["5105"] = {"codigo": "5105", "nombre": "GASTOS PERSONAL", "naturaleza": "DEBITO", "clase": "ESTADO_RESULTADOS", "nivel": 3, "aceptaMovimientos": True}
    
    def obtener_cuenta(self, codigo):
        return self.cuentas.get(codigo)
    
    def listar_cuentas_activas(self):
        return [cuenta for cuenta in self.cuentas.values() if cuenta.get("aceptaMovimientos", False)]

class LibroDiario:
    def __init__(self, conta, puc):
        self.conta = conta
        self.puc = puc
        self.asientos = []
        self.secuencial = 1
    
    def registrar_asiento(self, transaccion):
        try:
            for mov in transaccion["movimientos"]:
                cuenta = self.puc.obtener_cuenta(mov["cuenta"])
                if not cuenta or not cuenta.get("aceptaMovimientos", False):
                    raise Exception(f"Cuenta {mov['cuenta']} no válida")
            
            asiento = {
                "id": f"A-{self.secuencial:04d}",
                "fecha": transaccion.get("fecha", datetime.now().strftime("%Y-%m-%d")),
                "descripcion": transaccion.get("descripcion", ""),
                "tercero": transaccion.get("tercero", ""),
                "movimientos": [],
                "totalDebito": 0,
                "totalCredito": 0
            }
            
            for mov in transaccion["movimientos"]:
                cuenta = self.puc.obtener_cuenta(mov["cuenta"])
                movimiento = {
                    "cuenta": mov["cuenta"],
                    "nombre": cuenta["nombre"],
                    "detalle": mov.get("detalle", ""),
                    "debito": mov["valor"] if mov["tipo"] == "DEBITO" else 0,
                    "credito": mov["valor"] if mov["tipo"] == "CREDITO" else 0
                }
                asiento["movimientos"].append(movimiento)
                asiento["totalDebito"] += movimiento["debito"]
                asiento["totalCredito"] += movimiento["credito"]
            
            if abs(asiento["totalDebito"] - asiento["totalCredito"]) > 0.01:
                raise Exception("No cuadra la partida doble")
            
            self.asientos.append(asiento)
            self.secuencial += 1
            return {"exito": True, "asiento": asiento}
        except Exception as e:
            return {"exito": False, "error": str(e)}
    
    def obtener_ingresos(self):
        total = 0
        for a in self.asientos:
            for m in a["movimientos"]:
                if m["cuenta"] in ["4135"] and m["credito"] > 0:
                    total += m["credito"]
        return total
    
    def obtener_gastos(self):
        total = 0
        for a in self.asientos:
            for m in a["movimientos"]:
                if m["cuenta"] in ["5105"] and m["debito"] > 0:
                    total += m["debito"]
        return total
    
    def obtener_balance(self):
        return self.obtener_ingresos() - self.obtener_gastos()
    
    def obtener_ultimos_movimientos(self, n=10):
        movimientos = []
        for a in self.asientos[-n:]:
            for m in a["movimientos"]:
                movimientos.append({
                    "fecha": a["fecha"],
                    "descripcion": a["descripcion"],
                    "cuenta": m["nombre"],
                    "debito": m["debito"],
                    "credito": m["credito"],
                    "tercero": a["tercero"]
                })
        return movimientos

class AsistenteIA:
    def __init__(self, conta, libro, openai_client=None):
        self.conta = conta
        self.libro = libro
        self.client = openai_client
    
    def explicar_termino(self, termino):
        """Explica un término contable en lenguaje simple usando OpenAI"""
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": """Eres un asistente contable amigable que explica términos financieros 
                        a personas que NO saben nada de contabilidad. Usa ejemplos de la vida cotidiana, emojis, 
                        y lenguaje cálido. Máximo 100 palabras."""},
                        {"role": "user", "content": f"Explica en términos muy simples qué significa: {termino}"}
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"⚠️ Error con IA: {e}. {self.conta.explicar_concepto(termino)}"
        return self.conta.explicar_concepto(termino)
    
    def ayudar_registrar(self, descripcion_usuario):
        """Ayuda al usuario a registrar una transacción desde lenguaje natural"""
        if self.client:
            try:
                # Lista de cuentas disponibles para la IA
                cuentas = self.puc.listar_cuentas_activas()
                cuentas_str = ", ".join([f"{c['codigo']}:{c['nombre']}" for c in cuentas])
                
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"""Eres un asistente contable experto. Interpreta descripciones de transacciones.
                        
                        Cuentas disponibles (código:nombre):
                        {cuentas_str}
                        
                        Reglas:
                        - Ventas: DEBITO a CLIENTES (1305) o CAJA (110505), CREDITO a VENTAS (4135)
                        - Si es venta con IVA (19%): también CREDITO a IMPUESTOS POR PAGAR (2408)
                        - Gastos: DEBITO a GASTOS PERSONAL (5105), CREDITO a CAJA (110505) o BANCOS (110510)
                        - Compras: DEBITO a INVENTARIO (1405), CREDITO a PROVEEDORES (2105)
                        
                        Devuelve SOLO JSON válido con:
                        {{
                            "descripcion": "descripción clara",
                            "tercero": "nombre del cliente/proveedor",
                            "movimientos": [
                                {{"cuenta": "código", "tipo": "DEBITO o CREDITO", "valor": número, "detalle": "detalle"}}
                            ]
                        }}
                        """},
                        {"role": "user", "content": descripcion_usuario}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                
                import re
                text = response.choices[0].message.content
                # Extraer JSON
                json_match = re.search(r'\{.*\}', text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except Exception as e:
                st.error(f"Error IA: {e}")
        return None
    
    def recomendar(self):
        """Da recomendaciones financieras simples"""
        ingresos = self.libro.obtener_ingresos()
        gastos = self.libro.obtener_gastos()
        balance = ingresos - gastos
        
        recomendaciones = []
        
        if balance < 0:
            recomendaciones.append("⚠️ Tus gastos superan a tus ingresos. Revisa dónde puedes reducir gastos.")
        elif balance < 500000:
            recomendaciones.append("💡 Tu margen es ajustado. Busca aumentar ventas o reducir gastos pequeños.")
        else:
            recomendaciones.append("✅ Vas bien. Considera ahorrar parte de tus ganancias para futuras inversiones.")
        
        if ingresos == 0:
            recomendaciones.append("🤔 No has registrado ventas. Recuerda registrar tus ingresos para tener un control real.")
        
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Eres un asesor financiero amigable para pequeños negocios. Sé práctico y da consejos simples."},
                        {"role": "user", "content": f"Basado en ingresos=${ingresos:,.0f}, gastos=${gastos:,.0f}, balance=${balance:,.0f}. Da 2 recomendaciones cortas."}
                    ],
                    temperature=0.7,
                    max_tokens=150
                )
                recomendaciones.append(response.choices[0].message.content)
            except:
                recomendaciones.append("💡 Registra todas tus transacciones para obtener mejores recomendaciones.")
        
        return recomendaciones

# ============================================
# INICIALIZAR SISTEMA EN SESSION STATE
# ============================================
def inicializar_sistema():
    if "conta" not in st.session_state:
        st.session_state.conta = Conta()
        st.session_state.puc = PUCInteligente(st.session_state.conta)
        st.session_state.libro = LibroDiario(st.session_state.conta, st.session_state.puc)
        st.session_state.openai_client = configurar_openai()
        st.session_state.asistente = AsistenteIA(
            st.session_state.conta, 
            st.session_state.libro, 
            st.session_state.openai_client
        )
        
        # Datos de ejemplo
        ejemplos = [
            {
                "fecha": "2024-03-15",
                "descripcion": "Venta de mercancía",
                "tercero": "Cliente A",
                "movimientos": [
                    {"cuenta": "1305", "tipo": "DEBITO", "valor": 1190000, "detalle": "Cliente"},
                    {"cuenta": "4135", "tipo": "CREDITO", "valor": 1000000, "detalle": "Ventas"},
                    {"cuenta": "2408", "tipo": "CREDITO", "valor": 190000, "detalle": "IVA"}
                ]
            },
            {
                "fecha": "2024-03-20",
                "descripcion": "Venta servicios",
                "tercero": "Cliente B",
                "movimientos": [
                    {"cuenta": "110505", "tipo": "DEBITO", "valor": 500000, "detalle": "Efectivo"},
                    {"cuenta": "4135", "tipo": "CREDITO", "valor": 500000, "detalle": "Ventas"}
                ]
            }
        ]
        
        for ej in ejemplos:
            st.session_state.libro.registrar_asiento(ej)
        
        st.session_state.logged_in = False

inicializar_sistema()

# ============================================
# LOGIN SIMPLE
# ============================================
if not st.session_state.logged_in:
    st.markdown("""
    <div style='text-align: center; padding: 3rem;'>
        <h1 style='color: #345470;'>💰 Tu Amigo Contable</h1>
        <p style='font-size: 1.2rem; color: #666;'>Tu asistente contable inteligente</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.container():
            st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);'>
                <h2 style='color: #345470; text-align: center;'>Bienvenido</h2>
                <p style='text-align: center;'>Accede para gestionar tu contabilidad con ayuda de IA</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔴 Entrar con Google", use_container_width=True):
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
    <div class='tagline'>Tu asistente contable inteligente</div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Menú")
    menu = st.radio(
        "Navegación",
        ["🏠 Dashboard", "✍️ Registrar", "🤖 Asistente IA", "📚 Aprende", "📞 Contacto"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("### 💡 Consejo")
    st.info("¿No sabes contabilidad? Usa el Asistente IA para ayudarte a registrar tus movimientos.")
    
    # Mostrar estado de IA
    if st.session_state.openai_client:
        st.success("✅ IA activa")
    else:
        st.warning("⚠️ IA no disponible - Configura OPENAI_API_KEY")
    
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ============================================
# PÁGINA 1: DASHBOARD
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
            <div class='variacion positiva'>+12%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='card'>
            <h3>💸 EGRESOS</h3>
            <div class='valor'>${gastos:,.0f}</div>
            <div class='variacion negativa'>-5%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='card'>
            <h3>⚖️ BALANCE</h3>
            <div class='valor'>${balance:,.0f}</div>
            <div class='variacion positiva'>Positivo</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-title'>📋 ÚLTIMOS MOVIMIENTOS</div>", unsafe_allow_html=True)
    
    movimientos = st.session_state.libro.obtener_ultimos_movimientos(10)
    if movimientos:
        df = pd.DataFrame(movimientos)
        df["Monto"] = df.apply(lambda x: f"${x['debito'] or x['credito']:,.0f}", axis=1)
        df["Tipo"] = df.apply(lambda x: "Débito" if x['debito'] > 0 else "Crédito", axis=1)
        st.dataframe(df[["fecha", "descripcion", "cuenta", "Monto", "tercero"]], use_container_width=True, hide_index=True)
    else:
        st.info("Aún no hay movimientos registrados. Usa el Asistente IA para comenzar.")
    
    # Recomendaciones IA
    st.markdown("<div class='section-title'>💡 Recomendaciones IA</div>", unsafe_allow_html=True)
    recomendaciones = st.session_state.asistente.recomendar()
    for rec in recomendaciones:
        st.markdown(f"<div class='ia-card'>🤖 {rec}</div>", unsafe_allow_html=True)

# ============================================
# PÁGINA 2: REGISTRAR TRANSACCIÓN
# ============================================
elif menu == "✍️ Registrar":
    st.markdown("<div class='section-title'>✍️ Registrar Movimiento</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 Formulario Simple", "🤖 Asistente IA"])
    
    with tab1:
        with st.form("registro_simple"):
            st.markdown("### Datos de la transacción")
            
            col1, col2 = st.columns(2)
            with col1:
                fecha = st.date_input("Fecha", datetime.now())
                descripcion = st.text_input("Descripción", placeholder="Ej: Venta de producto")
                tercero = st.text_input("Cliente/Proveedor", placeholder="Nombre")
            with col2:
                tipo = st.selectbox("Tipo", ["Ingreso (Venta)", "Gasto (Compra)", "Gasto (Personal)"])
                cuenta = st.selectbox("Cuenta", [
                    "CAJA (110505) - Efectivo",
                    "BANCOS (110510) - Cuenta bancaria",
                    "CLIENTES (1305) - Ventas a crédito",
                    "PROVEEDORES (2105) - Compras a crédito"
                ])
                monto = st.number_input("Monto", min_value=0.0, step=10000.0, format="%0.0f")
            
            submit = st.form_submit_button("Registrar Movimiento", use_container_width=True)
            
            if submit and monto > 0:
                # Mapear cuenta seleccionada a código PUC
                cuenta_map = {
                    "CAJA (110505) - Efectivo": "110505",
                    "BANCOS (110510) - Cuenta bancaria": "110510",
                    "CLIENTES (1305) - Ventas a crédito": "1305",
                    "PROVEEDORES (2105) - Compras a crédito": "2105"
                }
                codigo_cuenta = cuenta_map.get(cuenta, "110505")
                
                if "Ingreso" in tipo:
                    # Registrar venta
                    iva = monto * 0.19
                    transaccion = {
                        "fecha": fecha.strftime("%Y-%m-%d"),
                        "descripcion": descripcion,
                        "tercero": tercero,
                        "movimientos": [
                            {"cuenta": codigo_cuenta, "tipo": "DEBITO", "valor": monto + iva, "detalle": descripcion},
                            {"cuenta": "4135", "tipo": "CREDITO", "valor": monto, "detalle": "Ventas"},
                            {"cuenta": "2408", "tipo": "CREDITO", "valor": iva, "detalle": "IVA"}
                        ]
                    }
                else:
                    # Registrar gasto
                    transaccion = {
                        "fecha": fecha.strftime("%Y-%m-%d"),
                        "descripcion": descripcion,
                        "tercero": tercero,
                        "movimientos": [
                            {"cuenta": "5105", "tipo": "DEBITO", "valor": monto, "detalle": descripcion},
                            {"cuenta": codigo_cuenta, "tipo": "CREDITO", "valor": monto, "detalle": descripcion}
                        ]
                    }
                
                resultado = st.session_state.libro.registrar_asiento(transaccion)
                if resultado["exito"]:
                    st.success(f"✅ Movimiento registrado correctamente")
                else:
                    st.error(f"❌ Error: {resultado['error']}")
    
    with tab2:
        st.markdown("""
        <div class='ia-card'>
            🤖 <strong>Asistente IA</strong><br>
            Describe con tus palabras lo que quieres registrar y la IA lo hará por ti.
        </div>
        """, unsafe_allow_html=True)
        
        descripcion_usuario = st.text_area("Describe tu transacción", 
            placeholder="Ejemplo: Vendí un producto a Juan Pérez por $100,000 en efectivo",
            height=100)
        
        if st.button("🤖 Registrar con IA", use_container_width=True):
            if descripcion_usuario:
                with st.spinner("La IA está analizando tu transacción..."):
                    # Necesitamos pasar el puc al asistente
                    st.session_state.asistente.puc = st.session_state.puc
                    resultado = st.session_state.asistente.ayudar_registrar(descripcion_usuario)
                    if resultado:
                        st.json(resultado)
                        if st.button("Confirmar y Registrar"):
                            transaccion = {
                                "fecha": datetime.now().strftime("%Y-%m-%d"),
                                "descripcion": resultado.get("descripcion", descripcion_usuario),
                                "tercero": resultado.get("tercero", ""),
                                "movimientos": resultado.get("movimientos", [])
                            }
                            if transaccion["movimientos"]:
                                registro = st.session_state.libro.registrar_asiento(transaccion)
                                if registro["exito"]:
                                    st.success("✅ Registrado con éxito")
                                else:
                                    st.error(f"Error: {registro['error']}")
                    else:
                        st.warning("No pude interpretar tu mensaje. Intenta ser más específico.")
            else:
                st.warning("Describe la transacción primero")

# ============================================
# PÁGINA 3: ASISTENTE IA
# ============================================
elif menu == "🤖 Asistente IA":
    st.markdown("<div class='section-title'>🤖 Asistente Contable IA</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='ia-card'>
        🧠 <strong>Soy tu asistente contable</strong><br>
        Pregúntame cualquier cosa sobre contabilidad, finanzas o tu negocio.
        Explico todo en términos simples.
    </div>
    """, unsafe_allow_html=True)
    
    # Chat con IA
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Mostrar historial
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div style='background: #e3f2fd; padding: 1rem; border-radius: 15px; margin-bottom: 0.5rem;'><strong>Tú:</strong> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background: {COLORES['verde']}20; padding: 1rem; border-radius: 15px; margin-bottom: 0.5rem; border-left: 4px solid {COLORES['verde']};'><strong>🤖 Asistente:</strong> {msg['content']}</div>", unsafe_allow_html=True)
    
    pregunta = st.text_input("Hazme una pregunta:", placeholder="Ej: ¿Qué es el IVA? ¿Cómo registro una venta?")
    
    if pregunta:
        st.session_state.chat_history.append({"role": "user", "content": pregunta})
        
        with st.spinner("Pensando..."):
            respuesta = st.session_state.asistente.explicar_termino(pregunta)
        
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
        st.rerun()
    
    # Botones de preguntas rápidas
    st.markdown("### 📌 Preguntas rápidas")
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    preguntas = ["¿Qué es el IVA?", "¿Qué es un balance?", "¿Cómo registro una venta?", "¿Qué es depreciación?"]
    
    for i, q in enumerate(preguntas):
        with [col_q1, col_q2, col_q3, col_q4][i]:
            if st.button(q, use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": q})
                respuesta = st.session_state.asistente.explicar_termino(q)
                st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
                st.rerun()

# ============================================
# PÁGINA 4: APRENDE
# ============================================
elif menu == "📚 Aprende":
    st.markdown("<div class='section-title'>📚 Aprende Contabilidad Fácil</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 20px; margin-bottom: 2rem;'>
        <p style='font-size: 1.2rem;'>La contabilidad no tiene que ser difícil. Aquí tienes conceptos explicados en lenguaje simple:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tarjetas de conceptos
    col_c1, col_c2 = st.columns(2)
    
    conceptos = [
        ("📊 ¿Qué es contabilidad?", "La contabilidad es como un diario de tu negocio. Anotas todo lo que entra (ingresos) y todo lo que sale (gastos) para saber si estás ganando o perdiendo dinero."),
        ("⚖️ ¿Qué es un balance?", "El balance es una foto de tu negocio en un momento específico. Te muestra lo que tienes (activos), lo que debes (pasivos) y lo que realmente es tuyo (patrimonio)."),
        ("💰 ¿Qué es el IVA?", "El IVA es un impuesto que cobras por tus ventas y luego pagas al gobierno. Es dinero que pasa por tu negocio, no es ganancia tuya."),
        ("📉 ¿Qué es depreciación?", "La depreciación es cuando algo que compraste (como un computador) pierde valor con el tiempo. La contabilidad lo reconoce poco a poco como un gasto."),
        ("💳 ¿Qué es partida doble?", "Es la regla de oro: por cada dinero que entra, otro sale. Si vendes algo, ganas dinero (ingreso) pero entregas un producto (gasto). Siempre se equilibra."),
        ("📈 ¿Qué es el PUC?", "El PUC (Plan Único de Cuentas) es como un código de colores para organizar tu dinero. Cada cuenta tiene un número único para saber exactamente qué es.")
    ]
    
    for i, (titulo, contenido) in enumerate(conceptos):
        if i % 2 == 0:
            with col_c1:
                with st.expander(titulo):
                    st.write(contenido)
        else:
            with col_c2:
                with st.expander(titulo):
                    st.write(contenido)
    
    st.markdown("---")
    st.markdown("### 🎓 ¿Quieres aprender más?")
    st.info("Pregúntale al Asistente IA cualquier concepto contable. Explica todo en términos simples.")

# ============================================
# PÁGINA 5: CONTACTO
# ============================================
elif menu == "📞 Contacto":
    st.markdown("<div class='section-title'>📞 Contáctanos</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 20px;'>
            <h3 style='color: #345470;'>📍 Ubicación</h3>
            <p>Cedritos, Bogotá, Colombia</p>
            
            <h3 style='color: #345470; margin-top: 1.5rem;'>📧 Email</h3>
            <p>soporte@tuamigocontable.com</p>
            
            <h3 style='color: #345470; margin-top: 1.5rem;'>📞 Teléfono</h3>
            <p>+57 (601) 123-4567</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        df_mapa = pd.DataFrame({'lat': [4.7228], 'lon': [-74.0450]})
        st.map(df_mapa, zoom=13)

# ============================================
# BOTÓN FLOTANTE IA
# ============================================
st.markdown(f"""
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
    <button onclick="window.location.href='#asistente-ia'" 
        style="width: 60px; height: 60px; border-radius: 50%; 
               background: linear-gradient(135deg, {COLORES['verde']} 0%, #6aa84f 100%);
               color: white; border: none; font-size: 30px; cursor: pointer;
               box-shadow: 0 4px 15px rgba(0,0,0,0.3); animation: pulse 2s infinite;">
        🤖
    </button>
</div>
""", unsafe_allow_html=True)
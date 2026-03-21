import streamlit as st
import pandas as pd
import json
import os
import hashlib
from datetime import datetime, timedelta
from openai import OpenAI
import plotly.graph_objects as go
import plotly.express as px

# ============================================
# CONFIGURACIÓN Y ESTILOS
# ============================================
st.set_page_config(
    page_title="Tu Amigo Contable",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colores
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
    
    .ia-card {{
        background: linear-gradient(135deg, {COLORES['verde']} 0%, #6aa84f 100%);
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
    .chat-message-bot {{
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
# CLASES CONTABLES
# ============================================
class Conta:
    def __init__(self, usuario_id="default"):
        self.usuario_id = usuario_id
        self.pais = "Colombia"
        self.moneda = "COP"
        
    def hablar_como_contador(self, mensaje):
        """Responde como un contador amigable"""
        return f"📊 Como contador con 20 años de experiencia, te explico: {mensaje}"

class PUCInteligente:
    def __init__(self):
        self.cuentas = {
            "110505": {"codigo": "110505", "nombre": "CAJA", "naturaleza": "DEBITO", "tipo": "ACTIVO"},
            "110510": {"codigo": "110510", "nombre": "BANCOS", "naturaleza": "DEBITO", "tipo": "ACTIVO"},
            "1305": {"codigo": "1305", "nombre": "CLIENTES", "naturaleza": "DEBITO", "tipo": "ACTIVO"},
            "2105": {"codigo": "2105", "nombre": "PROVEEDORES", "naturaleza": "CREDITO", "tipo": "PASIVO"},
            "2408": {"codigo": "2408", "nombre": "IMPUESTOS POR PAGAR", "naturaleza": "CREDITO", "tipo": "PASIVO"},
            "4135": {"codigo": "4135", "nombre": "VENTAS", "naturaleza": "CREDITO", "tipo": "INGRESO"},
            "5105": {"codigo": "5105", "nombre": "GASTOS OPERACIONALES", "naturaleza": "DEBITO", "tipo": "GASTO"},
            "510510": {"codigo": "510510", "nombre": "GASTOS PERSONAL", "naturaleza": "DEBITO", "tipo": "GASTO"},
            "510515": {"codigo": "510515", "nombre": "GASTOS SERVICIOS", "naturaleza": "DEBITO", "tipo": "GASTO"},
        }
    
    def obtener_cuenta(self, codigo):
        return self.cuentas.get(codigo)
    
    def listar_cuentas(self):
        return list(self.cuentas.values())

class LibroDiario:
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id
        self.asientos = []
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga datos del usuario desde archivo local"""
        archivo = f"datos_{self.usuario_id}.json"
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r') as f:
                    data = json.load(f)
                    self.asientos = data.get('asientos', [])
            except:
                self.asientos = []
    
    def guardar_datos(self):
        """Guarda datos del usuario"""
        archivo = f"datos_{self.usuario_id}.json"
        with open(archivo, 'w') as f:
            json.dump({'asientos': self.asientos}, f)
    
    def registrar(self, descripcion, tercero, movimientos):
        """Registra un nuevo asiento"""
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
        """Calcula ingresos totales"""
        hoy = datetime.now()
        if periodo == "mes":
            fecha_inicio = hoy.replace(day=1)
        elif periodo == "trimestre":
            mes_inicio = ((hoy.month - 1) // 3) * 3 + 1
            fecha_inicio = hoy.replace(month=mes_inicio, day=1)
        elif periodo == "año":
            fecha_inicio = hoy.replace(month=1, day=1)
        else:
            fecha_inicio = hoy - timedelta(days=30)
        
        total = 0
        for a in self.asientos:
            fecha_asiento = datetime.strptime(a["fecha"], "%Y-%m-%d")
            if fecha_asiento >= fecha_inicio:
                for m in a["movimientos"]:
                    if m["tipo"] == "CREDITO" and "VENTAS" in m.get("cuenta_nombre", ""):
                        total += m["valor"]
        return total
    
    def obtener_gastos(self, periodo="mes"):
        """Calcula gastos totales"""
        hoy = datetime.now()
        if periodo == "mes":
            fecha_inicio = hoy.replace(day=1)
        elif periodo == "trimestre":
            mes_inicio = ((hoy.month - 1) // 3) * 3 + 1
            fecha_inicio = hoy.replace(month=mes_inicio, day=1)
        elif periodo == "año":
            fecha_inicio = hoy.replace(month=1, day=1)
        else:
            fecha_inicio = hoy - timedelta(days=30)
        
        total = 0
        for a in self.asientos:
            fecha_asiento = datetime.strptime(a["fecha"], "%Y-%m-%d")
            if fecha_asiento >= fecha_inicio:
                for m in a["movimientos"]:
                    if m["tipo"] == "DEBITO" and "GASTOS" in m.get("cuenta_nombre", ""):
                        total += m["valor"]
        return total
    
    def obtener_balance(self):
        return self.obtener_ingresos() - self.obtener_gastos()
    
    def obtener_movimientos_recientes(self, n=10):
        return self.asientos[-n:][::-1]
    
    def obtener_estadisticas(self):
        """Calcula estadísticas para reportes"""
        ingresos_mensuales = []
        gastos_mensuales = []
        meses = []
        
        for i in range(6):
            fecha = datetime.now().replace(day=1) - timedelta(days=30*i)
            mes_nombre = fecha.strftime("%B")
            meses.insert(0, mes_nombre)
            
            # Calcular para ese mes
            inicio_mes = fecha.replace(day=1)
            fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            ing_mes = 0
            gas_mes = 0
            
            for a in self.asientos:
                fecha_a = datetime.strptime(a["fecha"], "%Y-%m-%d")
                if inicio_mes <= fecha_a <= fin_mes:
                    for m in a["movimientos"]:
                        if m["tipo"] == "CREDITO" and "VENTAS" in m.get("cuenta_nombre", ""):
                            ing_mes += m["valor"]
                        if m["tipo"] == "DEBITO" and "GASTOS" in m.get("cuenta_nombre", ""):
                            gas_mes += m["valor"]
            
            ingresos_mensuales.insert(0, ing_mes)
            gastos_mensuales.insert(0, gas_mes)
        
        return {
            "meses": meses,
            "ingresos": ingresos_mensuales,
            "gastos": gastos_mensuales,
            "balance": sum(ingresos_mensuales) - sum(gastos_mensuales)
        }

class AsistenteContable:
    def __init__(self, openai_client, libro):
        self.client = openai_client
        self.libro = libro
        self.contexto = []
    
    def hablar(self, mensaje_usuario):
        """Responde como un contador amigable y conversacional"""
        if not self.client:
            return self.respuesta_sin_ia(mensaje_usuario)
        
        # Obtener contexto financiero del usuario
        ingresos = self.libro.obtener_ingresos()
        gastos = self.libro.obtener_gastos()
        balance = ingresos - gastos
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"""Eres "Tu Amigo Contable", un asistente contable cálido y amigable.
                    
                    DATOS DEL USUARIO:
                    - Ingresos totales: ${ingresos:,.0f}
                    - Gastos totales: ${gastos:,.0f}
                    - Balance: ${balance:,.0f}
                    
                    INSTRUCCIONES:
                    - Habla como un contador con 20 años de experiencia pero en lenguaje simple
                    - Usa emojis para hacer la conversación más amigable
                    - Sé cálido, cercano y motivador
                    - Explica conceptos contables con ejemplos de la vida real
                    - Si el usuario quiere registrar algo, ayúdalo a hacerlo
                    - Si pregunta por sus finanzas, usa los datos reales
                    - Máximo 150 palabras por respuesta
                    """,
                    },
                    {"role": "user", "content": mensaje_usuario}
                ],
                temperature=0.7,
                max_tokens=300
            )
            respuesta = response.choices[0].message.content
            self.contexto.append({"user": mensaje_usuario, "bot": respuesta})
            return respuesta
        except Exception as e:
            return f"⚠️ Error: {e}\n\n{self.respuesta_sin_ia(mensaje_usuario)}"
    
    def respuesta_sin_ia(self, mensaje):
        """Respuesta básica sin IA"""
        if "registrar" in mensaje.lower() or "venta" in mensaje.lower():
            return "📝 ¡Claro! Para registrar una venta, necesito saber: ¿qué vendiste?, ¿a quién?, ¿por cuánto?, ¿en efectivo o crédito?"
        elif "balance" in mensaje.lower() or "ganancia" in mensaje.lower():
            ingresos = self.libro.obtener_ingresos()
            gastos = self.libro.obtener_gastos()
            return f"💰 Según tus registros, tus ingresos son ${ingresos:,.0f}, tus gastos ${gastos:,.0f} y tu balance es ${ingresos - gastos:,.0f}. ¿Quieres registrar más movimientos?"
        else:
            return "🤗 ¡Hola! Soy tu asistente contable. Puedo ayudarte a registrar ventas, gastos, y mostrarte tus reportes financieros. ¿Qué necesitas hoy?"
    
    def interpretar_transaccion(self, texto):
        """Interpreta una descripción de transacción para registrarla"""
        if not self.client:
            return None
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """Eres un asistente contable experto. Interpreta transacciones y devuelve SOLO JSON.

Reglas:
- Venta: DEBITO a CAJA (110505) o CLIENTES (1305), CREDITO a VENTAS (4135)
- Si es venta, calcular IVA 19% como CREDITO a IMPUESTOS POR PAGAR (2408)
- Gasto: DEBITO a GASTOS OPERACIONALES (5105), CREDITO a CAJA (110505)

Devuelve JSON:
{
    "descripcion": "descripción",
    "tercero": "cliente/proveedor",
    "movimientos": [
        {"cuenta": "110505", "tipo": "DEBITO", "valor": 100000, "detalle": "detalle"}
    ]
}"""},
                    {"role": "user", "content": texto}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            import re
            text = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return None

# ============================================
# FUNCIONES DE REPORTES
# ============================================
def mostrar_reportes(libro):
    """Genera reportes profesionales en el dashboard"""
    stats = libro.obtener_estadisticas()
    ingresos = libro.obtener_ingresos()
    gastos = libro.obtener_gastos()
    balance = ingresos - gastos
    
    # Tarjetas principales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='card'>
            <h3>💰 INGRESOS</h3>
            <div class='valor'>${ingresos:,.0f}</div>
            <div style='color: {COLORES["verde"]};'>↑ vs mes anterior</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='card'>
            <h3>💸 GASTOS</h3>
            <div class='valor'>${gastos:,.0f}</div>
            <div style='color: {COLORES["rojo"]};'>↓ vs mes anterior</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        color_balance = COLORES["verde"] if balance >= 0 else COLORES["rojo"]
        st.markdown(f"""
        <div class='card'>
            <h3>⚖️ BALANCE</h3>
            <div class='valor'>${balance:,.0f}</div>
            <div style='color: {color_balance};'>{'Positivo' if balance >= 0 else 'Negativo'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de evolución
    st.markdown("<div class='section-title'>📈 Evolución Financiera</div>", unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stats["meses"], y=stats["ingresos"], 
                             name="Ingresos", line=dict(color=COLORES["verde"], width=3)))
    fig.add_trace(go.Scatter(x=stats["meses"], y=stats["gastos"], 
                             name="Gastos", line=dict(color=COLORES["rojo"], width=3)))
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title="Ingresos vs Gastos por Mes",
        xaxis_title="Mes",
        yaxis_title="Monto (COP)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de movimientos recientes
    st.markdown("<div class='section-title'>📋 Últimos Movimientos</div>", unsafe_allow_html=True)
    
    movimientos = libro.obtener_movimientos_recientes(10)
    if movimientos:
        data = []
        for m in movimientos:
            for mov in m["movimientos"]:
                data.append({
                    "Fecha": m["fecha"],
                    "Descripción": m["descripcion"],
                    "Cliente/Proveedor": m["tercero"],
                    "Cuenta": mov.get("cuenta_nombre", mov.get("cuenta", "")),
                    "Débito": f"${mov['valor']:,.0f}" if mov["tipo"] == "DEBITO" else "-",
                    "Crédito": f"${mov['valor']:,.0f}" if mov["tipo"] == "CREDITO" else "-"
                })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Aún no hay movimientos registrados. ¡Comienza registrando tu primera venta o gasto!")
    
    # Consejos financieros
    st.markdown("<div class='section-title'>💡 Consejos para tu Negocio</div>", unsafe_allow_html=True)
    
    if balance > 0:
        st.success(f"✅ ¡Excelente! Tienes un balance positivo de ${balance:,.0f}. Considera ahorrar al menos el 20% para impuestos y emergencias.")
    elif balance == 0:
        st.warning("⚠️ Estás en punto de equilibrio. Revisa tus gastos fijos y busca aumentar tus ventas.")
    else:
        st.error(f"⚠️ Tus gastos superan a tus ingresos por ${abs(balance):,.0f}. Revisa tus gastos variables y considera reducir costos.")
    
    if ingresos == 0:
        st.info("📝 No has registrado ingresos aún. Recuerda registrar todas tus ventas para tener un control real de tu negocio.")

# ============================================
# INICIALIZACIÓN
# ============================================
def inicializar_sistema():
    if "usuario_id" not in st.session_state:
        st.session_state.usuario_id = "demo_user"
    if "libro" not in st.session_state:
        st.session_state.libro = LibroDiario(st.session_state.usuario_id)
    if "openai_client" not in st.session_state:
        st.session_state.openai_client = configurar_openai()
    if "asistente" not in st.session_state:
        st.session_state.asistente = AsistenteContable(
            st.session_state.openai_client, 
            st.session_state.libro
        )
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

inicializar_sistema()

# ============================================
# LOGIN
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
        if st.button("🔴 Entrar como Invitado", use_container_width=True):
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
        ["🏠 Dashboard", "📸 Escanear Factura", "💬 Conversar con IA", "✍️ Registrar Manual", "📚 Aprende"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    
    # Estado de IA
    if st.session_state.openai_client:
        st.success("✅ IA conectada")
    else:
        st.warning("⚠️ IA no disponible")
    
    # Datos del usuario
    st.markdown(f"**👤 Usuario:** Demo")
    st.markdown(f"**📅 Última actividad:** {datetime.now().strftime('%d/%m/%Y')}")
    
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ============================================
# PÁGINA 1: DASHBOARD
# ============================================
if menu == "🏠 Dashboard":
    mostrar_reportes(st.session_state.libro)

# ============================================
# PÁGINA 2: ESCANEAR FACTURA (OCR SIMULADO)
# ============================================
elif menu == "📸 Escanear Factura":
    st.markdown("<div class='section-title'>📸 Escanear Factura</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='ia-card'>
        🤖 <strong>Escáner Inteligente de Facturas</strong><br>
        Sube una foto o factura y la IA leerá los datos automáticamente.
        <br><br>
        <small>📌 Por ahora puedes probar con descripciones de facturas:</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulación de OCR (por ahora texto manual)
    texto_factura = st.text_area(
        "📄 Copia el texto de tu factura aquí:",
        placeholder="Ejemplo:\nFACTURA No. 001\nCliente: Juan Pérez\nFecha: 20/03/2026\nTotal: $150,000\nIVA 19%\nProducto: Camisa",
        height=150
    )
    
    if st.button("🔍 Analizar Factura con IA", use_container_width=True):
        if texto_factura:
            with st.spinner("🤖 La IA está analizando la factura..."):
                prompt = f"""
                Analiza esta factura y extrae la información clave. Devuelve SOLO JSON:
                
                Texto: {texto_factura}
                
                Formato esperado:
                {{
                    "tipo": "venta" o "gasto",
                    "tercero": "nombre del cliente/proveedor",
                    "fecha": "YYYY-MM-DD",
                    "total": número,
                    "iva": número,
                    "productos": ["producto1", "producto2"]
                }}
                """
                
                if st.session_state.openai_client:
                    try:
                        response = st.session_state.openai_client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.2,
                            max_tokens=300
                        )
                        import re
                        text = response.choices[0].message.content
                        json_match = re.search(r'\{.*\}', text, re.DOTALL)
                        if json_match:
                            datos = json.loads(json_match.group())
                            st.success("✅ Datos extraídos correctamente:")
                            st.json(datos)
                            
                            if st.button("📝 Registrar esta Factura"):
                                if datos["tipo"] == "venta":
                                    iva = datos.get("iva", datos["total"] * 0.19)
                                    movimientos = [
                                        {"cuenta": "110505", "tipo": "DEBITO", "valor": datos["total"], "cuenta_nombre": "CAJA", "detalle": datos.get("productos", ["Venta"])[0]},
                                        {"cuenta": "4135", "tipo": "CREDITO", "valor": datos["total"] - iva, "cuenta_nombre": "VENTAS", "detalle": "Venta"},
                                    ]
                                    if iva > 0:
                                        movimientos.append({"cuenta": "2408", "tipo": "CREDITO", "valor": iva, "cuenta_nombre": "IMPUESTOS POR PAGAR", "detalle": "IVA"})
                                else:
                                    movimientos = [
                                        {"cuenta": "5105", "tipo": "DEBITO", "valor": datos["total"], "cuenta_nombre": "GASTOS OPERACIONALES", "detalle": datos.get("productos", ["Gasto"])[0]},
                                        {"cuenta": "110505", "tipo": "CREDITO", "valor": datos["total"], "cuenta_nombre": "CAJA", "detalle": "Pago"},
                                    ]
                                
                                resultado = st.session_state.libro.registrar(
                                    descripcion=f"Factura {datos.get('productos', ['compra'])[0]}",
                                    tercero=datos.get("tercero", ""),
                                    movimientos=movimientos
                                )
                                st.success("✅ ¡Factura registrada exitosamente!")
                                st.rerun()
                    except Exception as e:
                        st.error(f"Error al analizar: {e}")
                else:
                    st.warning("IA no disponible. Configura tu API key.")
        else:
            st.warning("Pega el texto de una factura para analizar")

# ============================================
# PÁGINA 3: CONVERSAR CON IA
# ============================================
elif menu == "💬 Conversar con IA":
    st.markdown("<div class='section-title'>💬 Conversa con Tu Amigo Contable</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='ia-card'>
        🧠 <strong>Habla conmigo como si fuera tu contador personal</strong><br>
        Puedes preguntarme sobre tus finanzas, pedirme que registre movimientos, o consultar conceptos contables.
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar historial de conversación
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-message-user'><strong>Tú:</strong> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-message-bot'><strong>🤖 Tu Amigo Contable:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
    
    # Input del usuario
    mensaje = st.text_input("Escribe tu mensaje:", placeholder="Ej: ¿Cómo voy con mis finanzas? o Registra una venta de $100,000 a Juan")
    
    col_enviar, col_limpiar = st.columns([4, 1])
    with col_enviar:
        if st.button("📤 Enviar", use_container_width=True):
            if mensaje:
                st.session_state.chat_history.append({"role": "user", "content": mensaje})
                
                with st.spinner("🤖 Pensando..."):
                    # Verificar si es una transacción para registrar
                    if any(palabra in mensaje.lower() for palabra in ["registrar", "venta", "gasto", "compré", "vendí", "pagué"]):
                        transaccion = st.session_state.asistente.interpretar_transaccion(mensaje)
                        if transaccion and transaccion.get("movimientos"):
                            resultado = st.session_state.libro.registrar(
                                descripcion=transaccion.get("descripcion", mensaje),
                                tercero=transaccion.get("tercero", ""),
                                movimientos=transaccion["movimientos"]
                            )
                            if resultado:
                                respuesta = f"✅ ¡Listo! He registrado {transaccion.get('descripcion', 'tu transacción')} por ${sum(m['valor'] for m in transaccion['movimientos'] if m['tipo'] == 'DEBITO'):,.0f}. ¿Quieres registrar algo más?"
                            else:
                                respuesta = "⚠️ Tuve un problema al registrar. ¿Podrías darme más detalles?"
                        else:
                            respuesta = st.session_state.asistente.hablar(mensaje)
                    else:
                        respuesta = st.session_state.asistente.hablar(mensaje)
                
                st.session_state.chat_history.append({"role": "bot", "content": respuesta})
                st.rerun()
    
    with col_limpiar:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Sugerencias rápidas
    st.markdown("### 📌 Preguntas sugeridas")
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    sugerencias = ["¿Cómo voy con mis finanzas?", "Registra una venta de $50,000", "¿Qué es el IVA?", "¿Cómo puedo ahorrar más?"]
    
    for i, sug in enumerate(sugerencias):
        with [col_s1, col_s2, col_s3, col_s4][i]:
            if st.button(sug, use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": sug})
                
                with st.spinner("🤖 Pensando..."):
                    if "registra" in sug.lower():
                        transaccion = st.session_state.asistente.interpretar_transaccion(sug)
                        if transaccion and transaccion.get("movimientos"):
                            resultado = st.session_state.libro.registrar(
                                descripcion=transaccion.get("descripcion", sug),
                                tercero=transaccion.get("tercero", ""),
                                movimientos=transaccion["movimientos"]
                            )
                            respuesta = f"✅ ¡Registrado! Tu balance actual es ${st.session_state.libro.obtener_balance():,.0f}"
                        else:
                            respuesta = st.session_state.asistente.hablar(sug)
                    else:
                        respuesta = st.session_state.asistente.hablar(sug)
                
                st.session_state.chat_history.append({"role": "bot", "content": respuesta})
                st.rerun()

# ============================================
# PÁGINA 4: REGISTRAR MANUAL
# ============================================
elif menu == "✍️ Registrar Manual":
    st.markdown("<div class='section-title'>✍️ Registrar Movimiento Manual</div>", unsafe_allow_html=True)
    
    with st.form("registro_manual"):
        col1, col2 = st.columns(2)
        with col1:
            descripcion = st.text_input("Descripción", placeholder="Ej: Venta de producto")
            tercero = st.text_input("Cliente/Proveedor", placeholder="Nombre")
            fecha = st.date_input("Fecha", datetime.now())
        with col2:
            tipo = st.selectbox("Tipo", ["Ingreso (Venta)", "Gasto"])
            monto = st.number_input("Monto", min_value=0.0, step=10000.0, format="%0.0f")
            metodo = st.selectbox("Método de pago", ["Efectivo", "Banco", "Crédito"])
        
        submit = st.form_submit_button("Registrar Movimiento", use_container_width=True)
        
        if submit and monto > 0:
            if tipo == "Ingreso (Venta)":
                iva = monto * 0.19
                movimientos = [
                    {"cuenta": "110505" if metodo == "Efectivo" else "110510", "tipo": "DEBITO", "valor": monto + iva, "cuenta_nombre": "CAJA" if metodo == "Efectivo" else "BANCOS", "detalle": descripcion},
                    {"cuenta": "4135", "tipo": "CREDITO", "valor": monto, "cuenta_nombre": "VENTAS", "detalle": "Venta"},
                ]
                if iva > 0:
                    movimientos.append({"cuenta": "2408", "tipo": "CREDITO", "valor": iva, "cuenta_nombre": "IMPUESTOS POR PAGAR", "detalle": "IVA"})
            else:
                movimientos = [
                    {"cuenta": "5105", "tipo": "DEBITO", "valor": monto, "cuenta_nombre": "GASTOS OPERACIONALES", "detalle": descripcion},
                    {"cuenta": "110505" if metodo == "Efectivo" else "110510", "tipo": "CREDITO", "valor": monto, "cuenta_nombre": "CAJA" if metodo == "Efectivo" else "BANCOS", "detalle": "Pago"},
                ]
            
            resultado = st.session_state.libro.registrar(descripcion, tercero, movimientos)
            if resultado:
                st.success("✅ Movimiento registrado correctamente")
            else:
                st.error("Error al registrar")

# ============================================
# PÁGINA 5: APRENDE
# ============================================
elif menu == "📚 Aprende":
    st.markdown("<div class='section-title'>📚 Aprende Contabilidad Fácil</div>", unsafe_allow_html=True)
    
    conceptos = {
        "📊 ¿Qué es contabilidad?": "La contabilidad es como un diario de tu negocio. Anotas todo lo que entra (ingresos) y todo lo que sale (gastos) para saber si estás ganando o perdiendo dinero.",
        "⚖️ ¿Qué es un balance?": "El balance es una foto de tu negocio en un momento específico. Te muestra lo que tienes (activos), lo que debes (pasivos) y lo que realmente es tuyo (patrimonio).",
        "💰 ¿Qué es el IVA?": "El IVA es un impuesto que cobras por tus ventas y luego pagas al gobierno. En Colombia es del 19%. Es dinero que pasa por tu negocio, no es ganancia tuya.",
        "📈 ¿Qué es una utilidad?": "La utilidad es lo que te sobra después de restar todos tus gastos de tus ingresos. Si vendes $100 y gastaste $70, tu utilidad es $30.",
        "💳 ¿Qué es partida doble?": "Es la regla de oro: por cada dinero que entra, otro sale. Si vendes algo, ganas dinero pero entregas un producto. Siempre se equilibra."
    }
    
    col1, col2 = st.columns(2)
    for i, (titulo, contenido) in enumerate(conceptos.items()):
        with col1 if i % 2 == 0 else col2:
            with st.expander(titulo):
                st.write(contenido)
    
    st.markdown("---")
    st.markdown("### 🎓 ¿Quieres aprender más?")
    st.info("💬 Ve a la sección 'Conversar con IA' y pregúntame cualquier concepto contable. ¡Te explico todo en términos simples!")

# ============================================
# BOTÓN FLOTANTE IA
# ============================================
st.markdown(f"""
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
    <button onclick="window.location.href='#conversar-con-ia'" 
        style="width: 60px; height: 60px; border-radius: 50%; 
               background: linear-gradient(135deg, {COLORES['verde']} 0%, #6aa84f 100%);
               color: white; border: none; font-size: 30px; cursor: pointer;
               box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        💬
    </button>
</div>
""", unsafe_allow_html=True)
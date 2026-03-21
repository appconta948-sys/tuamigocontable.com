# main.py
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ========== CONFIGURACIÓN ==========
st.set_page_config(
    page_title="Tu Amigo Contable - CONTA",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CSS PERSONALIZADO ==========
st.markdown("""
<style>
    /* Estilo general */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Botones de navegación */
    .nav-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(102,126,234,0.4);
    }
    
    /* Tarjetas de métricas */
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 0.8rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 0.9rem;
        color: #666;
    }
    
    .metric-card .value {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    /* Títulos */
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
        color: #333;
        border-left: 4px solid #667eea;
        padding-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== INICIALIZACIÓN ==========
def inicializar_datos():
    """Inicializa los datos de ejemplo según tu modelo de negocio"""
    
    if 'transacciones' not in st.session_state:
        # Datos de ejemplo para mostrar funcionalidad
        datos_ejemplo = {
            'fecha': pd.date_range(start='2024-01-01', periods=20, freq='D'),
            'concepto': [
                'Venta suscripción mensual', 'Compra insumos', 'Venta suscripción trimestral',
                'Pago hosting', 'Venta suscripción anual', 'Gastos marketing',
                'Venta suscripción mensual', 'Pago API OpenAI', 'Venta suscripción mensual',
                'Gastos administrativos', 'Venta suscripción trimestral', 'Pago servicios',
                'Venta suscripción mensual', 'Gastos publicidad', 'Venta suscripción anual',
                'Pago salarios', 'Venta suscripción mensual', 'Gastos operativos',
                'Venta suscripción trimestral', 'Pago herramientas'
            ],
            'ingreso': [
                8, 0, 19, 0, 83, 0, 8, 0, 8, 0, 19, 0, 8, 0, 83, 0, 8, 0, 19, 0
            ],
            'gasto': [
                0, 50, 0, 14, 0, 100, 0, 1, 0, 200, 0, 30, 0, 80, 0, 400, 0, 50, 0, 25
            ],
            'categoria': [
                'Ingresos', 'Gastos Operativos', 'Ingresos', 'Gastos Operativos',
                'Ingresos', 'Marketing', 'Ingresos', 'Gastos Operativos',
                'Ingresos', 'Gastos Administrativos', 'Ingresos', 'Gastos Operativos',
                'Ingresos', 'Marketing', 'Ingresos', 'Gastos Administrativos',
                'Ingresos', 'Gastos Operativos', 'Ingresos', 'Gastos Operativos'
            ]
        }
        st.session_state.transacciones = pd.DataFrame(datos_ejemplo)
        st.session_state.transacciones['fecha'] = pd.to_datetime(st.session_state.transacciones['fecha'])
    
    if 'usuarios' not in st.session_state:
        st.session_state.usuarios = {
            'activos': 47,
            'prueba_gratis': 23,
            'suscriptores_mensual': 15,
            'suscriptores_trimestral': 6,
            'suscriptores_anual': 3
        }
    
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"

def calcular_metricas():
    """Calcula métricas financieras"""
    df = st.session_state.transacciones
    
    total_ingresos = df['ingreso'].sum()
    total_gastos = df['gasto'].sum()
    balance = total_ingresos - total_gastos
    
    # Ingresos por tipo de suscripción
    ingresos_suscripciones = {
        'Mensual ($8)': len(df[df['concepto'].str.contains('mensual', case=False)]) * 8,
        'Trimestral ($19)': len(df[df['concepto'].str.contains('trimestral', case=False)]) * 19,
        'Anual ($83)': len(df[df['concepto'].str.contains('anual', case=False)]) * 83
    }
    
    return {
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'balance': balance,
        'rentabilidad': (balance / total_ingresos * 100) if total_ingresos > 0 else 0,
        'ingresos_suscripciones': ingresos_suscripciones
    }

# ========== DASHBOARD PRINCIPAL ==========
def dashboard():
    """Página principal del dashboard"""
    
    st.title("💰 Dashboard - Tu Amigo Contable")
    st.markdown("Bienvenido/a a tu asistente contable personal. Aquí tienes un resumen de tus finanzas.")
    
    # Métricas principales
    metricas = calcular_metricas()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Total Ingresos</h3>
            <div class="value">${metricas['total_ingresos']:,.2f}</div>
            <small>USD</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💸 Total Gastos</h3>
            <div class="value">${metricas['total_gastos']:,.2f}</div>
            <small>USD</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = "green" if metricas['balance'] > 0 else "red"
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚖️ Balance</h3>
            <div class="value" style="color: {color};">${metricas['balance']:,.2f}</div>
            <small>USD</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Rentabilidad</h3>
            <div class="value">{metricas['rentabilidad']:.1f}%</div>
            <small>sobre ingresos</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Evolución de Ingresos vs Gastos")
        df_evolucion = st.session_state.transacciones.groupby('fecha').agg({
            'ingreso': 'sum',
            'gasto': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_evolucion['fecha'], y=df_evolucion['ingreso'], 
                                 name='Ingresos', line=dict(color='#00ff87', width=3)))
        fig.add_trace(go.Scatter(x=df_evolucion['fecha'], y=df_evolucion['gasto'], 
                                 name='Gastos', line=dict(color='#ff6b6b', width=3)))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Fecha",
            yaxis_title="Monto (USD)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Ingresos por Suscripción")
        
        # Datos de suscripciones
        suscripciones = pd.DataFrame({
            'Plan': list(metricas['ingresos_suscripciones'].keys()),
            'Ingresos': list(metricas['ingresos_suscripciones'].values())
        })
        
        fig = px.pie(suscripciones, values='Ingresos', names='Plan', 
                     color_discrete_sequence=['#667eea', '#764ba2', '#f093fb'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Usuarios activos
    st.markdown("---")
    st.subheader("👥 Usuarios Activos")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Usuarios", st.session_state.usuarios['activos'], 
                  delta=f"+{st.session_state.usuarios['prueba_gratis']} en prueba")
    with col2:
        st.metric("Plan Mensual", st.session_state.usuarios['suscriptores_mensual'])
    with col3:
        st.metric("Plan Trimestral", st.session_state.usuarios['suscriptores_trimestral'])
    with col4:
        st.metric("Plan Anual", st.session_state.usuarios['suscriptores_anual'])
    
    # Últimas transacciones
    st.markdown("---")
    st.subheader("📋 Últimas Transacciones")
    
    ultimas = st.session_state.transacciones.tail(10).sort_values('fecha', ascending=False)
    st.dataframe(ultimas[['fecha', 'concepto', 'ingreso', 'gasto', 'categoria']], 
                 use_container_width=True)

def registro_diario():
    """Registro de transacciones diarias"""
    st.title("📝 Registro Diario")
    st.markdown("Registra tus transacciones en lenguaje cotidiano")
    
    # Formulario de registro
    with st.form("registro_form"):
        st.subheader("Nueva Transacción")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fecha = st.date_input("Fecha", datetime.now())
            concepto = st.text_input("Concepto/Descripción", 
                                     placeholder="Ej: Venta suscripción mensual")
            categoria = st.selectbox("Categoría", 
                                     ["Ingresos", "Gastos Operativos", 
                                      "Gastos Administrativos", "Marketing"])
        
        with col2:
            tipo = st.radio("Tipo", ["💰 Ingreso", "💸 Gasto"], horizontal=True)
            monto = st.number_input("Monto (USD)", min_value=0.0, step=1.0)
            
            if tipo == "💰 Ingreso":
                ingreso = monto
                gasto = 0
            else:
                ingreso = 0
                gasto = monto
        
        submitted = st.form_submit_button("✅ Registrar Transacción", use_container_width=True)
        
        if submitted and concepto and monto > 0:
            nueva = pd.DataFrame({
                'fecha': [fecha],
                'concepto': [concepto],
                'ingreso': [ingreso],
                'gasto': [gasto],
                'categoria': [categoria]
            })
            st.session_state.transacciones = pd.concat([st.session_state.transacciones, nueva], ignore_index=True)
            st.success("✅ Transacción registrada correctamente!")
            st.balloons()
    
    # Resumen del día
    st.markdown("---")
    st.subheader("📊 Resumen del Día")
    
    hoy = datetime.now().date()
    transacciones_hoy = st.session_state.transacciones[
        st.session_state.transacciones['fecha'].dt.date == hoy
    ]
    
    if not transacciones_hoy.empty:
        ingresos_hoy = transacciones_hoy['ingreso'].sum()
        gastos_hoy = transacciones_hoy['gasto'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Ingresos Hoy", f"${ingresos_hoy:,.2f}")
        col2.metric("Gastos Hoy", f"${gastos_hoy:,.2f}")
        col3.metric("Balance Hoy", f"${ingresos_hoy - gastos_hoy:,.2f}")
        
        st.dataframe(transacciones_hoy[['concepto', 'ingreso', 'gasto', 'categoria']], 
                     use_container_width=True)
    else:
        st.info("📭 No hay transacciones registradas hoy")

def libro_diario():
    """Libro diario contable"""
    st.title("📚 Libro Diario")
    st.markdown("Registro cronológico de todas las transacciones")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Desde", st.session_state.transacciones['fecha'].min().date())
    with col2:
        fecha_fin = st.date_input("Hasta", st.session_state.transacciones['fecha'].max().date())
    
    # Filtrar
    df_filtrado = st.session_state.transacciones[
        (st.session_state.transacciones['fecha'].dt.date >= fecha_inicio) &
        (st.session_state.transacciones['fecha'].dt.date <= fecha_fin)
    ].sort_values('fecha', ascending=False)
    
    # Mostrar libro diario
    st.subheader("📋 Registro Contable")
    
    # Formato contable
    libro = df_filtrado.copy()
    libro['Debe'] = libro['gasto'].apply(lambda x: x if x > 0 else 0)
    libro['Haber'] = libro['ingreso'].apply(lambda x: x if x > 0 else 0)
    
    st.dataframe(
        libro[['fecha', 'concepto', 'Debe', 'Haber', 'categoria']],
        use_container_width=True,
        column_config={
            'fecha': st.column_config.DateColumn("Fecha"),
            'concepto': st.column_config.TextColumn("Concepto"),
            'Debe': st.column_config.NumberColumn("Debe", format="$%.2f"),
            'Haber': st.column_config.NumberColumn("Haber", format="$%.2f"),
            'categoria': st.column_config.TextColumn("Categoría")
        }
    )
    
    # Totales
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Debe", f"${df_filtrado['gasto'].sum():,.2f}")
    with col2:
        st.metric("Total Haber", f"${df_filtrado['ingreso'].sum():,.2f}")

def estado_financiero():
    """Estado de resultados"""
    st.title("📊 Estado de Resultados")
    st.markdown("Resumen de ingresos, gastos y utilidad del período")
    
    # Seleccionar período
    periodo = st.selectbox("Seleccionar período", ["Mes actual", "Trimestre", "Año", "Personalizado"])
    
    hoy = datetime.now()
    if periodo == "Mes actual":
        df_periodo = st.session_state.transacciones[
            st.session_state.transacciones['fecha'].dt.month == hoy.month
        ]
        titulo = f"Mes de {hoy.strftime('%B %Y')}"
    elif periodo == "Trimestre":
        trimestre = (hoy.month - 1) // 3 + 1
        df_periodo = st.session_state.transacciones[
            st.session_state.transacciones['fecha'].dt.quarter == trimestre
        ]
        titulo = f"Trimestre {trimestre} - {hoy.year}"
    elif periodo == "Año":
        df_periodo = st.session_state.transacciones[
            st.session_state.transacciones['fecha'].dt.year == hoy.year
        ]
        titulo = f"Año {hoy.year}"
    else:
        col1, col2 = st.columns(2)
        with col1:
            fecha_ini = st.date_input("Fecha inicio", datetime.now().replace(day=1))
        with col2:
            fecha_fin = st.date_input("Fecha fin", datetime.now())
        df_periodo = st.session_state.transacciones[
            (st.session_state.transacciones['fecha'].dt.date >= fecha_ini) &
            (st.session_state.transacciones['fecha'].dt.date <= fecha_fin)
        ]
        titulo = f"{fecha_ini.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}"
    
    # Calcular resultados
    ingresos = df_periodo['ingreso'].sum()
    gastos = df_periodo['gasto'].sum()
    utilidad = ingresos - gastos
    
    # Ingresos por categoría
    ingresos_cat = df_periodo[df_periodo['ingreso'] > 0].groupby('categoria')['ingreso'].sum()
    gastos_cat = df_periodo[df_periodo['gasto'] > 0].groupby('categoria')['gasto'].sum()
    
    # Mostrar estado de resultados
    st.subheader(f"Estado de Resultados - {titulo}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Ingresos")
        for cat, monto in ingresos_cat.items():
            st.write(f"- **{cat}:** ${monto:,.2f}")
        st.markdown(f"**Total Ingresos:** ${ingresos:,.2f}")
        
        st.markdown("### 📉 Gastos")
        for cat, monto in gastos_cat.items():
            st.write(f"- **{cat}:** ${monto:,.2f}")
        st.markdown(f"**Total Gastos:** ${gastos:,.2f}")
        
        st.markdown("---")
        if utilidad >= 0:
            st.markdown(f"### ✅ **Utilidad Neta: ${utilidad:,.2f}**")
        else:
            st.markdown(f"### ⚠️ **Pérdida Neta: ${utilidad:,.2f}**")
    
    with col2:
        fig = go.Figure(data=[
            go.Bar(name='Ingresos', x=list(ingresos_cat.index), y=list(ingresos_cat.values), marker_color='#00ff87'),
            go.Bar(name='Gastos', x=list(gastos_cat.index), y=list(gastos_cat.values), marker_color='#ff6b6b')
        ])
        fig.update_layout(barmode='group', title="Ingresos vs Gastos por Categoría")
        st.plotly_chart(fig, use_container_width=True)

def balance_general():
    """Balance general"""
    st.title("⚖️ Balance General")
    st.markdown("Situación financiera actual de tu negocio")
    
    # Calcular balances
    total_ingresos = st.session_state.transacciones['ingreso'].sum()
    total_gastos = st.session_state.transacciones['gasto'].sum()
    patrimonio = total_ingresos - total_gastos
    
    # Activos (efectivo disponible)
    activos = {
        'Efectivo': total_ingresos - total_gastos,
        'Cuentas por Cobrar': st.session_state.transacciones['ingreso'].tail(30).sum() * 0.3,
        'Total Activos': total_ingresos - total_gastos + (st.session_state.transacciones['ingreso'].tail(30).sum() * 0.3)
    }
    
    # Pasivos
    pasivos = {
        'Cuentas por Pagar': st.session_state.transacciones['gasto'].tail(30).sum() * 0.2,
        'Gastos Acumulados': st.session_state.transacciones['gasto'].tail(15).sum() * 0.1,
        'Total Pasivos': (st.session_state.transacciones['gasto'].tail(30).sum() * 0.2) + 
                         (st.session_state.transacciones['gasto'].tail(15).sum() * 0.1)
    }
    
    # Patrimonio
    patrimonio_calculado = activos['Total Activos'] - pasivos['Total Pasivos']
    
    # Mostrar balance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 ACTIVOS")
        for nombre, valor in activos.items():
            if nombre != 'Total Activos':
                st.write(f"- **{nombre}:** ${valor:,.2f}")
        st.markdown(f"### **Total Activos: ${activos['Total Activos']:,.2f}**")
    
    with col2:
        st.subheader("📋 PASIVOS")
        for nombre, valor in pasivos.items():
            if nombre != 'Total Pasivos':
                st.write(f"- **{nombre}:** ${valor:,.2f}")
        st.markdown(f"### **Total Pasivos: ${pasivos['Total Pasivos']:,.2f}**")
    
    st.markdown("---")
    st.subheader("🏢 PATRIMONIO")
    st.markdown(f"### **Patrimonio Neto: ${patrimonio_calculado:,.2f}**")
    
    # Ecuación contable
    st.info(f"📐 **Ecuación Contable:** Activos ({activos['Total Activos']:,.2f}) = Pasivos ({pasivos['Total Pasivos']:,.2f}) + Patrimonio ({patrimonio_calculado:,.2f})")

# ========== NAVEGACIÓN PRINCIPAL ==========
def main():
    inicializar_datos()
    
    # Sidebar con navegación visual
    with st.sidebar:
        st.image("https://via.placeholder.com/200x60?text=TU+AMIGO+CONTABLE", use_column_width=True)
        st.markdown("---")
        
        st.markdown("### 📊 Menú Principal")
        
        # Botones de navegación
        if st.button("🏠 Dashboard", use_container_width=True, type="primary"):
            st.session_state.page = "dashboard"
            st.rerun()
        
        if st.button("📝 Registro Diario", use_container_width=True):
            st.session_state.page = "registro"
            st.rerun()
        
        if st.button("📚 Libro Diario", use_container_width=True):
            st.session_state.page = "libro"
            st.rerun()
        
        if st.button("📊 Estado Financiero", use_container_width=True):
            st.session_state.page = "estado"
            st.rerun()
        
        if st.button("⚖️ Balance General", use_container_width=True):
            st.session_state.page = "balance"
            st.rerun()
        
        if st.button("🤖 Asistente IA", use_container_width=True):
            st.session_state.page = "asistente"
            st.rerun()
        
        st.markdown("---")
        
        # Métricas rápidas en sidebar
        metricas = calcular_metricas()
        st.markdown("### 📈 Resumen Rápido")
        st.metric("Ingresos", f"${metricas['total_ingresos']:,.0f}")
        st.metric("Gastos", f"${metricas['total_gastos']:,.0f}")
        st.metric("Balance", f"${metricas['balance']:,.0f}", 
                  delta=f"{metricas['rentabilidad']:.1f}%" if metricas['balance'] > 0 else None)
    
    # Mostrar página según selección
    if st.session_state.page == "dashboard":
        dashboard()
    elif st.session_state.page == "registro":
        registro_diario()
    elif st.session_state.page == "libro":
        libro_diario()
    elif st.session_state.page == "estado":
        estado_financiero()
    elif st.session_state.page == "balance":
        balance_general()
    elif st.session_state.page == "asistente":
        st.title("🤖 Asistente IA - Próximamente")
        st.info("""
        ### 🚧 En desarrollo
        
        El asistente con IA estará disponible pronto. Podrás:
        - 💬 Chatear con IA para resolver dudas contables
        - 📝 Traducir lenguaje cotidiano a registros contables
        - 📊 Obtener análisis financiero automático
        - 💡 Recibir consejos personalizados
        """)

if __name__ == "__main__":
    main()

# main.py - Asegúrate de tener estas importaciones
from asistente_ia import ContaAsistente
from memoria import MemoriaAsistente
from aprendizaje import SistemaAprendizaje
from logica_contable import obtener_logica_contable

# Inicializar todo
conta = ContaAsistente()
memoria = MemoriaAsistente()
aprendizaje = SistemaAprendizaje()
logica = obtener_logica_contable()
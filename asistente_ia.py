import streamlit as st
import pandas as pd
from datetime import datetime
import io

# ============================================
# 1. CONFIGURACIÓN INICIAL Y PALETA DE COLORES
# ============================================
st.set_page_config(
    page_title="tuamigocontable.com",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS para fuente, colores y diseño limpio
st.markdown("""
<style>
    /* Fuente profesional (Open Sans) y fondo claro */
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Open Sans', sans-serif;
        background-color: #f4f7f9; /* Fondo gris muy claro */
    }

    /* BARRA LATERAL (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa; /* Fondo lateral casi blanco */
        border-right: 1px solid #e9ecef;
    }
    
    /* Encabezado principal estilo 'MIRA TU BALANCE AQUÍ' */
    .main-header {
        background-color: #46637f; /* EL AZUL DE TU IMAGEN */
        color: white;
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .main-header h1 { font-size: 36px; margin-bottom: 5px; color: white !important; }
    .main-header p { font-size: 18px; opacity: 0.9; }

    /* TARJETAS DE MÉTRICAS (Dashboard) */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
        border-top: 5px solid #46637f; /* Borde superior azul */
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-3px); }
    .metric-value { font-size: 32px; font-weight: bold; color: #46637f; margin: 10px 0; }
    .metric-label { font-size: 16px; color: #6c757d; text-transform: uppercase; letter-spacing: 1px; }

    /* BOTONES PRIMARIOS (Azul de la imagen) */
    .stButton>button {
        background-color: #46637f !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        width: 100%;
    }
    .stButton>button:hover { background-color: #385169 !important; }

    /* Ocultar elementos de Streamlit por seguridad */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ============================================
# 2. SISTEMA DE LOGIN (Simulado)
# ============================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.session_state.logged_in = True

if not st.session_state.logged_in:
    st.markdown("""
    <div style="display:flex; justify-content:center; align-items:center; height:80vh;">
        <div style="background:white; padding:50px; border-radius:15px; box-shadow:0 10px 25px rgba(0,0,0,0.1); text-align:center; width: 400px;">
            <h1 style="color:#46637f; margin-bottom:10px;">📊 Welcome</h1>
            <p style="color:#6c757d; margin-bottom:30px;">tuamigocontable.com</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón de Login (Simulando "Entrar con Google")
    st.columns([1,2,1])[1].button("🔑 Entrar con Google (Acceso Demo)", on_click=login)
    st.stop() # Detiene la ejecución aquí si no está logueado

# ============================================
# 3. NAVEGACIÓN (Menú Lateral)
# ============================================
with st.sidebar:
    st.markdown(f'<div style="text-align:center; padding:10px 0;"><h2 style="color:#46637f;">tuamigocontable.com</h2><p style="color:#6c757d; font-size:12px;">v1.0.0</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Opciones de Menú
    opcion = st.radio(
        "📂 Menú Principal",
        ["🏠 Dashboard", "📄 Facturación y Registros", "📈 Reportes y Plantillas", "🏢 About Empresa", "💳 Suscripción y Pagos", "📞 Contáctanos", "🔐 Seguridad y Legal"]
    )
    
    st.markdown("---")
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()

# ============================================
# 4. LÓGICA DE PÁGINAS
# ============================================

# --------------------------------------------
# PÁGINA 1: DASHBOARD
# --------------------------------------------
if opcion == "🏠 Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>MIRA TU BALANCE AQUÍ</h1>
        <p>Tu resumen financiero inteligente</p>
    </div>
    """, unsafe_allow_html=True)

    # Métricas de ejemplo (Usando el estilo de tu imagen)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown('<div class="metric-card"><div class="metric-label">💰 Balance Actual</div><div class="metric-value">$4,500.00</div><small>Suma Neto</small></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="metric-card"><div class="metric-label">📉 Consumo del Mes</div><div class="metric-value">$1,250.00</div><small>Gastos Operativos</small></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="metric-card"><div class="metric-label">📊 Nuevos Reportes</div><div class="metric-value">3</div><small>Listos este mes</small></div>', unsafe_allow_html=True)
    with col4: st.markdown('<div class="metric-card"><div class="metric-label">🤖 Recomendaciones</div><div class="metric-value">5</div><small>Tips de IA pendientes</small></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Últimos Registros (Ejemplo de tabla)
    st.subheader("📋 Últimos Movimientos (Registro Diario)")
    df_demo = pd.DataFrame({
        "Fecha": ["2026-03-18", "2026-03-17", "2026-03-16"],
        "Detalle": ["Pago Servidor Web", "Venta Suscripción Anual", "Honorarios Contador"],
        "Tipo": ["Egreso", "Ingreso", "Egreso"],
        "Monto": ["$150.00", "$99.00", "$500.00"]
    })
    st.table(df_demo)

# --------------------------------------------
# PÁGINA 2: FACTURACIÓN Y REGISTROS
# --------------------------------------------
elif opcion == "📄 Facturación y Registros":
    st.title("📄 Generar Facturas y Registro Diario")
    
    col_a, col_b = st.columns(2)
    with col_a:
        with st.form("form_factura"):
            st.subheader("Generar Nueva Factura")
            st.text_input("Cliente")
            st.text_input("Concepto")
            st.number_input("Monto", min_value=0.0)
            st.form_submit_button("Crear Factura PDF")
            
    with col_b:
        with st.form("form_registro"):
            st.subheader("Registro Diario de Movimientos")
            st.date_input("Fecha")
            st.selectbox("Tipo", ["Ingreso", "Egreso"])
            st.text_input("Descripción")
            st.number_input("Valor", min_value=0.0)
            st.form_submit_button("Registrar Movimiento")

# --------------------------------------------
# PÁGINA 3: REPORTES Y PLANTILLAS
# --------------------------------------------
elif opcion == "📈 Reportes y Plantillas":
    st.title("📈 Reportes y Exportación de Plantillas")
    st.info("Estas plantillas profesionales se basan en los formatos estándar de tu carpeta 'tabla'.")
    
    c_rep1, c_rep2, c_rep3 = st.columns(3)
    
    # Generar Excel en memoria para descarga (como tu primer código)
    df_balance = pd.DataFrame({"Cuenta": ["Activo", "Pasivo", "Patrimonio"], "Suma": [10000, 5000, 5000]})
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_balance.to_excel(writer, index=False, sheet_name='Balance')
        
    c_rep1.download_button(label="📥 Descargar Balance General (Excel)", data=buffer, file_name="balance_general.xlsx", mime="application/vnd.ms-excel", use_container_width=True)
    c_rep2.button("📊 Generar Reporte Mensual PDF", use_container_width=True)
    c_rep3.button("📂 Exportar Plantilla NIIF", use_container_width=True)

# --------------------------------------------
# PÁGINA 4: ABOUT EMPRESA
# --------------------------------------------
elif opcion == "🏢 About Empresa":
    st.title("🏢 About tuamigocontable.com")
    
    col_ab1, col_ab2 = st.columns(2)
    with col_ab1:
        st.markdown("""
        ### Objetivos
        Ofrecer una solución contable inteligente y accesible para pequeñas empresas y autónomos, democratizando el acceso a la tecnología financiera.
        """)
    with col_ab2:
        st.markdown("""
        ### Misión
        Facilitar la gestión financiera diaria de nuestros usuarios mediante herramientas intuitivas y análisis avanzados, permitiéndoles enfocarse en crecer sus negocios.
        """)
        
    st.markdown("---")
    st.markdown("""
    ### Visión
    Ser la plataforma contable líder en Colombia, reconocida por su innovación, seguridad y su asistente IA que interpreta y simplifica la contabilidad.
    """)

# --------------------------------------------
# PÁGINA 5: SUSCRIPCIÓN Y PAGOS
# --------------------------------------------
elif opcion == "💳 Suscripción y Pagos":
    st.title("💳 Configuración de Suscripción")
    st.success("💳 Sistema de pagos seguro y global (Similar a Shein)")
    
    st.info("🎁 Comienza con tu prueba gratis de 7 días. Después, selecciona tu plan:")

    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📅 Mensual</div>
            <div class="metric-value">$10.00 <span style="font-size:12px;color:#6c757d;">/ mes</span></div>
            <p>Acceso completo, facturación ilimitada.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("💰 Pagar Mensual", key="btn_m")

    with col_p2:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 5px solid #28a745;">
            <div class="metric-label" style="color:#28a745;">💎 Trimestral</div>
            <div class="metric-value" style="color:#28a745;">$25.00 <span style="font-size:12px;color:#6c757d;">/ 3 meses</span></div>
            <p>Ahorra 17%, incluye reportes avanzados.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("💰 Pagar Trimestral", key="btn_t")

    with col_p3:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 5px solid #ffc107;">
            <div class="metric-label" style="color:#ffc107;">🏆 Anual</div>
            <div class="metric-value" style="color:#ffc107;">$99.00 <span style="font-size:12px;color:#6c757d;">/ año</span></div>
            <p>Ahorra 17.5%, soporte prioritario 24/7.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("💰 Pagar Anual", key="btn_a")

# --------------------------------------------
# PÁGINA 6: CONTÁCTANOS
# --------------------------------------------
elif opcion == "📞 Contáctanos":
    st.title("📞 Contáctanos")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.subheader("Envíanos un mensaje")
        st.text_input("Nombre")
        st.text_input("Email")
        st.text_area("Mensaje")
        st.button("Enviar Consulta")
        
    with col_c2:
        st.subheader("Nuestra Ubicación")
        st.markdown("""
        **Dirección:** Cedrito, Bogotá, Colombia  
        **Email:** soporte@tuamigocontable.com  
        **Teléfono:** +57 (1) 123-4567
        """)
        # GPS Ubicado en Cedrito, Bogotá (Simulado)
        df_map = pd.DataFrame({'lat': [4.72], 'lon': [-74.04]})
        st.map(df_map, zoom=13)

# --------------------------------------------
# PÁGINA 7: SEGURIDAD Y LEGAL
# --------------------------------------------
elif opcion == "🔐 Seguridad y Legal":
    st.title("🔐 Seguridad y Marco Legal")
    st.warning("🔒 Sistema protegido con seguro antihacker de última generación.")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["🔒 Política de Privacidad", "📄 Términos y Condiciones", "©️ Copy Write"])
    
    with tab1:
        st.subheader("Política de Privacidad")
        st.write("Tu privacidad es nuestra prioridad. En tuamigocontable.com, nos comprometemos a proteger tus datos personales y financieros...")
        st.markdown("[Ver política completa en PDF]")
        
    with tab2:
        st.subheader("Términos y Condiciones de Uso")
        st.write("Al utilizar tuamigocontable.com, aceptas nuestros términos y condiciones de servicio. Nuestra plataforma ofrece herramientas contables...")
        st.markdown("[Ver términos completos en PDF]")

    with tab3:
        st.subheader("Copyright ©")
        st.write(f"Todos los derechos reservados {datetime.now().year}, tuamigocontable.com.")
        st.write("Queda prohibida la reproducción total o parcial de esta plataforma.")

# ============================================
# 5. FOOTER (Copy Write Global)
# ============================================
st.markdown("---")
col_f1, col_f2 = st.columns([2,1])
with col_f1:
    st.caption(f"© {datetime.now().year} tuamigocontable.com - Todos los derechos reservados.")
with col_f2:
    st.caption("Hecho con ❤️ en Colombia | Contabilidad Inteligente")

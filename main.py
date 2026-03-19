import streamlit as st
import pandas as pd
import io

# 1. CONFIGURACIÓN Y ESTILO (Colores de tu imagen de referencia)
st.set_page_config(page_title="tuamigocontable.com", layout="wide")

st.markdown("""
<style>
    .main { background-color: #f4f7f9; }
    .header-style {
        background-color: #46637f;
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        border-bottom: 4px solid #46637f;
    }
    .val-in { color: #28a745; font-size: 30px; font-weight: bold; }
    .val-eg { color: #dc3545; font-size: 30px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. ENCABEZADO
st.markdown('<div class="header-style"><h1>MIRA TU BALANCE AQUÍ</h1><p>Gestión Inteligente de Registros Contables</p></div>', unsafe_allow_html=True)

# 3. MÉTRICAS PRINCIPALES
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="card">💵<br>Total Ingresos<br><span class="val-in">$5,450.00</span></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card">💳<br>Total Egresos<br><span class="val-eg">$4,980.00</span></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="card">⚖️<br>Balance Neto<br><span style="font-size:30px; font-weight:bold; color:#17a2b8;">$470.00</span></div>', unsafe_allow_html=True)

st.markdown("---")

# 4. BOTONES DE ACCIÓN (Reportes)
st.subheader("📊 Reportes y Exportación")
col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    if st.button("📈 Generar Balance General"):
        st.success("Analizando carpetas de 'contabilidad-general'...")

with col_b2:
    # Botón de descarga real
    df_descarga = pd.DataFrame({"Detalle": ["Ingresos", "Egresos"], "Monto": [5450, 4980]})
    buffer = io.BytesIO()
    df_descarga.to_excel(buffer, index=False)
    st.download_button(label="📥 Descargar Reporte Mes (Excel)", data=buffer, file_name="reporte_contable.xlsx")

with col_b3:
    if st.button("📑 Reporte Fiscal"):
        st.info("Consultando carpeta 'fiscal'...")

# 5. EL ASISTENTE (Motor de interpretación)
st.sidebar.markdown("## 🤖 CONTA IA")
st.sidebar.write("Estoy listo para analizar tus carpetas de registro.")

if "chat" not in st.session_state:
    st.session_state.chat = []

for m in st.session_state.chat:
    with st.sidebar.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.sidebar.chat_input("¿Qué quieres saber de tus cuentas?"):
    st.session_state.chat.append({"role": "user", "content": prompt})
    
    # Lógica de interpretación simple (mientras conectas la API)
    if "balance" in prompt.lower():
        res = "Según tus registros de este mes, tu balance es de $470.00. Tienes un margen de seguridad del 8.6%."
    elif "fiscal" in prompt.lower():
        res = "Revisando la carpeta 'fiscal'... no olvides subir los soportes de IVA de esta semana."
    else:
        res = "Hecho. Estoy procesando esa información con tus tablas contables."
        
    st.session_state.chat.append({"role": "assistant", "content": res})
    st.sidebar.rerun()

# 6. TABLA DE REGISTROS
st.subheader("📋 Últimos Registros")
st.write("Datos extraídos de tu carpeta 'libro-de-registro-de-contabilidad'")
# Simulación de carga de datos
data = pd.DataFrame({
    "Fecha": ["2026-03-10", "2026-03-12"],
    "Carpeta": ["Ingresos", "Egresos"],
    "Monto": [1200, 500],
    "Estado": ["Contabilizado", "Pendiente"]
})
st.dataframe(data, use_container_width=True)

import os

# Función para que la IA "vea" qué archivos tienes
def listar_documentos(carpeta):
    try:
        archivos = os.listdir(carpeta)
        return archivos if archivos else ["La carpeta está vacía"]
    except FileNotFoundError:
        return ["Carpeta no encontrada"]

# --- En la sección de la IA en el sidebar ---
if prompt := st.sidebar.chat_input("¿Qué hay en mis archivos?"):
    st.session_state.chat.append({"role": "user", "content": prompt})
    
    # Ejemplo de interpretación de carpetas reales
    if "fiscal" in prompt.lower():
        docs = listar_documentos("fiscal")
        res = f"En tu carpeta 'fiscal' encontré: {', '.join(docs)}. ¿Quieres que analice alguno?"
    elif "registro" in prompt.lower():
        docs = listar_documentos("libro-de-registro-de-contabilidad")
        res = f"Tienes estos registros guardados: {', '.join(docs)}."
    else:
        res = "Entendido. Estoy listo para procesar los datos de tus subcarpetas."
    
    st.session_state.chat.append({"role": "assistant", "content": res})

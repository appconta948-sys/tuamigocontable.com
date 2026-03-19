import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="tuamigocontable.com", layout="wide")

# 2. ENCABEZADO Y TÍTULOS (Basado en tu primer diseño funcional)
st.title("📊 Reportes y Exportación")

# 3. BOTONES DE ACCIÓN
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📈 Generar Balance General"):
        st.write("Procesando balance...")

with col2:
    if st.button("📥 Descargar Reporte Mes (Excel)"):
        st.write("Preparando descarga...")

with col3:
    if st.button("📑 Reporte Fiscal"):
        st.write("Consultando carpeta fiscal...")

st.markdown("---")

# 4. VISUALIZACIÓN DE ARCHIVOS (Lo que ya te funcionaba)
st.subheader("📋 Últimos Registros")
st.write("Archivos detectados en tus carpetas de GitHub:")

# Esta es la lógica que lee tus carpetas reales
try:
    # Intenta leer la carpeta que ya tienes en tu repo
    archivos = os.listdir("libro-de-registro-de-contabilidad")
    if archivos:
        st.info(f"Archivos encontrados: {', '.join(archivos)}")
    else:
        st.warning("La carpeta 'libro-de-registro-de-contabilidad' está vacía.")
except Exception as e:
    st.error("No se pudo acceder a la carpeta de registros. Verifica que el nombre sea exacto en GitHub.")

# 5. TABLA DE DATOS (Métrica de balance que tenías originalmente)
st.markdown("---")
st.subheader("⚖️ Estado de Cuenta Actual")
data_original = pd.DataFrame({
    "Detalle": ["Total Ingresos", "Total Egresos", "Balance Neto"],
    "Monto": ["$5,450.00", "$4,980.00", "$470.00"]
})
st.table(data_original)

# 6. ASISTENTE (Versión simple en el sidebar)
with st.sidebar:
    st.header("🤖 Asistente Contable")
    st.write("Sistema conectado a tus carpetas.")
    prompt = st.chat_input("¿Qué deseas consultar?")
    if prompt:
        st.write(f"Has consultado: {prompt}")
        st.caption("Buscando en tus archivos .md...")

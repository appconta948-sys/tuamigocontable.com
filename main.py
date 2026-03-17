# ============================================
# CONTA APP - VERSIÓN STREAMLIT
# Archivo: main.py
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import hashlib
import os
import google.generativeai as genai

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

class ContaInteligente:
    def __init__(self, conta=None, puc=None, libro=None):
        self.conta = conta
        self.puc = puc
        self.libro = libro
        self.disponible = False
        try:
            self.api_key = st.secrets["GEMINI_API_KEY"]
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                self.disponible = True
        except Exception as e:
            self.disponible = False
    
    def interpretar_mensaje(self, mensaje):
        if not self.disponible:
            return {"error": "IA no disponible"}
        prompt = f"""Eres un asistente contable. Interpreta este mensaje: "{mensaje}". 
        Devuelve JSON con tipo, monto, tercero, producto, cantidad."""
        try:
            response = self.model.generate_content(prompt)
            return {"exito": True, "respuesta": response.text}
        except Exception as e:
            return {"error": str(e)}

# ============================================
# INICIALIZAR SISTEMA (con caché)
# ============================================
@st.cache_resource
def init_system():
    conta = Conta("Colombia", "COP", 2)
    puc = PUCInteligente(conta, "Colombia")
    libro = LibroDiario(conta, puc)
    ia = ContaInteligente(conta, puc, libro)
    
    # Agregar datos de ejemplo si no hay
    if len(libro.asientos) == 0:
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
    
    return conta, puc, libro, ia

# Cargar sistema
if 'system_loaded' not in st.session_state:
    st.session_state.conta, st.session_state.puc, st.session_state.libro, st.session_state.ia = init_system()
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

col1.metric("Ingresos del Mes", f"${ingresos:,.0f}")
col2.metric("Egresos del Mes", f"${egresos:,.0f}")
col3.metric("Balance del Mes", f"${balance:,.0f}")

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

# Chat con IA
st.subheader("🤖 Asistente IA")
mensaje = st.chat_input("Pregúntale algo a la IA (ej: 'me deben 2000 por 4 cajas de papa')")
if mensaje:
    if st.session_state.ia.disponible:
        with st.spinner("Pensando..."):
            respuesta = st.session_state.ia.interpretar_mensaje(mensaje)
            st.json(respuesta)
    else:
        st.warning("⚠️ IA no disponible. Verifica la API key en Secrets.")

# Exportar datos (opcional)
with st.expander("📥 Exportar datos"):
    st.download_button(
        label="Descargar asientos como JSON",
        data=json.dumps(st.session_state.libro.asientos, indent=2),
        file_name=f"asientos_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )

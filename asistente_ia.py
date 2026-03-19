import os
import streamlit as st

class ContaIA:
    def __init__(self):
        self.nombre = "Conta IA"
        self.empresa = "tuamigocontable.com"

    def analizar_archivos_locales(self):
        # Esta función escanea tus carpetas de GitHub
        carpetas = ['fiscal', 'contabilidad-general', 'libro-de-registro-de-contabilidad']
        resumen = {}
        for c in carpetas:
            try:
                resumen[c] = os.listdir(c)
            except:
                resumen[c] = []
        return resumen

    def responder(self, consulta, datos_dashboard):
        # Aquí es donde la IA "piensa"
        consulta = consulta.lower()
        
        if "balance" in consulta:
            return f"Tu balance actual es de {datos_dashboard['balance']}. Revisando tus libros, el flujo es estable."
        
        if "archivos" in consulta or "libros" in consulta:
            archivos = self.analizar_archivos_locales()
            return f"He detectado archivos en tus libros: {archivos.get('libro-de-registro-de-contabilidad', 'Ninguno')}."
            
        return "Soy tu asistente contable. Puedo ayudarte a interpretar tus balances o buscar documentos en tus carpetas fiscales."

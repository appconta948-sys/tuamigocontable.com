# aprendizaje.py - Sistema de aprendizaje continuo
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import numpy as np
from collections import Counter

class SistemaAprendizaje:
    """Sistema de aprendizaje continuo para el asistente IA"""
    
    def __init__(self, usuario_id="default"):
        self.usuario_id = usuario_id
        self.inicializar_aprendizaje()
    
    def inicializar_aprendizaje(self):
        """Inicializa todas las estructuras de aprendizaje"""
        
        # Base de conocimiento del usuario
        if f'conocimiento_{self.usuario_id}' not in st.session_state:
            st.session_state[f'conocimiento_{self.usuario_id}'] = {
                'terminos_preferidos': {},  # Términos que el usuario prefiere usar
                'categorias_personalizadas': {},  # Categorías creadas por usuario
                'frases_comunes': {},  # Frases que el usuario usa frecuentemente
                'correcciones': [],  # Correcciones que ha hecho el usuario
                'feedback': []  # Feedback de respuestas
            }
        
        # Modelo de aprendizaje
        if f'modelo_aprendizaje_{self.usuario_id}' not in st.session_state:
            st.session_state[f'modelo_aprendizaje_{self.usuario_id}'] = {
                'patrones_ingreso': {},  # Patrones aprendidos de ingresos
                'patrones_gasto': {},  # Patrones aprendidos de gastos
                'pesos_aprendidos': {},  # Pesos para clasificación
                'ejemplos_entrenamiento': [],  # Ejemplos para mejorar
                'metricas_rendimiento': {
                    'precision': 0.85,  # Precisión actual
                    'total_interacciones': 0,
                    'correcciones_recibidas': 0,
                    'feedback_positivo': 0,
                    'feedback_negativo': 0
                }
            }
        
        # Memoria de errores
        if f'errores_{self.usuario_id}' not in st.session_state:
            st.session_state[f'errores_{self.usuario_id}'] = {
                'errores_comunes': [],  # Errores frecuentes
                'mejoras_aplicadas': [],  # Mejoras implementadas
                'ultima_mejora': None
            }
    
    def aprender_de_interaccion(self, mensaje_usuario, respuesta_ia, feedback=None, correccion=None):
        """Aprende de cada interacción con el usuario"""
        
        # Clasificar el tipo de interacción
        tipo = self.clasificar_mensaje(mensaje_usuario)
        
        # Extraer patrones del mensaje
        patrones = self.extraer_patrones(mensaje_usuario)
        
        # Guardar en conocimiento
        conocimiento = st.session_state[f'conocimiento_{self.usuario_id}']
        modelo = st.session_state[f'modelo_aprendizaje_{self.usuario_id}']
        
        # Actualizar frases comunes
        frase_key = mensaje_usuario[:50]
        if frase_key in conocimiento['frases_comunes']:
            conocimiento['frases_comunes'][frase_key] += 1
        else:
            conocimiento['frases_comunes'][frase_key] = 1
        
        # Aprender de correcciones
        if correccion:
            self.aprender_de_correccion(mensaje_usuario, correccion)
            modelo['metricas_rendimiento']['correcciones_recibidas'] += 1
        
        # Aprender de feedback
        if feedback:
            self.aprender_de_feedback(feedback, respuesta_ia)
            if feedback == "positivo":
                modelo['metricas_rendimiento']['feedback_positivo'] += 1
            elif feedback == "negativo":
                modelo['metricas_rendimiento']['feedback_negativo'] += 1
        
        # Actualizar métricas
        modelo['metricas_rendimiento']['total_interacciones'] += 1
        
        # Actualizar precisión
        precision = (modelo['metricas_rendimiento']['feedback_positivo'] / 
                    max(1, modelo['metricas_rendimiento']['total_interacciones']))
        modelo['metricas_rendimiento']['precision'] = precision
        
        # Guardar ejemplo de entrenamiento
        if feedback == "positivo" or correccion:
            ejemplo = {
                'mensaje': mensaje_usuario,
                'respuesta': respuesta_ia,
                'correccion': correccion,
                'feedback': feedback,
                'fecha': datetime.now()
            }
            modelo['ejemplos_entrenamiento'].append(ejemplo)
            # Mantener solo los últimos 100 ejemplos
            if len(modelo['ejemplos_entrenamiento']) > 100:
                modelo['ejemplos_entrenamiento'] = modelo['ejemplos_entrenamiento'][-100:]
    
    def clasificar_mensaje(self, mensaje):
        """Clasifica el mensaje usando patrones aprendidos"""
        mensaje_lower = mensaje.lower()
        
        # Patrones aprendidos de ingresos
        patrones_ingreso = st.session_state[f'modelo_aprendizaje_{self.usuario_id}']['patrones_ingreso']
        patrones_gasto = st.session_state[f'modelo_aprendizaje_{self.usuario_id}']['patrones_gasto']
        
        # Verificar patrones aprendidos primero
        for patron in patrones_ingreso:
            if patron in mensaje_lower:
                return 'ingreso'
        
        for patron in patrones_gasto:
            if patron in mensaje_lower:
                return 'gasto'
        
        # Patrones por defecto
        if any(p in mensaje_lower for p in ['pagaron', 'recibí', 'gané', 'vendí']):
            return 'ingreso'
        elif any(p in mensaje_lower for p in ['compré', 'gasté', 'pagué']):
            return 'gasto'
        else:
            return 'consulta'
    
    def extraer_patrones(self, mensaje):
        """Extrae patrones del mensaje para aprendizaje"""
        palabras = mensaje.lower().split()
        
        # Extraer palabras clave
        palabras_clave = [p for p in palabras if len(p) > 3]
        
        # Extraer números y montos
        import re
        numeros = re.findall(r'\d+', mensaje)
        montos = [int(n) for n in numeros] if numeros else []
        
        # Extraer moneda
        moneda = "USD"
        if "peso" in mensaje.lower() or "mil" in mensaje.lower():
            moneda = "COP"
        elif "dólar" in mensaje.lower() or "dolar" in mensaje.lower():
            moneda = "USD"
        
        return {
            'palabras_clave': palabras_clave,
            'montos': montos,
            'moneda': moneda,
            'longitud': len(mensaje),
            'tiene_numeros': len(numeros) > 0
        }
    
    def aprender_de_correccion(self, mensaje_original, correccion):
        """Aprende de las correcciones del usuario"""
        
        conocimiento = st.session_state[f'conocimiento_{self.usuario_id}']
        modelo = st.session_state[f'modelo_aprendizaje_{self.usuario_id}']
        
        # Guardar corrección
        correccion_data = {
            'mensaje': mensaje_original,
            'correccion': correccion,
            'fecha': datetime.now()
        }
        conocimiento['correcciones'].append(correccion_data)
        
        # Analizar qué aprendió
        if 'ingreso' in correccion.lower() and 'gasto' not in correccion.lower():
            # Aprender que este tipo de mensaje es un ingreso
            patrones_ingreso = modelo['patrones_ingreso']
            palabras_clave = mensaje_original.lower().split()
            for palabra in palabras_clave:
                if len(palabra) > 3:
                    patrones_ingreso[palabra] = patrones_ingreso.get(palabra, 0) + 1
        
        elif 'gasto' in correccion.lower():
            # Aprender que es un gasto
            patrones_gasto = modelo['patrones_gasto']
            palabras_clave = mensaje_original.lower().split()
            for palabra in palabras_clave:
                if len(palabra) > 3:
                    patrones_gasto[palabra] = patrones_gasto.get(palabra, 0) + 1
        
        # Registrar mejora
        errores = st.session_state[f'errores_{self.usuario_id}']
        errores['mejoras_aplicadas'].append({
            'tipo': 'correccion',
            'descripcion': f"Aprendí que '{mensaje_original[:50]}' es {correccion}",
            'fecha': datetime.now()
        })
        errores['ultima_mejora'] = datetime.now()
    
    def aprender_de_feedback(self, feedback, respuesta):
        """Aprende del feedback del usuario"""
        
        conocimiento = st.session_state[f'conocimiento_{self.usuario_id}']
        
        feedback_data = {
            'respuesta': respuesta,
            'feedback': feedback,
            'fecha': datetime.now()
        }
        conocimiento['feedback'].append(feedback_data)
        
        # Si es feedback negativo, analizar qué salió mal
        if feedback == "negativo":
            self.analizar_error(respuesta)
    
    def analizar_error(self, respuesta):
        """Analiza errores para mejorar"""
        
        errores = st.session_state[f'errores_{self.usuario_id}']
        
        # Buscar patrones de error
        error_comun = None
        if "balance" in respuesta.lower() and "error" in respuesta.lower():
            error_comun = "Error en cálculo de balance"
        elif "no entendí" in respuesta.lower():
            error_comun = "No entendió el mensaje del usuario"
        
        if error_comun:
            errores['errores_comunes'].append({
                'error': error_comun,
                'respuesta': respuesta,
                'fecha': datetime.now()
            })
    
    def personalizar_categoria(self, mensaje, categoria_asignada):
        """Aprende categorías personalizadas del usuario"""
        
        conocimiento = st.session_state[f'conocimiento_{self.usuario_id}']
        
        # Extraer palabras clave del mensaje
        palabras = mensaje.lower().split()
        palabras_clave = [p for p in palabras if len(p) > 3]
        
        # Asociar palabras con categoría
        for palabra in palabras_clave:
            if palabra not in conocimiento['categorias_personalizadas']:
                conocimiento['categorias_personalizadas'][palabra] = {}
            
            if categoria_asignada not in conocimiento['categorias_personalizadas'][palabra]:
                conocimiento['categorias_personalizadas'][palabra][categoria_asignada] = 0
            conocimiento['categorias_personalizadas'][palabra][categoria_asignada] += 1
        
        return f"Aprendí que '{palabras_clave[0] if palabras_clave else 'esto'}' normalmente es {categoria_asignada}"
    
    def predecir_categoria(self, mensaje):
        """Predice la categoría basada en aprendizaje previo"""
        
        conocimiento = st.session_state[f'conocimiento_{self.usuario_id}']
        
        palabras = mensaje.lower().split()
        palabras_clave = [p for p in palabras if len(p) > 3]
        
        # Contar votos para cada categoría
        votos = {}
        for palabra in palabras_clave:
            if palabra in conocimiento['categorias_personalizadas']:
                for categoria, peso in conocimiento['categorias_personalizadas'][palabra].items():
                    votos[categoria] = votos.get(categoria, 0) + peso
        
        if votos:
            # Devolver la categoría con más votos
            return max(votos, key=votos.get)
        
        return None
    
    def recomendar_mejora(self):
        """Recomienda mejoras basadas en aprendizaje"""
        
        modelo = st.session_state[f'modelo_aprendizaje_{self.usuario_id}']
        errores = st.session_state[f'errores_{self.usuario_id}']
        
        recomendaciones = []
        
        # Si hay muchos errores, recomendar revisión
        if modelo['metricas_rendimiento']['precision'] < 0.7:
            recomendaciones.append("📊 La precisión está baja. ¿Quieres revisar algunas transacciones pasadas para corregirlas?")
        
        # Si hay muchos errores comunes, recomendar solución
        if len(errores['errores_comunes']) > 5:
            errores_frecuentes = Counter([e['error'] for e in errores['errores_comunes']])
            error_mas_comun = errores_frecuentes.most_common(1)[0]
            recomendaciones.append(f"⚠️ Detecto que {error_mas_comun[0]} frecuentemente. ¿Quieres que ajuste mi configuración?")
        
        # Recomendar crear categorías personalizadas
        if len(conocimiento['categorias_personalizadas']) < 3 and len(modelo['ejemplos_entrenamiento']) > 10:
            recomendaciones.append("💡 Puedes crear categorías personalizadas para organizar mejor tus finanzas")
        
        return recomendaciones
    
    def obtener_estadisticas_aprendizaje(self):
        """Obtiene estadísticas del aprendizaje"""
        
        modelo = st.session_state[f'modelo_aprendizaje_{self.usuario_id}']
        conocimiento = st.session_state[f'conocimiento_{self.usuario_id}']
        errores = st.session_state[f'errores_{self.usuario_id}']
        
        return {
            'precision_actual': modelo['metricas_rendimiento']['precision'],
            'total_interacciones': modelo['metricas_rendimiento']['total_interacciones'],
            'correcciones': modelo['metricas_rendimiento']['correcciones_recibidas'],
            'feedback_positivo': modelo['metricas_rendimiento']['feedback_positivo'],
            'feedback_negativo': modelo['metricas_rendimiento']['feedback_negativo'],
            'patrones_aprendidos': {
                'ingresos': len(modelo['patrones_ingreso']),
                'gastos': len(modelo['patrones_gasto'])
            },
            'categorias_personalizadas': len(conocimiento['categorias_personalizadas']),
            'errores_comunes': len(errores['errores_comunes']),
            'mejoras_aplicadas': len(errores['mejoras_aplicadas'])
        }
    
    def exportar_conocimiento(self):
        """Exporta el conocimiento aprendido para análisis"""
        
        conocimiento = st.session_state[f'conocimiento_{self.usuario_id}']
        modelo = st.session_state[f'modelo_aprendizaje_{self.usuario_id}']
        
        return {
            'conocimiento': conocimiento,
            'modelo': modelo,
            'fecha_exportacion': datetime.now()
        }
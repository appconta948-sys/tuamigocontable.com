# memoria.py - Archivo separado para la lógica de memoria
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

class MemoriaAsistente:
    """Sistema de memoria a corto, mediano y largo plazo"""
    
    def __init__(self, usuario_id="default"):
        self.usuario_id = usuario_id
        self.inicializar_memoria()
    
    def inicializar_memoria(self):
        """Inicializa todas las estructuras de memoria"""
        
        # MEMORIA A CORTO PLAZO (últimos 7 días)
        if f'memoria_corto_plazo_{self.usuario_id}' not in st.session_state:
            st.session_state[f'memoria_corto_plazo_{self.usuario_id}'] = {
                'ultimas_interacciones': [],  # Últimas 10 conversaciones
                'transacciones_recientes': [],  # Últimos 7 días
                'contexto_actual': None,
                'pendientes': []  # Tareas pendientes
            }
        
        # MEMORIA A MEDIANO PLAZO (últimos 3 meses)
        if f'memoria_mediano_plazo_{self.usuario_id}' not in st.session_state:
            st.session_state[f'memoria_mediano_plazo_{self.usuario_id}'] = {
                'patrones_gastos': {},  # Patrones de gasto detectados
                'patrones_ingresos': {},  # Patrones de ingreso detectados
                'objetivos': [],  # Objetivos financieros
                'alertas': [],  # Alertas configuradas
                'aprendizajes': []  # Cosas que ha aprendido del usuario
            }
        
        # MEMORIA A LARGO PLAZO (histórico completo)
        if f'memoria_largo_plazo_{self.usuario_id}' not in st.session_state:
            st.session_state[f'memoria_largo_plazo_{self.usuario_id}'] = {
                'historial_completo': [],  # Resumen mensual histórico
                'tendencias': {},  # Tendencias detectadas
                'logros': [],  # Logros financieros
                'consejos_anteriores': []  # Consejos ya dados
            }
        
        # MEMORIA SEMÁNTICA (conocimiento del usuario)
        if f'memoria_semantica_{self.usuario_id}' not in st.session_state:
            st.session_state[f'memoria_semantica_{self.usuario_id}'] = {
                'preferencias': {},  # Preferencias del usuario
                'nivel_conocimiento': 'principiante',  # Principiante, intermedio, avanzado
                'terminos_aprendidos': [],  # Términos contables que ya conoce
                'preguntas_frecuentes': []  # Preguntas que hace seguido
            }
    
    def guardar_interaccion(self, mensaje_usuario, respuesta_asistente):
        """Guarda cada interacción en memoria a corto plazo"""
        interaccion = {
            'fecha': datetime.now(),
            'mensaje': mensaje_usuario,
            'respuesta': respuesta_asistente,
            'tipo': self.clasificar_interaccion(mensaje_usuario)
        }
        
        memoria = st.session_state[f'memoria_corto_plazo_{self.usuario_id}']
        memoria['ultimas_interacciones'].append(interaccion)
        
        # Mantener solo las últimas 20 interacciones
        if len(memoria['ultimas_interacciones']) > 20:
            memoria['ultimas_interacciones'] = memoria['ultimas_interacciones'][-20:]
    
    def clasificar_interaccion(self, mensaje):
        """Clasifica el tipo de interacción"""
        mensaje_lower = mensaje.lower()
        
        if any(p in mensaje_lower for p in ['pagaron', 'recibí', 'gané', 'vendí', 'ingreso']):
            return 'registro_ingreso'
        elif any(p in mensaje_lower for p in ['compré', 'gasté', 'pagué', 'gasto']):
            return 'registro_gasto'
        elif any(p in mensaje_lower for p in ['balance', 'cómo voy', 'resumen']):
            return 'consulta_balance'
        elif any(p in mensaje_lower for p in ['objetivo', 'meta', 'quiero ahorrar']):
            return 'objetivo'
        elif any(p in mensaje_lower for p in ['recordar', 'acordar', 'avísame']):
            return 'alerta'
        else:
            return 'consulta_general'
    
    def analizar_patrones(self):
        """Analiza patrones en los datos para memoria mediano plazo"""
        if st.session_state.transacciones.empty:
            return
        
        df = st.session_state.transacciones
        df['mes'] = df['fecha'].dt.to_period('M')
        
        # Patrones de gastos por categoría
        patrones_gastos = df[df['gasto'] > 0].groupby(['mes', 'categoria'])['gasto'].sum().to_dict()
        
        # Patrones de ingresos
        patrones_ingresos = df[df['ingreso'] > 0].groupby(['mes'])['ingreso'].sum().to_dict()
        
        # Detectar anomalías
        promedio_gastos = df[df['gasto'] > 0]['gasto'].mean()
        gastos_mayores = df[df['gasto'] > promedio_gastos * 1.5]
        
        memoria_mediano = st.session_state[f'memoria_mediano_plazo_{self.usuario_id}']
        memoria_mediano['patrones_gastos'] = patrones_gastos
        memoria_mediano['patrones_ingresos'] = patrones_ingresos
        
        # Generar alertas si hay gastos inusuales
        if not gastos_mayores.empty:
            for _, gasto in gastos_mayores.iterrows():
                alerta = {
                    'fecha': gasto['fecha'],
                    'concepto': gasto['concepto_contable'],
                    'monto': gasto['gasto'],
                    'tipo': 'gasto_inusual'
                }
                if alerta not in memoria_mediano['alertas']:
                    memoria_mediano['alertas'].append(alerta)
    
    def actualizar_memoria_largo_plazo(self):
        """Actualiza la memoria a largo plazo mensualmente"""
        if st.session_state.transacciones.empty:
            return
        
        df = st.session_state.transacciones
        ultimo_mes = df['fecha'].max().to_period('M')
        
        memoria_largo = st.session_state[f'memoria_largo_plazo_{self.usuario_id}']
        
        # Verificar si ya tenemos este mes en histórico
        meses_registrados = [h.get('mes') for h in memoria_largo['historial_completo']]
        
        if ultimo_mes not in meses_registrados:
            # Resumen del mes
            df_mes = df[df['fecha'].dt.to_period('M') == ultimo_mes]
            resumen_mes = {
                'mes': str(ultimo_mes),
                'ingresos': df_mes['ingreso'].sum(),
                'gastos': df_mes['gasto'].sum(),
                'balance': df_mes['ingreso'].sum() - df_mes['gasto'].sum(),
                'num_transacciones': len(df_mes)
            }
            memoria_largo['historial_completo'].append(resumen_mes)
        
        # Actualizar tendencias
        if len(memoria_largo['historial_completo']) >= 3:
            ultimos_3 = memoria_largo['historial_completo'][-3:]
            tendencia_ingresos = 'creciente' if ultimos_3[-1]['ingresos'] > ultimos_3[-2]['ingresos'] else 'decreciente'
            tendencia_gastos = 'creciente' if ultimos_3[-1]['gastos'] > ultimos_3[-2]['gastos'] else 'decreciente'
            
            memoria_largo['tendencias'] = {
                'ingresos': tendencia_ingresos,
                'gastos': tendencia_gastos,
                'ultima_actualizacion': datetime.now()
            }
    
    def recordar_contexto(self):
        """Recupera contexto relevante para la conversación actual"""
        contexto = {
            'corto_plazo': [],
            'mediano_plazo': [],
            'largo_plazo': []
        }
        
        # Contexto de corto plazo: última interacción
        memoria_corto = st.session_state[f'memoria_corto_plazo_{self.usuario_id}']
        if memoria_corto['ultimas_interacciones']:
            contexto['corto_plazo'].append(memoria_corto['ultimas_interacciones'][-1])
        
        # Contexto de mediano plazo: tareas pendientes y objetivos
        memoria_mediano = st.session_state[f'memoria_mediano_plazo_{self.usuario_id}']
        if memoria_mediano['pendientes']:
            contexto['mediano_plazo'].append({'pendientes': memoria_mediano['pendientes']})
        if memoria_mediano['objetivos']:
            contexto['mediano_plazo'].append({'objetivos': memoria_mediano['objetivos']})
        
        # Contexto de largo plazo: logros y tendencias
        memoria_largo = st.session_state[f'memoria_largo_plazo_{self.usuario_id}']
        if memoria_largo['logros']:
            contexto['largo_plazo'].append({'logros': memoria_largo['logros']})
        if memoria_largo['tendencias']:
            contexto['largo_plazo'].append({'tendencias': memoria_largo['tendencias']})
        
        return contexto
    
    def establecer_objetivo(self, objetivo, monto, plazo):
        """Establece un objetivo financiero"""
        objetivo_data = {
            'descripcion': objetivo,
            'monto': monto,
            'plazo': plazo,
            'fecha_inicio': datetime.now(),
            'progreso': 0,
            'completado': False
        }
        
        memoria_mediano = st.session_state[f'memoria_mediano_plazo_{self.usuario_id}']
        memoria_mediano['objetivos'].append(objetivo_data)
        
        return f"✅ He guardado tu objetivo: ahorrar ${monto} para {objetivo} en {plazo}"
    
    def crear_alerta(self, condicion, mensaje):
        """Crea una alerta para el usuario"""
        alerta = {
            'condicion': condicion,
            'mensaje': mensaje,
            'fecha_creacion': datetime.now(),
            'activa': True
        }
        
        memoria_mediano = st.session_state[f'memoria_mediano_plazo_{self.usuario_id}']
        memoria_mediano['alertas'].append(alerta)
        
        return f"✅ Te avisaré cuando: {condicion}"
    
    def verificar_alertas(self):
        """Verifica si hay alertas que activar"""
        alertas_activas = []
        memoria_mediano = st.session_state[f'memoria_mediano_plazo_{self.usuario_id}']
        
        if st.session_state.transacciones.empty:
            return alertas_activas
        
        df = st.session_state.transacciones
        total_gastos = df['gasto'].sum()
        total_ingresos = df['ingreso'].sum()
        
        for alerta in memoria_mediano['alertas']:
            if not alerta['activa']:
                continue
            
            condicion = alerta['condicion'].lower()
            
            if 'gasto' in condicion and '100' in condicion and total_gastos > 100:
                alerta['activa'] = False
                alertas_activas.append(alerta['mensaje'])
            
            elif 'ingreso' in condicion and '500' in condicion and total_ingresos > 500:
                alerta['activa'] = False
                alertas_activas.append(alerta['mensaje'])
        
        return alertas_activas
    
    def generar_recomendaciones(self):
        """Genera recomendaciones basadas en la memoria"""
        recomendaciones = []
        memoria_largo = st.session_state[f'memoria_largo_plazo_{self.usuario_id}']
        memoria_mediano = st.session_state[f'memoria_mediano_plazo_{self.usuario_id}']
        
        # Recomendaciones basadas en tendencias
        if memoria_largo['tendencias'].get('gastos') == 'creciente':
            recomendaciones.append("📈 Tus gastos han aumentado en los últimos meses. ¿Quieres revisar en qué categorías?")
        
        # Recomendaciones basadas en objetivos
        objetivos_activos = [o for o in memoria_mediano['objetivos'] if not o['completado']]
        if objetivos_activos:
            recomendaciones.append(f"🎯 Recuerda tu objetivo: {objetivos_activos[0]['descripcion']}")
        
        # Recomendaciones basadas en patrones
        if st.session_state.transacciones.empty:
            return recomendaciones
        
        df = st.session_state.transacciones
        if not df.empty:
            categoria_max_gasto = df[df['gasto'] > 0].groupby('categoria')['gasto'].sum().idxmax()
            recomendaciones.append(f"💡 Tu mayor gasto es en {categoria_max_gasto}. ¿Quieres consejos para optimizarlo?")
        
        return recomendaciones
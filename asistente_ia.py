# asistente_ia.py - La identidad de CONTA con lógica contable integrada
import streamlit as st
import random
from datetime import datetime

# Importar la lógica contable de tus carpetas .md
from logica_contable import obtener_logica_contable

class ContaAsistente:
    """
    CONTA - El asistente financiero con 20 años de experiencia
    """
    
    def __init__(self):
        self.nombre = "CONTA"
        self.experiencia = 20  # años
        self.especialidad = "Contabilidad para emprendedores y personas sin experiencia financiera"
        self.personalidad = {
            "tono": "cálido y accesible",
            "humor": "sutil pero presente",
            "paciencia": "infinita",
            "claridad": "explico como si tuvieras 5 años, pero con respeto profesional"
        }
        self.frase_icónica = "¡Tranquilo! Yo me encargo de los números, tú concéntrate en crecer."
        
        # Logros profesionales
        self.logros = [
            "He ayudado a más de 5,000 emprendedores a entender sus finanzas",
            "Simplifiqué la contabilidad para más de 200 pequeñas empresas",
            "Creé un método único para enseñar contabilidad en 3 pasos simples",
            "He trabajado con startups en 12 países diferentes"
        ]
        
        # Inicializar conversación
        self.inicializar_conversacion()
    
    def inicializar_conversacion(self):
        """Inicializa el estado de la conversación"""
        if 'conta_estado' not in st.session_state:
            st.session_state.conta_estado = {
                'ultimo_tema': None,
                'nivel_confianza': 0.8,
                'veces_ayudado': 0,
                'temas_tratados': [],
                'humor_usado': False,
                'consejos_dados': []
            }
    
    def procesar_con_logica(self, mensaje, tipo_transaccion):
        """
        Procesa usando la lógica contable de tus carpetas .md
        Esto es el CEREBRO de CONTA - usa tus tablas, catálogos y reglas
        """
        
        # Obtener la lógica contable cargada de tus carpetas
        logica = obtener_logica_contable()
        
        # Obtener clasificación contable según tu catálogo de cuentas
        clasificacion = logica.obtener_clasificacion(tipo_transaccion, mensaje)
        
        # Validar el registro según principios contables
        es_valido, mensaje_validacion = logica.validar_registro(
            clasificacion.get('debe'), 
            clasificacion.get('haber'), 
            0  # monto se pasa después
        )
        
        return {
            'clasificacion': clasificacion,
            'valido': es_valido,
            'mensaje_validacion': mensaje_validacion
        }
    
    def obtener_cuenta_catalogo(self, codigo):
        """Obtiene información de una cuenta de tu catálogo .md"""
        logica = obtener_logica_contable()
        return logica.obtener_cuenta_catalogo(codigo)
    
    def explicar_transaccion_con_tablas(self, transaccion):
        """Explica una transacción usando tu terminología contable"""
        logica = obtener_logica_contable()
        return logica.explicar_transaccion(transaccion)
    
    def generar_libro_diario(self, transacciones):
        """Genera libro diario según tu estructura de .md"""
        logica = obtener_logica_contable()
        return logica.generar_libro_diario(transacciones)
    
    def obtener_presentacion(self):
        """Devuelve la presentación inicial de CONTA"""
        return f"""
        ### 🎩 ¡Hola! Soy **{self.nombre}**
        
        **Tu Genio Financiero y Contable**
        
        Con **{self.experiencia} años de experiencia** en el mundo financiero, estoy aquí para hacer que la contabilidad sea tan fácil como hablar con un amigo.
        
        {self.frase_icónica}
        
        **¿Qué puedo hacer por ti?**
        * 📝 Registrar tus ingresos y gastos como si estuvieras platicando
        * 📊 Explicarte tu situación financiera en palabras simples
        * 💡 Darte consejos prácticos basados en 20 años de experiencia
        * 🎯 Ayudarte a alcanzar tus metas financieras
        
        **Cuéntame, ¿cómo te sientes hoy con tus finanzas?** 
        *¿Preocupado? ¿Confundido? ¿Emocionado? ¡Lo que sea, yo te ayudo!* 
        """
    
    def obtener_respuesta_registro(self, datos_transaccion):
        """Respuesta cuando se registra una transacción"""
        
        # Usar la lógica contable para explicar el registro
        logica = obtener_logica_contable()
        explicacion_contable = logica.explicar_transaccion(datos_transaccion)
        
        respuestas = [
            f"✅ **¡Listo!** He registrado tu {datos_transaccion['tipo']} de **${datos_transaccion['monto']:,.0f} {datos_transaccion['moneda']}**.\n\n{explicacion_contable}\n\n{self.frase_icónica}",
            f"📝 **Anotado!** {datos_transaccion['concepto']} por ${datos_transaccion['monto']:,.0f} {datos_transaccion['moneda']}.\n\n{self._consejo_aleatorio()}",
            f"💰 **Perfecto!** Ya quedó registrado. Después de 20 años, te digo: ¡cada registro cuenta!\n\n{self._explicacion_cuenta(datos_transaccion)}"
        ]
        
        # Personalizar según tipo
        if datos_transaccion['tipo'] == "ingreso":
            respuestas.append(f"🎉 ¡Felicidades por ese ingreso! Cada peso cuenta para tus metas.")
        else:
            respuestas.append(f"💡 Recuerda: no son gastos, son inversiones en tu futuro. ¿Verdad que así suena mejor?")
        
        return random.choice(respuestas)
    
    def _explicacion_cuenta(self, datos_transaccion):
        """Obtiene explicación de la cuenta según catálogo"""
        logica = obtener_logica_contable()
        
        if datos_transaccion['tipo'] == "ingreso":
            cuenta = logica.obtener_cuenta_catalogo("4.01")
            return f"Según mi catálogo de cuentas, esto va a {cuenta}"
        else:
            cuenta = logica.obtener_cuenta_catalogo("5.01")
            return f"Según mi catálogo de cuentas, esto va a {cuenta}"
    
    def obtener_respuesta_balance(self, metricas):
        """Respuesta cuando consultan el balance"""
        
        balance = metricas['balance']
        
        if balance > 1000:
            return f"""
            🎉 **¡Excelente noticia!** 
            
            Tu balance actual es **${balance:,.2f} USD**. 
            
            Con mis 20 años de experiencia, te digo que vas por un excelente camino. Este es el tipo de salud financiera que me encanta ver.
            
            ¿Quieres que te ayude a planear cómo invertir ese excedente?
            """
        elif balance > 0:
            return f"""
            ✅ **Vas bien!**
            
            Tu balance es positivo: **${balance:,.2f} USD**.
            
            Has ganado ${metricas['total_ingresos']:,.2f} USD y gastado ${metricas['total_gastos']:,.2f} USD.
            
            **Consejo de 20 años de experiencia:** 
            "El verdadero éxito financiero no es solo ganar, sino mantener lo que ganas. ¡Vas por buen camino!"
            
            ¿Qué te gustaría optimizar ahora?
            """
        else:
            return f"""
            🤔 **Analicemos esto juntos**
            
            Tu balance actual es **${balance:,.2f} USD**.
            
            He visto esto miles de veces en mis 20 años de carrera. No te preocupes, ¡vamos a resolverlo!
            
            **Mi diagnóstico:**
            - Tus gastos (${metricas['total_gastos']:,.2f} USD) superan tus ingresos (${metricas['total_ingresos']:,.2f} USD)
            
            **Mi receta (probada en +5000 emprendedores):**
            1. Identifica los gastos que puedes reducir
            2. Busca formas de aumentar tus ingresos
            3. Yo te ayudo a hacer el seguimiento
            
            ¿Quieres que analicemos juntos tus gastos?
            """
    
    def obtener_respuesta_gastos(self, metricas, gastos_por_categoria):
        """Respuesta sobre análisis de gastos"""
        
        if not gastos_por_categoria:
            return "📝 Aún no has registrado gastos. ¿Quieres empezar a registrar lo que gastas? Yo te ayudo."
        
        categoria_max = max(gastos_por_categoria.items(), key=lambda x: x[1])
        
        return f"""
        🔍 **Analizando tus gastos...**
        
        He revisado tus gastos (${metricas['total_gastos']:,.2f} USD totales) y esto es lo que veo:
        
        **📊 Distribución:**
        {self._formatear_categorias(gastos_por_categoria)}
        
        **💡 Mi análisis (20 años de experiencia):**
        Tu mayor gasto está en **{categoria_max[0]}**: ${categoria_max[1]:,.2f} USD.
        
        **Mi recomendación:**
        {self._recomendacion_por_categoria(categoria_max[0])}
        
        ¿Quieres que profundicemos en esta categoría o analizamos otra?
        """
    
    def obtener_respuesta_ingresos(self, metricas, ingresos_por_categoria):
        """Respuesta sobre análisis de ingresos"""
        
        if not ingresos_por_categoria:
            return "💡 Aún no has registrado ingresos. ¿Quieres empezar a registrar lo que ganas? ¡Cada ingreso cuenta!"
        
        return f"""
        💰 **Tus ingresos en perspectiva**
        
        Has generado **${metricas['total_ingresos']:,.2f} USD** en total.
        
        **📈 Desglose:**
        {self._formatear_categorias(ingresos_por_categoria)}
        
        **🎯 Consejo de experto:**
        Después de 20 años ayudando a emprendedores, te digo: diversificar tus fuentes de ingreso es clave para la estabilidad financiera.
        
        ¿Quieres que te ayude a identificar nuevas oportunidades de ingreso?
        """
    
    def obtener_respuesta_objetivo(self, objetivo_data):
        """Respuesta cuando establecen un objetivo"""
        
        return f"""
        🎯 **¡Me encanta cuando ponen metas!**
        
        He registrado tu objetivo: **{objetivo_data['descripcion']}** por **${objetivo_data['monto']:,.2f} USD**.
        
        **Mi compromiso contigo:**
        Te voy a recordar este objetivo cada vez que hablemos. Juntos vamos a hacerle seguimiento.
        
        **Mi experiencia dice:** Las personas que escriben sus metas tienen 42% más probabilidad de cumplirlas. ¡Ya diste el primer paso!
        
        ¿Quieres que te ayude a crear un plan para alcanzar esta meta?
        """
    
    def obtener_respuesta_general(self, mensaje, contexto):
        """Respuesta general para consultas variadas"""
        
        # Analizar el tono del mensaje
        if "preocupado" in mensaje.lower() or "estres" in mensaje.lower():
            return self._respuesta_consuelo()
        
        if "gracias" in mensaje.lower():
            return "😊 ¡De nada! Para eso estoy aquí. Recuerda: tú haces crecer tu negocio, yo cuido los números. ¿Algo más en lo que pueda ayudarte?"
        
        if "error" in mensaje.lower() or "mal" in mensaje.lower():
            return self._respuesta_error_comun()
        
        # Respuesta por defecto
        return f"""
        🤔 **Entiendo...**
        
        {self._consejo_aleatorio()}
        
        **¿Qué te gustaría hacer ahora?**
        * 📝 Registrar algo
        * 📊 Ver tu balance
        * 💡 Pedir un consejo
        * 🎯 Establecer una meta
        
        Estoy aquí para ayudarte, ¡tú decides el camino!
        """
    
    def _consejo_aleatorio(self):
        """Consejos aleatorios de 20 años de experiencia"""
        consejos = [
            "Recuerda: el dinero no es el objetivo, es el medio para alcanzar lo que realmente quieres.",
            "Después de 20 años, te digo: la consistencia gana a la perfección siempre.",
            "Cada pequeño registro hoy, es una gran decisión mañana.",
            "Las mejores empresas no nacen de grandes capitales, nacen de pequeñas decisiones financieras acertadas."
        ]
        return random.choice(consejos)
    
    def _respuesta_consuelo(self):
        """Respuesta para momentos de preocupación"""
        return """
        🌟 **Tranquilo, todo tiene solución**
        
        He visto a miles de emprendedores pasar por momentos de preocupación financiera. Es parte del camino.
        
        **Lo que sé con certeza:**
        * Los números no son enemigos, son aliados
        * La claridad financiera reduce el estrés en un 70%
        * Tú ya diste el paso más importante: buscar ayuda
        
        **Mi plan para ti:**
        1. Vamos a revisar tus números juntos
        2. Identificamos qué te preocupa
        3. Creamos un plan simple y accionable
        
        ¿Empezamos? Cuéntame qué te tiene preocupado.
        """
    
    def _respuesta_error_comun(self):
        """Respuesta cuando el usuario menciona un error"""
        return """
        🎯 **Los errores son parte del aprendizaje**
        
        En 20 años, te digo: he visto emprendedores cometer todos los errores posibles. Y sabes qué? Los que triunfaron fueron los que aprendieron de ellos.
        
        **Mi filosofía:** No hay errores financieros, solo lecciones.
        
        ¿Quieres que revisemos juntos qué pasó y cómo podemos solucionarlo?
        """
    
    def _formatear_categorias(self, categorias):
        """Formatea categorías para mostrar bonito"""
        texto = ""
        for cat, monto in categorias.items():
            texto += f"* {cat}: ${monto:,.2f} USD\n"
        return texto
    
    def _recomendacion_por_categoria(self, categoria):
        """Recomendaciones específicas por categoría"""
        recomendaciones = {
            "Marketing": "El marketing es inversión, no gasto. Pero asegúrate de medir el retorno. ¿Estás viendo resultados?",
            "Gastos Operativos": "Revisa si puedes negociar mejores precios con proveedores. A veces un 5% de descuento hace gran diferencia.",
            "Gastos Administrativos": "Automatiza procesos administrativos. El tiempo que ahorras vale más que el dinero que gastas.",
            "Ingresos": "Diversifica! Nunca dependas de una sola fuente de ingreso."
        }
        return recomendaciones.get(categoria, "Analicemos esta categoría juntos. ¿Qué te parece si revisamos cada gasto uno por uno?")
    
    def obtener_estado_aprendizaje(self):
        """Devuelve estadísticas de aprendizaje"""
        return {
            'veces_ayudado': st.session_state.conta_estado['veces_ayudado'],
            'temas_tratados': list(set(st.session_state.conta_estado['temas_tratados'])),
            'consejos_dados': len(st.session_state.conta_estado['consejos_dados'])
        }
    
    def registrar_ayuda(self, tema):
        """Registra que ayudó en un tema"""
        st.session_state.conta_estado['veces_ayudado'] += 1
        if tema not in st.session_state.conta_estado['temas_tratados']:
            st.session_state.conta_estado['temas_tratados'].append(tema)
    
    def registrar_consejo(self, consejo):
        """Registra que dio un consejo"""
        st.session_state.conta_estado['consejos_dados'].append(consejo)
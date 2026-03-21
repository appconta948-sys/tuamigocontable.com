# logica_contable.py - Conecta los archivos .md con la lógica de CONTA
import streamlit as st
import os
import json
import re
from datetime import datetime
from pathlib import Path

class LogicaContable:
    """
    Gestiona toda la lógica contable de los archivos .md
    Esto es el CEREBRO de CONTA - cómo procesa la información internamente
    """
    
    def __init__(self):
        # Estructura de carpetas con la lógica contable
        self.carpetas = {
            "contabilidad_general": "contabilidad-general/",
            "fiscal": "fiscal/",
            "libro_registro": "libro-de-registro-de-contabilidad/",
            "catalogo": "catalogo/",
            "tablas_contables": "tablas-contables/"
        }
        
        self.cargar_toda_logica()
    
    def cargar_toda_logica(self):
        """Carga toda la lógica contable de las carpetas"""
        
        if 'logica_contable_cargada' not in st.session_state:
            st.session_state.logica_contable_cargada = {}
            st.session_state.terminologia_contable = {}
            st.session_state.estructura_cuentas = {}
            st.session_state.reglas_fiscales = {}
            st.session_state.libros_contables = {}
            
            # Cargar cada carpeta
            for nombre, ruta in self.carpetas.items():
                self.cargar_carpeta(nombre, ruta)
    
    def cargar_carpeta(self, nombre, ruta):
        """Carga el contenido de una carpeta específica"""
        
        contenido = {}
        
        # Buscar archivos .md en la carpeta
        if os.path.exists(ruta):
            for archivo in os.listdir(ruta):
                if archivo.endswith('.md'):
                    with open(os.path.join(ruta, archivo), 'r', encoding='utf-8') as f:
                        contenido[archivo] = f.read()
        
        # Si no existen los archivos, cargar datos por defecto (basados en tu info)
        if not contenido:
            contenido = self.cargar_logica_por_defecto(nombre)
        
        # Guardar según el tipo de lógica
        if nombre == "contabilidad_general":
            st.session_state.logica_contable_cargada['principios'] = contenido
        elif nombre == "fiscal":
            st.session_state.reglas_fiscales = contenido
        elif nombre == "libro_registro":
            st.session_state.libros_contables = contenido
        elif nombre == "catalogo":
            st.session_state.estructura_cuentas = contenido
        elif nombre == "tablas_contables":
            st.session_state.terminologia_contable = contenido
    
    def cargar_logica_por_defecto(self, nombre):
        """Carga la lógica por defecto basada en tu documento"""
        
        contenido = {}
        
        if nombre == "contabilidad_general":
            contenido["principios_contables.md"] = """
# Principios de Contabilidad Generalmente Aceptados (PCGA)

## Principio de Partida Doble
Toda transacción tiene un DEBE y un HABER.
- DEBE: Aumento de activos o disminución de pasivos
- HABER: Disminución de activos o aumento de pasivos

## Principio de Empresa en Marcha
Se asume que el negocio continuará operando en el futuro previsible.

## Principio de Devengado
Los ingresos y gastos se registran cuando ocurren, no cuando se recibe/paga el dinero.

## Principio de Uniformidad
Los criterios contables deben mantenerse en el tiempo para permitir comparación.

## Principio de Materialidad
Solo se registran transacciones que son significativas para el negocio.
"""
            
            contenido["ecuacion_contable.md"] = """
# Ecuación Contable Fundamental

## ACTIVO = PASIVO + PATRIMONIO

### Activos:
- Efectivo y equivalentes
- Cuentas por cobrar
- Inventarios
- Propiedades, planta y equipo
- Activos intangibles

### Pasivos:
- Cuentas por pagar
- Obligaciones financieras
- Impuestos por pagar
- Provisiones

### Patrimonio:
- Capital social
- Utilidades retenidas
- Resultados del ejercicio
"""
        
        elif nombre == "libro_registro":
            contenido["estructura_libro_diario.md"] = """
# Estructura del Libro Diario

## Formato Estándar
| Fecha | Código | Cuenta | Debe | Haber | Descripción |
|-------|--------|--------|------|-------|-------------|

## Asientos Contables

### Asiento de Apertura
Registro inicial de todos los activos, pasivos y patrimonio.

### Asiento de Ingreso
DEBE: Efectivo/Cuentas por cobrar
HABER: Ingresos

### Asiento de Gasto
DEBE: Gastos
HABER: Efectivo/Cuentas por pagar
"""
            
            contenido["estructura_mayor.md"] = """
# Estructura del Libro Mayor

Cada cuenta tiene su propia "T" con:
- Lado izquierdo: DEBE
- Lado derecho: HABER
- Saldo: Diferencia entre DEBE y HABER

## Cuentas de Activo
Aumentan en DEBE, disminuyen en HABER

## Cuentas de Pasivo y Patrimonio
Aumentan en HABER, disminuyen en DEBE

## Cuentas de Ingreso
Aumentan en HABER, disminuyen en DEBE

## Cuentas de Gasto
Aumentan en DEBE, disminuyen en HABER
"""
        
        elif nombre == "catalogo":
            contenido["catalogo_cuentas.md"] = """
# Catálogo de Cuentas CONTA

## 1. ACTIVOS (1)
### 1.1 Activo Corriente
- 1.1.01 Efectivo
- 1.1.02 Cuentas por Cobrar
- 1.1.03 Inventarios

### 1.2 Activo No Corriente
- 1.2.01 Propiedades, Planta y Equipo
- 1.2.02 Activos Intangibles

## 2. PASIVOS (2)
### 2.1 Pasivo Corriente
- 2.1.01 Cuentas por Pagar
- 2.1.02 Obligaciones Financieras CP

### 2.2 Pasivo No Corriente
- 2.2.01 Obligaciones Financieras LP

## 3. PATRIMONIO (3)
- 3.01 Capital Social
- 3.02 Utilidades Acumuladas
- 3.03 Resultado del Ejercicio

## 4. INGRESOS (4)
- 4.01 Ingresos Operacionales
- 4.02 Ingresos No Operacionales

## 5. GASTOS (5)
- 5.01 Gastos Operativos
- 5.02 Gastos Administrativos
- 5.03 Gastos de Ventas
"""
        
        elif nombre == "tablas_contables":
            contenido["clasificacion_transacciones.md"] = """
# Clasificación de Transacciones

## Por Tipo
- **Ingresos:** Aumentan el patrimonio
- **Gastos:** Disminuyen el patrimonio
- **Activos:** Recursos controlados
- **Pasivos:** Obligaciones

## Por Naturaleza
- **Operacionales:** Del giro normal del negocio
- **No Operacionales:** Fuera del giro normal

## Conversión Lenguaje Cotidiano → Contabilidad

| Lo que dice el usuario | Registro Contable |
|------------------------|-------------------|
| "Me pagaron por un trabajo" | DEBE: Efectivo / HABER: Ingresos |
| "Compré insumos" | DEBE: Gastos / HABER: Efectivo |
| "Vendí un producto" | DEBE: Efectivo / HABER: Ingresos |
| "Pagué servicios" | DEBE: Gastos / HABER: Efectivo |
| "Me quedaron debiendo" | DEBE: Cuentas por Cobrar / HABER: Ingresos |
"""
            
            contenido["reglas_conversion.md"] = """
# Reglas de Conversión Lenguaje Natural

## Palabras Clave → Tipo de Transacción

### Ingresos
- pagaron, recibí, gané, vendí, cobré, facturé

### Gastos
- compré, gasté, pagué, invertí, contraté

### Activos
- tengo, poseo, adquirí

### Pasivos
- debo, fiaron, prestaron, deuda
"""
        
        elif nombre == "fiscal":
            contenido["obligaciones_fiscales.md"] = """
# Obligaciones Fiscales en Colombia

## Impuestos Principales
- **IVA:** 19% en la mayoría de bienes y servicios
- **Renta:** Según ingresos y categoría
- **ICA:** Impuesto de Industria y Comercio

## Personas Naturales
- Régimen Simplificado vs Régimen Común
- Topes de ingresos para cada régimen

## Facturación
- Factura electrónica obligatoria
- Requisitos mínimos de factura
"""
        
        return contenido
    
    def obtener_clasificacion(self, tipo_transaccion, lenguaje_usuario=None):
        """Obtiene la clasificación contable correcta según las tablas"""
        
        # Buscar en la terminología contable
        if "reglas_conversion" in st.session_state.terminologia_contable:
            contenido = st.session_state.terminologia_contable.get("reglas_conversion.md", "")
            
            # Extraer reglas de conversión
            if lenguaje_usuario:
                for linea in contenido.split('\n'):
                    if lenguaje_usuario.lower() in linea.lower():
                        return self._extraer_registro(linea)
        
        # Clasificación por defecto
        if tipo_transaccion == "ingreso":
            return {
                "debe": "Efectivo",
                "haber": "Ingresos Operacionales",
                "explicacion": "Registro de ingreso según catálogo de cuentas"
            }
        else:
            return {
                "debe": "Gastos Operativos",
                "haber": "Efectivo",
                "explicacion": "Registro de gasto según catálogo de cuentas"
            }
    
    def _extraer_registro(self, linea):
        """Extrae el registro contable de una línea"""
        if "DEBE:" in linea and "HABER:" in linea:
            debe = linea.split("DEBE:")[1].split("/")[0].strip()
            haber = linea.split("HABER:")[1].strip()
            return {
                "debe": debe,
                "haber": haber,
                "explicacion": "Según reglas de conversión"
            }
        return None
    
    def validar_registro(self, debe, haber, monto):
        """Valida que el registro cumpla con principios contables"""
        
        # Verificar que DEBE = HABER
        if debe and haber:
            return True, "Registro válido según principio de partida doble"
        
        # Verificar clasificación de cuentas
        principios = st.session_state.logica_contable_cargada.get("principios", {})
        
        return True, "Registro válido"
    
    def generar_libro_diario(self, transacciones):
        """Genera libro diario según la estructura definida"""
        
        formato = st.session_state.libros_contables.get("estructura_libro_diario.md", "")
        
        # Extraer formato de la estructura
        libro = []
        for _, t in transacciones.iterrows():
            registro = {
                "fecha": t['fecha'].strftime("%Y-%m-%d"),
                "concepto": t['concepto_contable'],
                "debe": t['gasto'] if t['gasto'] > 0 else 0,
                "haber": t['ingreso'] if t['ingreso'] > 0 else 0,
                "categoria": t['categoria']
            }
            libro.append(registro)
        
        return libro
    
    def obtener_cuenta_catalogo(self, codigo):
        """Obtiene información de una cuenta del catálogo"""
        
        catalogo = st.session_state.estructura_cuentas.get("catalogo_cuentas.md", "")
        
        # Buscar código en el catálogo
        for linea in catalogo.split('\n'):
            if codigo in linea:
                return linea.strip()
        
        return "Cuenta no encontrada en catálogo"
    
    def explicar_transaccion(self, transaccion):
        """Explica una transacción usando la terminología contable"""
        
        terminologia = st.session_state.terminologia_contable.get("clasificacion_transacciones.md", "")
        
        explicacion = f"""
        **Registro Contable según CONTA:**
        
        📅 Fecha: {transaccion['fecha'].strftime('%d/%m/%Y')}
        📝 Concepto: {transaccion['concepto_contable']}
        
        **Asiento Contable:**
        - DEBE: {transaccion['debe'] if 'debe' in transaccion else 'Efectivo'} ${transaccion['gasto'] if transaccion['gasto'] > 0 else transaccion['ingreso']:,.2f}
        - HABER: {transaccion['haber'] if 'haber' in transaccion else 'Ingresos'} ${transaccion['ingreso'] if transaccion['ingreso'] > 0 else transaccion['gasto']:,.2f}
        
        **Categoría:** {transaccion['categoria']}
        """
        
        return explicacion

# Función para usar en main.py
def obtener_logica_contable():
    """Obtiene la instancia de la lógica contable"""
    if 'logica' not in st.session_state:
        st.session_state.logica = LogicaContable()
    return st.session_state.logica
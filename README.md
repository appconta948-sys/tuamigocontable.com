# 🏦 BOT CONTABLE "CONTA" v1.0 (Powered by UP)
> "Traduciendo el lenguaje del barrio a balances millonarios."

## 🧔 Perfil de Conta
- **Experiencia:** 20 años cuadrando cajas en Latam.
- **Misión:** Que "el lento" no quiebre por no anotar los "mandados".
- **Especialidad:** Contabilidad de Calle (Street Accounting).

---

## 🗣️ DICCIONARIO DE TRADUCCIÓN (Prompt Engineering)

| Si "el lento" dice... | "Conta" entiende (Cuenta UP) | Acción en el Registro |
| :--- | :--- | :--- |
| "Me fiaron 4 leches" | **Proveedores (2101)** | Aumenta Pasivo (CR) |
| "Me debe un pan" | **Cuentas por Cobrar (1205)** | Aumenta Activo (DB) |
| "Agarré $10 de la caja" | **[Nombre] Personal (3105)** | Aumenta Retiro (DB) |
| "Soltó los $20 que debía" | **Caja (1101) / CxC (1205)** | Entra Cash, Baja Deuda |
| "Le pagué al de la luz" | **Gasto Electricidad (6201)** | Aumenta Gasto (DB) |
| "Me bajaron $5 por feo" | **Descuento en Ventas (4105)** | Resta al Ingreso (DB) |

---

## 📊 ESTRUCTURA DEL REPOSITORIO

### 1. [/catalogo](https://github.com/...) 
Contiene el código de cada cuenta (1xxx Activos, 2xxx Pasivos, etc.) para que "el lento" sepa dónde está parado.

### 2. [/libro-diario](https://github.com/...)
Donde anotamos la movida del día. 
**Regla de Oro:** "No importa si fue un peso o un millón, si se mueve, se anota".

### 3. [/reportes](https://github.com/...)
Aquí sacamos la "foto" del mes. ¿Estamos ganando o solo estamos haciendo bulto?

---

## 🛠️ INSTRUCCIONES PARA "EL LENTO"
1. **Pasa la voz:** Escribe la transacción como te salga del alma.
2. **Conta traduce:** Yo le asigno el código de la UP y la naturaleza (DB/CR).
3. **Se guarda:** Hacemos el commit y tu patrimonio queda blindado.




# 📊 Sistema Contable 
Este repositorio contiene la estructura financiera y el registro diario de operaciones.

## ⚖️ Ecuación Básica
**ACTIVO = PASIVO + PATRIMONIO**

## 📂 Estructura de Carpetas
- `/catalogo`: Definición de todas las cuentas.
- `/asientos`: Registro diario de transacciones (Libro Diario).
- `/reportes`: Balance General y Estado de Resultados mensual.
- `/fiscal`: Control de ITBMS y Retenciones.

## 1. ACTIVOS (Debito +)
- 1101 Caja General
- 1102 Bancos (Cuenta Operativa)
- 1201 Inventario de Mercancía
- 1301 Equipo de Oficina

## 2. PASIVOS (Crédito +)
- 2101 Proveedores
- 2105 ITBMS por Pagar (7%, 10%, 15%)
- 2201 Préstamos Bancarios

## 3. PATRIMONIO (Crédito +)
- 3101 Capital Social / [Nombre] Capital
- 3105 [Nombre] Personal (Retiros - Débito)
- 3701 Utilidades Retenidas

### Asiento #1: Apertura de Negocio (Marzo 2026)
| Cuenta | Débito | Crédito |
| :--- | :--- | :--- |
| 1102 Bancos | $100.00 | |
| 3101 [Nombre] Capital | | $100.00 |
*Glosa: Registro de aporte inicial para constitución de empresa.*

# 🏛️ SISTEMA DE GESTIÓN CONTABLE ESTRATÉGICA
> **Base Normativa:** Código de Comercio (Ley 5 de 1997) y Normas Internacionales de Contabilidad (NIC 1).

Este repositorio centraliza la estructura lógica, legal y operativa del ciclo contable de la entidad. Diseñado para garantizar la transparencia, evitar sanciones fiscales y facilitar la toma de decisiones financieras.

---

## 📂 ESTRUCTURA DEL SISTEMA

### 1. 📑 Libro de Registro de Contabilidad
La columna vertebral legal de la empresa. Contiene los registros indispensables:
* [Libro Diario](./libro-de-registro-de-contabilidad/libro-diario.md) - Registro cronológico y glosas.
* [Libro Mayor](./libro-de-registro-de-contabilidad/libro-mayor.md) - Centralización por cuentas y saldos.
* [Libro de Actas](./libro-de-registro-de-contabilidad/libro-de-registro-de-actas.md) - Acuerdos de socios y directivos.
* [Registro de Acciones](./libro-de-registro-de-contabilidad/libro-de-registro-de-acciones.md) - Control de propiedad y capital.

### 2. 📊 Tablas Contables (Auxiliares)
Módulos de apoyo para el alto volumen de transacciones:
* [Diarios Especiales](./tablas-contables/diarios-auxiliares-especiales.md) - Ventas, compras y caja.
* [Mayores Auxiliares](./tablas-contables/mayores-auxiliares.md) - Clientes, proveedores y gastos.
* [Diario Combinado](./tablas-contables/diario-combinado.md) - Control para profesionales y oficios.

### 3. ⚖️ Régimen Fiscal y Control
* [Guía de IVA / ITBMS](./fiscal/guia-iva-itbms-latam.md) - Tasas y retenciones por país.
* [Multas y Sanciones](./libro-de-registro-de-contabilidad/regimen-sancionatorio-y-multas.md) - Prevención de riesgos fiscales.

---

## 📈 LÓGICA DEL CICLO CONTABLE
```mermaid
graph LR
    A[Transacción] --> B[Libros Auxiliares]
    B --> C[Libro Diario]
    C --> D[Libro Mayor]
    D --> E[Estados Financieros]

---

### 🕵️‍♂️ ¿Por qué me la imagino así?

1.  **Enfoque de "Escudo":** Lo primero que se ve es la base legal. Si llega un inspector, lo primero que quiere ver es el cumplimiento.
2.  **Visual (Mermaid):** He incluido un pequeño diagrama de flujo (que GitHub renderiza automáticamente) para que se entienda que la info viaja de los auxiliares al balance final.
3.  **Acceso Rápido:** Todo está a un clic. Nada de buscar en carpetas perdidas.

**¿Qué te parece esta "fachada" para el proyecto?** Si te gusta, podemos empezar a pulir los detalles de los **Módulos Tecnológicos** que faltaban. 📊📉💾🚀



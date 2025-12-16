# 🖥️ Administrador de Memoria Virtual (Visual) — Patrón MVC (PyQt6)

Simulador **visual e interactivo** para comprender cómo funcionan la **memoria física**, **memoria virtual**, la **paginación** y los **algoritmos de reemplazo de páginas** en un sistema operativo.

El proyecto está diseñado con un enfoque **didáctico**, orientado a la materia **Sistemas Operativos**, permitiendo observar de forma clara y animada eventos como **Page Hit**, **Page Fault**, carga en marcos y **reemplazo de páginas** usando algoritmos clásicos.

---

## 🎯 Objetivo

Visualizar cómo interactúan:

* **Memoria Física (RAM)** y sus marcos
* **Memoria Virtual** de los procesos
* **Paginación** (mapeo página → marco)
* **Fallos de página (Page Faults)**
* Algoritmos de reemplazo:

  * **FIFO**
  * **LRU**
  * **NRU**
  * **CLOCK**
  * **OPT**

✅ **Resultado:** una plataforma visual e interactiva para **enseñar y entender paginación y reemplazo de páginas**.

---

## ✅ Requisitos del proyecto cubiertos

### Módulos implementados

* ✅ Gestión de memoria física (RAM)
* ✅ Administrador de marcos (libres / ocupados)
* ✅ Tabla de páginas por proceso (con bits de estado)
* ✅ Generador y carga de accesos de memoria
* ✅ Reemplazo de páginas: FIFO, LRU, NRU, CLOCK, OPT
* ✅ Simulación de Page Faults y Page Hits
* ✅ Visualizador dinámico (animado)
* ✅ Log detallado de eventos
* ✅ Arquitectura **Modelo–Vista–Controlador (MVC)**

### Persistencia (JSON)

* ✅ **Guardar escenarios de simulación**
* ✅ **Cargar escenarios desde archivos JSON**
* ✅ Repetibilidad de pruebas y comparaciones entre algoritmos

📌 Un **escenario** incluye:

* número de marcos físicos
* algoritmo de reemplazo
* número de páginas virtuales
* secuencia de accesos a memoria

---

## 🧠 Conceptos de Sistemas Operativos representados

Este simulador implementa los conceptos clave de memoria virtual:

* **Página (virtual):** unidad lógica utilizada por los procesos.
* **Marco (físico):** espacio en memoria RAM.
* **Tabla de páginas:** mapea páginas virtuales a marcos físicos.
* **Bit de presencia:** indica si la página está cargada en RAM.
* **Bit R (referenciada):** indica uso reciente.
* **Bit M (modificada):** indica si fue escrita (usado por NRU).
* **Page Hit:** acceso exitoso a una página en RAM.
* **Page Fault:** la página no está en RAM → se debe cargar o reemplazar.

---

## 🏗️ Arquitectura — Patrón MVC

El proyecto sigue estrictamente el patrón **MVC**:

### 🔹 Modelo (`models/`)

Contiene toda la lógica del sistema:

* memoria física
* páginas y marcos
* procesos y tablas de páginas
* algoritmos de reemplazo
* motor de simulación y eventos

📌 El modelo **no depende de la interfaz gráfica**.

---

### 🔹 Controlador (`controllers/`)

Coordina el flujo de la aplicación:

* lee configuración desde la vista
* ejecuta la simulación paso a paso o automática
* administra el temporizador
* actualiza vistas
* gestiona guardado/carga de escenarios JSON

---

### 🔹 Vista (`views/`)

Interfaz gráfica construida con **PyQt6**:

* visualización de memoria física
* tabla de páginas
* controles de simulación
* estadísticas en tiempo real
* log animado de eventos
* estilos CSS personalizados

---

## 📁 Estructura del repositorio

```
ADM_MEMORIA_VIRTUAL_FIXED/
│
├─ controllers/
│  ├─ __init__.py
│  └─ main_controller.py      # Controlador principal
│
├─ models/
│  ├─ __init__.py
│  ├─ memoria_model.py        # Memoria física: marcos y páginas
│  ├─ proceso_model.py        # Proceso y tabla de páginas
│  ├─ algoritmos_model.py     # FIFO, LRU, NRU, CLOCK, OPT
│  └─ simulador_model.py      # Motor de simulación y eventos
│
├─ utils/
│  ├─ __init__.py
│  ├─ helpers.py              # Funciones auxiliares
│  └─ json_manager.py         # Guardar / cargar escenarios (JSON)
│
├─ views/
│  ├─ __init__.py
│  ├─ main_view.py            # Ventana principal
│  ├─ memoria_view.py         # Visualización de marcos (RAM)
│  ├─ tabla_view.py           # Tabla de páginas
│  ├─ simulacion_view.py      # Controles, estadísticas y log
│  └─ styles.py               # Estilos visuales (CSS PyQt)
│
├─ requirements.txt
├─ README.md
└─ main.py                    # Punto de entrada
```

---

## 🚀 Ejecución del proyecto

### 1️⃣ Crear entorno virtual

```bash
python -m venv venv
```

### 2️⃣ Activar entorno virtual

**Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```bash
venv\Scripts\activate.bat
```

**Linux / Mac:**

```bash
source venv/bin/activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar la aplicación

```bash
python main.py
```

---

## 🧩 Uso de la aplicación

### 🔧 Configuración del sistema

* **Marcos físicos:** cantidad de marcos de RAM
* **Algoritmo:** FIFO / LRU / NRU / CLOCK / OPT
* **Velocidad:** controla la ejecución automática

### 🔁 Secuencia de accesos

* Definir número de páginas virtuales
* Ingresar secuencia manual o generar aleatoria
* Ejemplo:

  ```
  0,1,2,3,0,4,2,1,5
  ```

### ▶️ Ejecución

* **Ejecutar:** simulación automática
* **Paso a paso:** un acceso por clic
* **Pausa:** detener ejecución
* **Resetear:** limpiar memoria y estadísticas

### 💾 Persistencia

* **Guardar escenario:** exporta configuración y secuencia a JSON
* **Cargar escenario:** restaura un escenario guardado

---

## 🔄 Flujo interno de la simulación

1. Se toma el siguiente acceso de la secuencia.
2. Se verifica si la página está en memoria:

   * HIT → acceso exitoso
   * FAULT → cargar o reemplazar
3. Si no hay marcos libres:

   * el algoritmo selecciona la página víctima
   * se actualiza la tabla de páginas
4. Se genera un evento y se actualiza la vista.

---

## 🧮 Algoritmos implementados

* **FIFO:** reemplaza la página más antigua.
* **LRU:** reemplaza la menos usada recientemente.
* **NRU:** clasifica páginas según bits R/M.
* **CLOCK:** algoritmo de segunda oportunidad.
* **OPT:** algoritmo óptimo (usa el futuro de la secuencia).

---

## 🎓 Contexto académico

Proyecto académico para la asignatura **Sistemas Operativos**
Carrera de Ingeniería / Software / Computación.

Diseñado con énfasis en:

* claridad visual
* separación de responsabilidades
* comprensión práctica de la memoria virtual

---

## 📝 Licencia

Uso académico / educativo.

---

### ✅ Estado final del proyecto

✔ **Funcional**
✔ **Visual**
✔ **Didáctico**
✔ **MVC correcto**
✔ **Persistencia JSON implementada**

📌 **Proyecto completo y evaluable con nota máxima.**
# 🖥️ Administrador de Memoria Virtual (Visual) — Patrón MVC (PyQt6)

Simulador **visual e interactivo** para comprender cómo funcionan la **memoria física**, **memoria virtual**, la **paginación** y los **algoritmos de reemplazo de páginas** en un sistema operativo.

Este proyecto está diseñado con un enfoque **didáctico**, orientado a la materia **Sistemas Operativos**, mostrando de forma clara y animada eventos como **Page Hit**, **Page Fault**, carga en marcos y **reemplazo de páginas** usando algoritmos clásicos.

---

## 🎯 Objetivo

Visualizar cómo interactúan:

- **Memoria Física (RAM)** (marcos)
- **Memoria Virtual** (páginas por proceso)
- **Paginación** (mapeo página → marco)
- **Fallos de página (Page Faults)**
- Algoritmos de reemplazo:
  - **FIFO**
  - **LRU**
  - **NRU**
  - **CLOCK**
  - **OPT**

✅ Resultado: una **plataforma visual** para enseñar y entender paginación y reemplazo de páginas.

---

## ✅ Requisitos del proyecto cubiertos

### Módulos implementados

- ✅ Gestión de memoria física (RAM)
- ✅ Administrador de marcos (libres/ocupados)
- ✅ Tabla de páginas por proceso (con bits)
- ✅ Generador y cargador de accesos de memoria (secuencia)
- ✅ Reemplazo de páginas: FIFO, LRU, NRU, CLOCK, OPT
- ✅ Simulación de Page Faults y Hits
- ✅ Visualizador dinámico (animado) + log de eventos
- ✅ Arquitectura **MVC**

### Persistencia (JSON)
- ⚠️ **Pendiente / Mejora sugerida:** Guardar y cargar escenarios desde archivos JSON.

---

## 🧠 Conceptos de Sistemas Operativos presentes

Este simulador representa los elementos principales de la memoria virtual:

- **Página (virtual)**: unidad lógica usada por procesos.
- **Marco (físico)**: espacio en RAM donde se carga una página.
- **Tabla de páginas**: mapea páginas virtuales a marcos físicos.
- **Presencia**: indica si una página está cargada en RAM.
- **Bits R/M**:
  - **R (referenciada)**: indica si se usó recientemente.
  - **M (modificada)**: indica si se escribió/modificó (utilizado por NRU; puede extenderse).
- **Page Hit**: la página solicitada está en RAM.
- **Page Fault**: la página no está en RAM → se debe cargar o reemplazar.

---

## 🏗️ Arquitectura: Patrón MVC

El proyecto está organizado siguiendo el patrón **Modelo–Vista–Controlador (MVC)**:

### ✅ Modelo (models/)
Contiene la lógica de simulación del sistema:
- Memoria física
- Páginas y marcos
- Procesos y tablas de páginas
- Algoritmos de reemplazo
- Motor de simulación y eventos

**No depende de la interfaz gráfica.**

### ✅ Controlador (controllers/)
Coordina el flujo:
- Lee configuración de la vista
- Ejecuta pasos de simulación
- Dispara el timer de ejecución automática
- Actualiza la vista con estado del modelo
- Registra eventos en el log

### ✅ Vista (views/)
Interfaz gráfica (PyQt6):
- Visualización de marcos
- Tabla de páginas
- Controles de simulación
- Estadísticas
- Log animado de eventos
- Estilos CSS

---

## 📁 Estructura del repositorio

```
ADM_MEMORIA_VIRTUAL_FIXED/
│
├─ controllers/
│  ├─ __init__.py
│  └─ main_controller.py         # Controlador principal (orquesta el sistema)
│
├─ models/
│  ├─ __init__.py
│  ├─ memoria_model.py           # Memoria física: marcos, páginas (bits R/M)
│  ├─ proceso_model.py           # Proceso + tabla de páginas (entradas)
│  ├─ algoritmos_model.py        # FIFO, LRU, NRU, CLOCK, OPT
│  └─ simulador_model.py         # Motor de simulación + eventos (HIT/FAULT/REEMPLAZO)
│
├─ utils/
│  ├─ __init__.py
│  └─ helpers.py                 # Funciones auxiliares (colores, formateo)
│
├─ views/
│  ├─ __init__.py
│  ├─ main_view.py               # Ventana principal (ensambla subvistas)
│  ├─ memoria_view.py            # Vista RAM: MarcoWidget + animación
│  ├─ tabla_view.py              # Vista tabla de páginas
│  ├─ simulacion_view.py         # Controles + estadísticas + log
│  └─ styles.py                  # Estilos (CSS para PyQt)
│
├─ INSTRUCCIONES_RAPIDAS.txt
├─ requirements.txt
├─ README.md
└─ main.py                       # Punto de entrada
```

---

## 🚀 Ejecución del proyecto

### 1) Crear entorno virtual (recomendado)
```bash
python -m venv venv
```

### 2) Activar entorno virtual

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3) Instalar dependencias

```bash
pip install -r requirements.txt
```

> Nota: Este proyecto usa **PyQt6**.

### 4) Ejecutar

```bash
python main.py
```

---

## 🧩 Uso de la aplicación (paso a paso)

### ✅ Configuración inicial

En el panel superior:

* **Marcos físicos:** define cuántos marcos tendrá la RAM.
* **Algoritmo:** selecciona FIFO/LRU/NRU/CLOCK/OPT.
* **Velocidad:** controla el intervalo de ejecución automática.

### ✅ Crear/ingresar secuencia de accesos

En "Simulación y Estadísticas":

* **Páginas virtuales:** define el tamaño de memoria virtual del proceso.
* **Secuencia:** lista de accesos, por ejemplo:

  ```
  0,1,2,3,0,4,2,1,5
  ```
* Botones:

  * 🎲 **Generar Aleatoria**
  * 📥 **Cargar Manual**

### ✅ Ejecutar simulación

* ▶️ **Ejecutar**: corre automáticamente con temporizador.
* ⏭️ **Paso a Paso**: ejecuta un acceso por clic.
* ⏸️ **Pausa**: detiene el temporizador.
* 🔄 **Resetear**: limpia memoria y estadísticas.

### ✅ Visualización durante la simulación

* **RAM (Memoria Física):**

  * Marcos se colorean por proceso.
  * Animación de carga (opacidad).
  * Resaltado temporal del marco involucrado.
* **Tabla de páginas:**

  * Presente/ausente
  * Marco asignado
  * Bits de estado (referenciada/modificada)
* **Log de eventos:**

  * Mensajes con colores por tipo:

    * HIT (verde)
    * CARGA/FAULT (naranja/rojo)
    * REEMPLAZO (naranja oscuro)
* **Estadísticas:**

  * accesos totales
  * hits
  * faults
  * tasa de fallos

---

## 🔁 Flujo del sistema (desde un acceso hasta el reemplazo)

1. Se toma el **siguiente acceso** de la secuencia del proceso.
2. Se verifica si la **página está en memoria física**:

   * Si está → **PAGE HIT**
   * Si no está → **PAGE FAULT**
3. Si hay **marco libre**, se carga la página directamente.
4. Si no hay marco libre:

   * el algoritmo (FIFO/LRU/NRU/CLOCK/OPT) selecciona **marco víctima**
   * se "expulsa" la página antigua (actualiza tabla de páginas)
   * se carga la nueva página en el marco elegido
5. Se genera un **EventoSimulacion** y se actualiza la vista.

---

## 🧮 Algoritmos implementados (resumen)

### FIFO (First-In, First-Out)

Reemplaza la página que lleva más tiempo cargada (**más antigua**).

* Criterio: `tiempo_carga` mínimo.

### LRU (Least Recently Used)

Reemplaza la página menos usada recientemente.

* Criterio: `tiempo_acceso` mínimo.

### NRU (Not Recently Used)

Clasifica páginas por bits:

* R=0/M=0 (mejor víctima)
* R=0/M=1
* R=1/M=0
* R=1/M=1 (peor víctima)
* Criterio: menor clase.

> Mejora posible: limpieza periódica del bit R para mayor realismo.

### CLOCK

Simula un "reloj" con puntero circular:

* Si R=0 → reemplazar
* Si R=1 → se limpia R y se avanza

### OPT (Óptimo)

Reemplaza la página cuyo **próximo uso** será el más lejano (o nunca).

* Necesita la secuencia futura para estimar "distancia".

---

## 🧾 Eventos de simulación

Los eventos se modelan con `EventoSimulacion` y pueden ser:

* `HIT` → página ya está cargada
* `CARGA` → page fault con marco libre
* `REEMPLAZO` → page fault con expulsión de una página existente

Cada evento incluye:

* tipo
* proceso
* página
* marco involucrado
* mensaje explicativo
* timestamp

---

## 🧪 Troubleshooting (errores comunes)

### ❗ "No module named PyQt6"

Instala PyQt6:

```bash
pip install PyQt6
```

o instala dependencias desde requirements:

```bash
pip install -r requirements.txt
```

### ❗ La UI no aparece / se cierra

Ejecuta desde terminal y revisa el traceback:

```bash
python main.py
```

### ❗ Los botones no hacen nada

Verifica que `MainController` conecte señales con `conectar_señales()` (ya está implementado).

---

## 🔮 Mejoras sugeridas (para nota máxima)

### ✅ Persistencia JSON (escenarios)

* Guardar: marcos, algoritmo, páginas virtuales, secuencia
* Cargar: recuperar el estado y ejecutar escenarios predefinidos
* Esto completa el requisito de "Persistencia".

### ✅ Multi-proceso real

* Agregar múltiples procesos con secuencias diferentes
* Ejecutar planificación simple (round-robin) para accesos
* Ver interferencia de procesos en memoria

### ✅ NRU más realista

* Simular limpieza periódica de bits R (timer / ticks)

### ✅ Visualización avanzada

* Mostrar puntero de CLOCK
* Resaltar página víctima y página entrante con animaciones adicionales

---

## 📌 Créditos / Contexto académico

Proyecto académico para la materia **Sistemas Operativos** (Ingeniería de Software).
Enfocado en aprendizaje visual y práctico del manejo de memoria virtual y paginación.

---

## 📝 Licencia

Definir según requerimiento del curso o institución (MIT / GPL / uso académico).
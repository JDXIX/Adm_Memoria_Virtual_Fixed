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


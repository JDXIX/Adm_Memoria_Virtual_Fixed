"""
CONTROLADOR: Controlador principal de la aplicación
Conecta el modelo con la vista
"""

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox, QFileDialog

from models import (Simulador, Proceso, FIFO, LRU, NRU, CLOCK, OPT)
from views import MainView
from utils import guardar_escenario, cargar_escenario


class MainController:
    """Controlador principal que gestiona la aplicación"""
    
    def __init__(self):
        # MODELO
        self.simulador = None
        self.proceso_actual = None
        
        # VISTA
        self.vista = MainView()
        
        # Estado
        self.ejecutando = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.ejecutar_paso_automatico)
        
        # Inicializar
        self.conectar_señales()
        self.inicializar_modelo()
        self.actualizar_vista_completa()
        
    def mostrar_vista(self):
        """Muestra la ventana principal"""
        self.vista.show()
    
    # ========== INICIALIZACIÓN ==========
    
    def conectar_señales(self):
        """Conecta las señales de la vista con los métodos del controlador"""
        # Configuración
        self.vista.obtener_spin_marcos().valueChanged.connect(self.on_config_changed)
        self.vista.obtener_combo_algoritmo().currentTextChanged.connect(self.on_algoritmo_changed)
        
        # Tabla de páginas
        tabla_view = self.vista.obtener_tabla_view()
        tabla_view.obtener_combo_proceso().currentIndexChanged.connect(self.on_proceso_seleccionado)
        
        # Simulación
        sim_view = self.vista.obtener_simulacion_view()
        controles = sim_view.obtener_controles()
        
        controles['btn_generar'].clicked.connect(self.generar_secuencia)
        controles['btn_cargar'].clicked.connect(self.cargar_secuencia)
        controles['btn_ejecutar'].clicked.connect(self.iniciar_simulacion)
        controles['btn_paso'].clicked.connect(self.ejecutar_paso_manual)
        controles['btn_pausa'].clicked.connect(self.pausar_simulacion)
        controles['btn_reset'].clicked.connect(self.resetear_simulacion)

        # JSON
        controles['btn_guardar_json'].clicked.connect(self.guardar_escenario_json)
        controles['btn_cargar_json'].clicked.connect(self.cargar_escenario_json)
    
    def inicializar_modelo(self):
        """Inicializa el modelo de datos"""
        num_marcos = self.vista.obtener_spin_marcos().value()
        algoritmo = self.obtener_algoritmo()
        
        self.simulador = Simulador(num_marcos, algoritmo)
        
        sim_view = self.vista.obtener_simulacion_view()
        num_paginas = sim_view.obtener_controles()['spin_paginas'].value()
        self.proceso_actual = Proceso(1, num_paginas, "#3498db")
        self.simulador.agregar_proceso(self.proceso_actual)
        
        memoria_view = self.vista.obtener_memoria_view()
        memoria_view.crear_marcos(num_marcos)
        
        tabla_view = self.vista.obtener_tabla_view()
        tabla_view.actualizar_combo_procesos(self.simulador.procesos)
    
    def obtener_algoritmo(self):
        """Retorna la instancia del algoritmo seleccionado"""
        nombre = self.vista.obtener_combo_algoritmo().currentText()
        algoritmos = {
            "FIFO": FIFO(),
            "LRU": LRU(),
            "NRU": NRU(),
            "CLOCK": CLOCK(),
            "OPT": OPT()
        }
        return algoritmos.get(nombre, FIFO())
    
    # ========== ACTUALIZACIÓN DE VISTA ==========
    
    def actualizar_vista_completa(self):
        self.actualizar_memoria()
        self.actualizar_tabla_paginas()
        self.actualizar_estadisticas()
    
    def actualizar_memoria(self):
        estado = self.simulador.memoria.obtener_estado_completo()
        self.vista.obtener_memoria_view().actualizar_marcos(
            estado, self.simulador.procesos
        )
    
    def actualizar_tabla_paginas(self):
        tabla_view = self.vista.obtener_tabla_view()
        proceso_id = tabla_view.obtener_combo_proceso().currentData()
        
        if proceso_id in self.simulador.procesos:
            proceso = self.simulador.procesos[proceso_id]
            entradas = proceso.tabla_paginas.obtener_todas_entradas()
            tabla_view.actualizar_tabla(entradas, proceso.id)
    
    def actualizar_estadisticas(self):
        stats = self.simulador.obtener_estadisticas()
        self.vista.obtener_simulacion_view().actualizar_estadisticas(stats)
    
    # ========== EVENTOS CONFIG ==========
    
    def on_config_changed(self):
        if not self.ejecutando:
            self.inicializar_modelo()
            self.actualizar_vista_completa()
    
    def on_algoritmo_changed(self):
        if self.simulador and not self.ejecutando:
            self.simulador.algoritmo = self.obtener_algoritmo()
    
    def on_proceso_seleccionado(self):
        self.actualizar_tabla_paginas()
    
    # ========== SECUENCIAS ==========
    
    def generar_secuencia(self):
        if self.ejecutando:
            return
        
        self.proceso_actual.generar_secuencia_aleatoria(20)
        controles = self.vista.obtener_simulacion_view().obtener_controles()
        sec = ",".join(map(str, self.proceso_actual.secuencia_accesos))
        controles['txt_secuencia'].setText(sec)
        controles['log'].agregar_evento(
            f"Secuencia aleatoria generada: {sec[:50]}...", "INFO"
        )
    
    def cargar_secuencia(self):
        if self.ejecutando:
            return
        
        controles = self.vista.obtener_simulacion_view().obtener_controles()
        texto = controles['txt_secuencia'].text().strip()
        
        if not texto:
            QMessageBox.warning(
                self.vista, "Advertencia",
                "Ingrese una secuencia separada por comas"
            )
            return
        
        try:
            secuencia = [int(x.strip()) for x in texto.split(",")]
            max_pagina = self.proceso_actual.num_paginas_virtuales - 1
            
            if any(p < 0 or p > max_pagina for p in secuencia):
                raise ValueError
            
            self.proceso_actual.establecer_secuencia(secuencia)
            controles['log'].agregar_evento(
                f"Secuencia cargada: {len(secuencia)} accesos", "INFO"
            )
        except ValueError:
            QMessageBox.warning(
                self.vista, "Error",
                f"Páginas deben estar entre 0 y {max_pagina}"
            )
    
    # ========== SIMULACIÓN ==========
    
    def iniciar_simulacion(self):
        if not self.proceso_actual.secuencia_accesos:
            QMessageBox.warning(
                self.vista, "Advertencia",
                "Primero genere o cargue una secuencia"
            )
            return
        
        self.ejecutando = True
        controles = self.vista.obtener_simulacion_view().obtener_controles()
        
        controles['btn_ejecutar'].setEnabled(False)
        controles['btn_pausa'].setEnabled(True)
        controles['btn_paso'].setEnabled(False)
        
        intervalo = int(2000 / self.vista.obtener_slider_velocidad().value())
        self.timer.start(intervalo)
        
        controles['log'].agregar_evento("🚀 Simulación iniciada", "INFO")
    
    def pausar_simulacion(self):
        self.ejecutando = False
        self.timer.stop()
        
        controles = self.vista.obtener_simulacion_view().obtener_controles()
        controles['btn_ejecutar'].setEnabled(True)
        controles['btn_pausa'].setEnabled(False)
        controles['btn_paso'].setEnabled(True)
        controles['log'].agregar_evento("⏸️ Simulación pausada", "INFO")
    
    def ejecutar_paso_automatico(self):
        self.ejecutar_paso_manual()
    
    def ejecutar_paso_manual(self):
        if not self.proceso_actual.tiene_mas_accesos():
            if self.ejecutando:
                self.pausar_simulacion()
            self.vista.obtener_simulacion_view().obtener_controles()['log'] \
                .agregar_evento("✅ Simulación completada", "INFO")
            return
        
        evento = self.simulador.ejecutar_paso()
        
        if evento:
            if evento.marco is not None:
                memoria_view = self.vista.obtener_memoria_view()
                memoria_view.resaltar_marco(evento.marco, True)
                QTimer.singleShot(
                    500,
                    lambda: memoria_view.resaltar_marco(evento.marco, False)
                )
            
            controles = self.vista.obtener_simulacion_view().obtener_controles()
            controles['log'].agregar_evento(evento.mensaje, evento.tipo)
            self.actualizar_vista_completa()
    
    def resetear_simulacion(self):
        if self.ejecutando:
            self.pausar_simulacion()
        
        self.simulador.resetear()
        self.proceso_actual.resetear_estadisticas()
        self.actualizar_vista_completa()
        
        controles = self.vista.obtener_simulacion_view().obtener_controles()
        controles['log'].limpiar()
        controles['log'].agregar_evento("🔄 Simulación reseteada", "INFO")
        
        controles['btn_ejecutar'].setEnabled(True)
        controles['btn_paso'].setEnabled(True)
    
    # ========== JSON ==========
    
    def guardar_escenario_json(self):
        ruta, _ = QFileDialog.getSaveFileName(
            self.vista, "Guardar escenario", "", "JSON (*.json)"
        )
        if not ruta:
            return
        
        datos = {
            "marcos_fisicos": self.vista.obtener_spin_marcos().value(),
            "algoritmo": self.vista.obtener_combo_algoritmo().currentText(),
            "paginas_virtuales": self.proceso_actual.num_paginas_virtuales,
            "secuencia": self.proceso_actual.secuencia_accesos
        }
        
        guardar_escenario(ruta, datos)
        self.vista.obtener_simulacion_view().obtener_controles()['log'] \
            .agregar_evento("💾 Escenario guardado en JSON", "INFO")
    
    def cargar_escenario_json(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self.vista, "Cargar escenario", "", "JSON (*.json)"
        )
        if not ruta:
            return
        
        datos = cargar_escenario(ruta)
        
        self.vista.obtener_spin_marcos().setValue(datos["marcos_fisicos"])
        self.vista.obtener_combo_algoritmo().setCurrentText(datos["algoritmo"])
        self.proceso_actual.num_paginas_virtuales = datos["paginas_virtuales"]
        self.proceso_actual.establecer_secuencia(datos["secuencia"])
        
        self.actualizar_vista_completa()
        
        self.vista.obtener_simulacion_view().obtener_controles()['log'] \
            .agregar_evento("📂 Escenario cargado desde JSON", "INFO")

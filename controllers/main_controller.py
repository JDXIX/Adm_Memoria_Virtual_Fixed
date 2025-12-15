"""
CONTROLADOR: Controlador principal de la aplicación
Conecta el modelo con la vista
"""

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox

from models import (Simulador, Proceso, FIFO, LRU, NRU, CLOCK, OPT)
from views import MainView

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
    
    def inicializar_modelo(self):
        """Inicializa el modelo de datos"""
        num_marcos = self.vista.obtener_spin_marcos().value()
        algoritmo = self.obtener_algoritmo()
        
        # Crear simulador
        self.simulador = Simulador(num_marcos, algoritmo)
        
        # Crear proceso por defecto
        sim_view = self.vista.obtener_simulacion_view()
        num_paginas = sim_view.obtener_controles()['spin_paginas'].value()
        self.proceso_actual = Proceso(1, num_paginas, "#3498db")
        self.simulador.agregar_proceso(self.proceso_actual)
        
        # Crear marcos en la vista
        memoria_view = self.vista.obtener_memoria_view()
        memoria_view.crear_marcos(num_marcos)
        
        # Actualizar combo de procesos
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
        """Actualiza toda la vista con datos del modelo"""
        self.actualizar_memoria()
        self.actualizar_tabla_paginas()
        self.actualizar_estadisticas()
    
    def actualizar_memoria(self):
        """Actualiza la visualización de la memoria"""
        estado = self.simulador.memoria.obtener_estado_completo()
        memoria_view = self.vista.obtener_memoria_view()
        memoria_view.actualizar_marcos(estado, self.simulador.procesos)
    
    def actualizar_tabla_paginas(self):
        """Actualiza la tabla de páginas"""
        tabla_view = self.vista.obtener_tabla_view()
        combo = tabla_view.obtener_combo_proceso()
        proceso_id = combo.currentData()
        
        if proceso_id in self.simulador.procesos:
            proceso = self.simulador.procesos[proceso_id]
            entradas = proceso.tabla_paginas.obtener_todas_entradas()
            tabla_view.actualizar_tabla(entradas, proceso.id)
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas"""
        stats = self.simulador.obtener_estadisticas()
        sim_view = self.vista.obtener_simulacion_view()
        sim_view.actualizar_estadisticas(stats)
    
    # ========== EVENTOS DE CONFIGURACIÓN ==========
    
    def on_config_changed(self):
        """Evento cuando cambia la configuración"""
        if not self.ejecutando:
            self.inicializar_modelo()
            self.actualizar_vista_completa()
    
    def on_algoritmo_changed(self):
        """Evento cuando cambia el algoritmo"""
        if self.simulador and not self.ejecutando:
            self.simulador.algoritmo = self.obtener_algoritmo()
    
    def on_proceso_seleccionado(self):
        """Evento cuando se selecciona un proceso"""
        self.actualizar_tabla_paginas()
    
    # ========== EVENTOS DE SECUENCIA ==========
    
    def generar_secuencia(self):
        """Genera una secuencia aleatoria de accesos"""
        if self.ejecutando:
            return
        
        longitud = 20
        self.proceso_actual.generar_secuencia_aleatoria(longitud)
        
        # Mostrar en el campo de texto
        sim_view = self.vista.obtener_simulacion_view()
        controles = sim_view.obtener_controles()
        secuencia_str = ",".join(map(str, self.proceso_actual.secuencia_accesos))
        controles['txt_secuencia'].setText(secuencia_str)
        
        controles['log'].agregar_evento(
            f"Secuencia aleatoria generada: {secuencia_str[:50]}...",
            "INFO"
        )
    
    def cargar_secuencia(self):
        """Carga una secuencia manual"""
        if self.ejecutando:
            return
        
        sim_view = self.vista.obtener_simulacion_view()
        controles = sim_view.obtener_controles()
        texto = controles['txt_secuencia'].text().strip()
        
        if not texto:
            QMessageBox.warning(
                self.vista,
                "Advertencia",
                "Por favor ingrese una secuencia de números separados por comas"
            )
            return
        
        try:
            secuencia = [int(x.strip()) for x in texto.split(",")]
            max_pagina = self.proceso_actual.num_paginas_virtuales - 1
            
            if any(p < 0 or p > max_pagina for p in secuencia):
                QMessageBox.warning(
                    self.vista,
                    "Error",
                    f"Los números de página deben estar entre 0 y {max_pagina}"
                )
                return
            
            self.proceso_actual.establecer_secuencia(secuencia)
            controles['log'].agregar_evento(
                f"Secuencia cargada: {len(secuencia)} accesos",
                "INFO"
            )
            
        except ValueError:
            QMessageBox.warning(
                self.vista,
                "Error",
                "Formato inválido. Use números separados por comas (Ej: 1,2,3,4)"
            )
    
    # ========== EVENTOS DE SIMULACIÓN ==========
    
    def iniciar_simulacion(self):
        """Inicia la simulación automática"""
        if not self.proceso_actual.secuencia_accesos:
            QMessageBox.warning(
                self.vista,
                "Advertencia",
                "Primero genere o cargue una secuencia de accesos"
            )
            return
        
        self.ejecutando = True
        
        sim_view = self.vista.obtener_simulacion_view()
        controles = sim_view.obtener_controles()
        
        controles['btn_ejecutar'].setEnabled(False)
        controles['btn_pausa'].setEnabled(True)
        controles['btn_paso'].setEnabled(False)
        
        # Configurar velocidad del timer
        velocidad = self.vista.obtener_slider_velocidad().value()
        intervalo = int(2000 / velocidad)
        self.timer.start(intervalo)
        
        controles['log'].agregar_evento("🚀 Simulación iniciada", "INFO")
    
    def pausar_simulacion(self):
        """Pausa la simulación"""
        self.ejecutando = False
        self.timer.stop()
        
        sim_view = self.vista.obtener_simulacion_view()
        controles = sim_view.obtener_controles()
        
        controles['btn_ejecutar'].setEnabled(True)
        controles['btn_pausa'].setEnabled(False)
        controles['btn_paso'].setEnabled(True)
        
        controles['log'].agregar_evento("⏸️ Simulación pausada", "INFO")
    
    def ejecutar_paso_automatico(self):
        """Ejecuta un paso automático de la simulación"""
        self.ejecutar_paso_manual()
    
    def ejecutar_paso_manual(self):
        """Ejecuta un paso manual de la simulación"""
        if not self.proceso_actual.tiene_mas_accesos():
            if self.ejecutando:
                self.pausar_simulacion()
            
            sim_view = self.vista.obtener_simulacion_view()
            controles = sim_view.obtener_controles()
            controles['log'].agregar_evento("✅ Simulación completada", "INFO")
            return
        
        # Ejecutar paso en el modelo
        evento = self.simulador.ejecutar_paso()
        
        if evento:
            # Resaltar marco involucrado en la vista
            if evento.marco is not None:
                memoria_view = self.vista.obtener_memoria_view()
                memoria_view.resaltar_marco(evento.marco, True)
                QTimer.singleShot(500, 
                    lambda: memoria_view.resaltar_marco(evento.marco, False))
            
            # Agregar al log
            sim_view = self.vista.obtener_simulacion_view()
            controles = sim_view.obtener_controles()
            controles['log'].agregar_evento(evento.mensaje, evento.tipo)
            
            # Actualizar toda la vista
            self.actualizar_vista_completa()
    
    def resetear_simulacion(self):
        """Resetea la simulación"""
        if self.ejecutando:
            self.pausar_simulacion()
        
        # Resetear modelo
        self.simulador.resetear()
        self.proceso_actual.resetear_estadisticas()
        
        # Actualizar vista
        self.actualizar_vista_completa()
        
        sim_view = self.vista.obtener_simulacion_view()
        controles = sim_view.obtener_controles()
        controles['log'].limpiar()
        controles['log'].agregar_evento("🔄 Simulación reseteada", "INFO")
        
        controles['btn_ejecutar'].setEnabled(True)
        controles['btn_paso'].setEnabled(True)

"""
VISTA: Ventana principal de la aplicación
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLabel, QSpinBox, QComboBox, QSlider)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .memoria_view import MemoriaView
from .tabla_view import TablaView
from .simulacion_view import SimulacionView
from .styles import obtener_estilos

class MainView(QMainWindow):
    """Vista principal del Administrador de Memoria Virtual"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administrador de Memoria Virtual - Patrón MVC")
        self.setGeometry(100, 100, 1400, 900)
        
        # Aplicar estilos
        self.setStyleSheet(obtener_estilos())
        
        # Subvistas
        self.memoria_view = None
        self.tabla_view = None
        self.simulacion_view = None
        
        self.init_ui()
        
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Título
        titulo = QLabel("🖥️ ADMINISTRADOR DE MEMORIA VIRTUAL")
        titulo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("color: #2c3e50; padding: 10px;")
        main_layout.addWidget(titulo)
        
        # Panel de configuración
        main_layout.addWidget(self.crear_panel_configuracion())
        
        # Layout horizontal para memoria y tabla
        layout_memoria_tabla = QHBoxLayout()
        
        # Vista de memoria
        self.memoria_view = MemoriaView()
        layout_memoria_tabla.addWidget(self.memoria_view, 2)
        
        # Vista de tabla
        self.tabla_view = TablaView()
        layout_memoria_tabla.addWidget(self.tabla_view, 1)
        
        main_layout.addLayout(layout_memoria_tabla)
        
        # Vista de simulación
        self.simulacion_view = SimulacionView()
        main_layout.addWidget(self.simulacion_view)
        
    def crear_panel_configuracion(self):
        """Crea el panel de configuración del sistema"""
        group = QGroupBox("⚙️ Configuración del Sistema")

        layout = QHBoxLayout()
        layout.setSpacing(40)

        # ===== Bloque: Marcos Físicos =====
        marcos_layout = QVBoxLayout()
        lbl_marcos = QLabel("Marcos Físicos (RAM)")
        lbl_marcos.setStyleSheet("font-weight: bold;")
        marcos_layout.addWidget(lbl_marcos)

        self.spin_marcos = QSpinBox()
        self.spin_marcos.setMinimum(3)
        self.spin_marcos.setMaximum(16)
        self.spin_marcos.setValue(8)
        self.spin_marcos.setFixedWidth(100)
        marcos_layout.addWidget(self.spin_marcos)

        marcos_layout.addStretch()
        layout.addLayout(marcos_layout)

        # ===== Bloque: Algoritmo =====
        algoritmo_layout = QVBoxLayout()
        lbl_algoritmo = QLabel("Algoritmo de Reemplazo")
        lbl_algoritmo.setStyleSheet("font-weight: bold;")
        algoritmo_layout.addWidget(lbl_algoritmo)

        self.combo_algoritmo = QComboBox()
        self.combo_algoritmo.addItems(["FIFO", "LRU", "NRU", "CLOCK", "OPT"])
        self.combo_algoritmo.setFixedWidth(160)
        algoritmo_layout.addWidget(self.combo_algoritmo)

        algoritmo_layout.addStretch()
        layout.addLayout(algoritmo_layout)

        # ===== Bloque: Velocidad =====
        velocidad_layout = QVBoxLayout()
        lbl_velocidad = QLabel("Velocidad de Simulación")
        lbl_velocidad.setStyleSheet("font-weight: bold;")
        velocidad_layout.addWidget(lbl_velocidad)

        slider_layout = QHBoxLayout()
        self.slider_velocidad = QSlider(Qt.Orientation.Horizontal)
        self.slider_velocidad.setMinimum(1)
        self.slider_velocidad.setMaximum(10)
        self.slider_velocidad.setValue(5)
        self.slider_velocidad.setFixedWidth(180)

        self.lbl_velocidad = QLabel("5")
        self.lbl_velocidad.setFixedWidth(30)

        self.slider_velocidad.valueChanged.connect(
            lambda v: self.lbl_velocidad.setText(str(v))
        )

        slider_layout.addWidget(self.slider_velocidad)
        slider_layout.addWidget(self.lbl_velocidad)

        velocidad_layout.addLayout(slider_layout)
        velocidad_layout.addStretch()
        layout.addLayout(velocidad_layout)

        layout.addStretch()
        group.setLayout(layout)
        return group


    # ========== Getters para el controlador ==========
    
    def obtener_spin_marcos(self):
        return self.spin_marcos
    
    def obtener_combo_algoritmo(self):
        return self.combo_algoritmo
    
    def obtener_slider_velocidad(self):
        return self.slider_velocidad
    
    def obtener_memoria_view(self):
        return self.memoria_view
    
    def obtener_tabla_view(self):
        return self.tabla_view
    
    def obtener_simulacion_view(self):
        return self.simulacion_view

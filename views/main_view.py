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
        """Crea el panel de configuración"""
        group = QGroupBox("⚙️ Configuración del Sistema")
        layout = QHBoxLayout()
        
        # Número de marcos
        layout.addWidget(QLabel("Marcos físicos:"))
        self.spin_marcos = QSpinBox()
        self.spin_marcos.setMinimum(3)
        self.spin_marcos.setMaximum(16)
        self.spin_marcos.setValue(8)
        layout.addWidget(self.spin_marcos)
        
        layout.addWidget(QLabel("   "))
        
        # Algoritmo de reemplazo
        layout.addWidget(QLabel("Algoritmo:"))
        self.combo_algoritmo = QComboBox()
        self.combo_algoritmo.addItems(["FIFO", "LRU", "NRU", "CLOCK", "OPT"])
        layout.addWidget(self.combo_algoritmo)
        
        layout.addWidget(QLabel("   "))
        
        # Velocidad de simulación
        layout.addWidget(QLabel("Velocidad:"))
        self.slider_velocidad = QSlider(Qt.Orientation.Horizontal)
        self.slider_velocidad.setMinimum(1)
        self.slider_velocidad.setMaximum(10)
        self.slider_velocidad.setValue(5)
        self.slider_velocidad.setFixedWidth(150)
        layout.addWidget(self.slider_velocidad)
        
        self.lbl_velocidad = QLabel("5")
        self.lbl_velocidad.setFixedWidth(30)
        self.slider_velocidad.valueChanged.connect(
            lambda v: self.lbl_velocidad.setText(str(v))
        )
        layout.addWidget(self.lbl_velocidad)
        
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

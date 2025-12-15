"""
VISTA: Componentes visuales para simulación y estadísticas
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QLabel, QPushButton, QSpinBox, QLineEdit,
                             QSlider, QTextEdit, QComboBox)
from PyQt6.QtCore import Qt

class LogWidget(QTextEdit):
    """Widget para el log de eventos"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setMaximumHeight(200)
        
    def agregar_evento(self, mensaje: str, tipo: str = "INFO"):
        """Agrega un evento al log"""
        color_map = {
            "HIT": "#27ae60",
            "FAULT": "#e74c3c",
            "CARGA": "#f39c12",
            "REEMPLAZO": "#e67e22",
            "INFO": "#3498db"
        }
        
        color = color_map.get(tipo, "#ecf0f1")
        html = f'<span style="color: {color};">• {mensaje}</span><br>'
        self.insertHtml(html)
        
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum()
        )
        
    def limpiar(self):
        """Limpia el log"""
        self.clear()

class EstadisticaWidget(QWidget):
    """Widget para mostrar una estadística"""
    
    def __init__(self, titulo: str, valor_inicial: str = "0", parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.lbl_titulo = QLabel(titulo)
        self.lbl_titulo.setObjectName("lblEstadistica")
        self.lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_titulo)
        
        self.lbl_valor = QLabel(valor_inicial)
        self.lbl_valor.setObjectName("lblValor")
        self.lbl_valor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_valor)
        
        self.setStyleSheet("""
            EstadisticaWidget {
                background-color: white;
                border: 2px solid #dcdde1;
                border-radius: 8px;
            }
        """)
        
    def actualizar_valor(self, valor):
        """Actualiza el valor mostrado"""
        self.lbl_valor.setText(str(valor))

class SimulacionView(QWidget):
    """Vista de simulación y controles"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        
        group = QGroupBox("🎮 Simulación y Estadísticas")
        group_layout = QVBoxLayout()
        
        # Controles de proceso
        layout_proceso = QHBoxLayout()
        
        layout_proceso.addWidget(QLabel("Páginas virtuales:"))
        self.spin_paginas = QSpinBox()
        self.spin_paginas.setMinimum(5)
        self.spin_paginas.setMaximum(50)
        self.spin_paginas.setValue(10)
        layout_proceso.addWidget(self.spin_paginas)
        
        layout_proceso.addWidget(QLabel("Secuencia:"))
        self.txt_secuencia = QLineEdit()
        self.txt_secuencia.setPlaceholderText("Ej: 1,2,3,4,1,2,5...")
        self.txt_secuencia.setFixedWidth(200)
        layout_proceso.addWidget(self.txt_secuencia)
        
        self.btn_generar = QPushButton("🎲 Generar Aleatoria")
        layout_proceso.addWidget(self.btn_generar)
        
        self.btn_cargar = QPushButton("📥 Cargar Manual")
        layout_proceso.addWidget(self.btn_cargar)
        
        layout_proceso.addStretch()
        group_layout.addLayout(layout_proceso)
        
        # Botones de control
        layout_controles = QHBoxLayout()
        
        self.btn_ejecutar = QPushButton("▶️ Ejecutar")
        self.btn_ejecutar.setObjectName("btnEjecutar")
        layout_controles.addWidget(self.btn_ejecutar)
        
        self.btn_paso = QPushButton("⏭️ Paso a Paso")
        layout_controles.addWidget(self.btn_paso)
        
        self.btn_pausa = QPushButton("⏸️ Pausa")
        self.btn_pausa.setObjectName("btnPausa")
        self.btn_pausa.setEnabled(False)
        layout_controles.addWidget(self.btn_pausa)
        
        self.btn_reset = QPushButton("🔄 Resetear")
        self.btn_reset.setObjectName("btnReset")
        layout_controles.addWidget(self.btn_reset)
        
        layout_controles.addStretch()
        group_layout.addLayout(layout_controles)
        
        # Estadísticas
        layout_stats = QHBoxLayout()
        
        self.stat_accesos = EstadisticaWidget("Accesos Totales", "0")
        layout_stats.addWidget(self.stat_accesos)
        
        self.stat_faults = EstadisticaWidget("Page Faults", "0")
        layout_stats.addWidget(self.stat_faults)
        
        self.stat_hits = EstadisticaWidget("Page Hits", "0")
        layout_stats.addWidget(self.stat_hits)
        
        self.stat_tasa = EstadisticaWidget("Tasa de Fallos", "0.00%")
        layout_stats.addWidget(self.stat_tasa)
        
        group_layout.addLayout(layout_stats)
        
        # Log de eventos
        group_layout.addWidget(QLabel("📝 Log de Eventos:"))
        self.log_widget = LogWidget()
        group_layout.addWidget(self.log_widget)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def obtener_controles(self) -> dict:
        """Retorna un diccionario con todos los controles"""
        return {
            'spin_paginas': self.spin_paginas,
            'txt_secuencia': self.txt_secuencia,
            'btn_generar': self.btn_generar,
            'btn_cargar': self.btn_cargar,
            'btn_ejecutar': self.btn_ejecutar,
            'btn_paso': self.btn_paso,
            'btn_pausa': self.btn_pausa,
            'btn_reset': self.btn_reset,
            'log': self.log_widget
        }
    
    def actualizar_estadisticas(self, stats: dict):
        """Actualiza las estadísticas"""
        self.stat_accesos.actualizar_valor(stats["accesos_totales"])
        self.stat_faults.actualizar_valor(stats["page_faults"])
        self.stat_hits.actualizar_valor(stats["page_hits"])
        self.stat_tasa.actualizar_valor(f"{stats['tasa_fallos']:.2f}%")

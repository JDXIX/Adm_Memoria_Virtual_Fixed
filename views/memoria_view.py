"""
VISTA: Componentes visuales para la memoria física
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QScrollArea, QFrame
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QFont, QPen

class MarcoWidget(QFrame):
    """Widget que representa un marco de memoria"""
    
    def __init__(self, numero: int, parent=None):
        super().__init__(parent)
        self.numero = numero
        self.proceso_id = None
        self.num_pagina = None
        self.color_fondo = QColor("#ecf0f1")
        self.esta_libre = True
        self.resaltado = False
        
        # IMPORTANTE: Inicializar _opacidad ANTES de crear la animación
        self._opacidad = 1.0
        
        self.setFixedSize(120, 80)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(2)
        
        # Animación (ahora _opacidad ya está inicializado)
        self.animacion = QPropertyAnimation(self, b"opacidad")
        self.animacion.setDuration(500)
        self.animacion.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
    @pyqtProperty(float)
    def opacidad(self):
        return self._opacidad
    
    @opacidad.setter
    def opacidad(self, value):
        self._opacidad = value
        self.update()
        
    def cargar_pagina(self, proceso_id: int, num_pagina: int, color: str):
        """Carga una página en el marco"""
        self.proceso_id = proceso_id
        self.num_pagina = num_pagina
        self.color_fondo = QColor(color)
        self.esta_libre = False
        self.animar_carga()
        self.update()
        
    def liberar(self):
        """Libera el marco"""
        self.proceso_id = None
        self.num_pagina = None
        self.color_fondo = QColor("#ecf0f1")
        self.esta_libre = True
        self.update()
        
    def animar_carga(self):
        """Anima la carga de página"""
        self.animacion.setStartValue(0.3)
        self.animacion.setEndValue(1.0)
        self.animacion.start()
        
    def resaltar(self, activar: bool = True):
        """Resalta el marco"""
        self.resaltado = activar
        self.update()
        
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setOpacity(self._opacidad)
        
        if self.resaltado:
            color_borde = QColor("#f39c12")
            pen = QPen(color_borde, 4)
        else:
            color_borde = QColor("#bdc3c7")
            pen = QPen(color_borde, 2)
            
        painter.setPen(pen)
        painter.setBrush(self.color_fondo)
        painter.drawRoundedRect(5, 5, self.width() - 10, self.height() - 10, 8, 8)
        
        painter.setPen(Qt.GlobalColor.black)
        
        font_marco = QFont("Segoe UI", 9, QFont.Weight.Bold)
        painter.setFont(font_marco)
        painter.drawText(10, 20, f"Marco {self.numero}")
        
        if not self.esta_libre:
            font_contenido = QFont("Segoe UI", 10)
            painter.setFont(font_contenido)
            texto = f"P{self.proceso_id}-Pág{self.num_pagina}"
            painter.drawText(10, 45, texto)
        else:
            font_libre = QFont("Segoe UI", 11, QFont.Weight.Bold)
            painter.setFont(font_libre)
            painter.setPen(QColor("#95a5a6"))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "LIBRE")

class MemoriaView(QWidget):
    """Vista de la memoria física"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.marcos_widgets = []
        self.init_ui()
        
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        
        group = QGroupBox("💾 Memoria Física (RAM)")
        group_layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.container_marcos = QWidget()
        self.layout_marcos = QGridLayout(self.container_marcos)
        self.layout_marcos.setSpacing(10)
        
        scroll.setWidget(self.container_marcos)
        group_layout.addWidget(scroll)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
    def crear_marcos(self, num_marcos: int):
        """Crea los widgets de marcos"""
        # Limpiar widgets anteriores
        for widget in self.marcos_widgets:
            widget.deleteLater()
        self.marcos_widgets.clear()
        
        columnas = 4
        
        for i in range(num_marcos):
            marco_widget = MarcoWidget(i)
            fila = i // columnas
            columna = i % columnas
            self.layout_marcos.addWidget(marco_widget, fila, columna)
            self.marcos_widgets.append(marco_widget)
            
    def actualizar_marcos(self, estado_memoria: list, procesos: dict):
        """Actualiza la visualización de marcos"""
        for i, info_marco in enumerate(estado_memoria):
            if i < len(self.marcos_widgets):
                widget = self.marcos_widgets[i]
                
                if info_marco['libre']:
                    widget.liberar()
                else:
                    proceso_id = info_marco['proceso_id']
                    color = procesos[proceso_id].color
                    widget.cargar_pagina(
                        proceso_id,
                        info_marco['num_pagina'],
                        color
                    )
    
    def resaltar_marco(self, numero_marco: int, activar: bool = True):
        """Resalta un marco específico"""
        if 0 <= numero_marco < len(self.marcos_widgets):
            self.marcos_widgets[numero_marco].resaltar(activar)
    
    def obtener_marcos_widgets(self):
        """Retorna la lista de widgets de marcos"""
        return self.marcos_widgets
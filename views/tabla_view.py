"""
VISTA: Componentes visuales para la tabla de páginas
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QTableWidget, QTableWidgetItem, QComboBox, QLabel, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class TablaView(QWidget):
    """Vista de la tabla de páginas"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        
        group = QGroupBox("📋 Tabla de Páginas")
        group_layout = QVBoxLayout()
        
        # Selector de proceso
        selector_layout = QHBoxLayout()
        lbl_proceso = QLabel("Proceso:")
        lbl_proceso.setMinimumWidth(70)
        selector_layout.addWidget(lbl_proceso)
        
        self.combo_proceso = QComboBox()
        self.combo_proceso.setToolTip(
            "Selecciona el proceso para visualizar\n"
            "su tabla de páginas asociada."
        )
        selector_layout.addWidget(self.combo_proceso)
        selector_layout.addStretch()
        
        group_layout.addLayout(selector_layout)
        
        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            "Página", "Marco", "Presente", "Modificada", "Referenciada"
        ])
        
        # Configurar tabla
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setMinimumHeight(36)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Estilo y legibilidad
        self.tabla.setStyleSheet("""
            QTableWidget {
                font-size: 13px;
                color: #2c3e50;
                background-color: white;
                gridline-color: #dcdde1;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #d6eaf8;
                color: #1b4f72;
            }
            QHeaderView::section {
                font-size: 13px;
                font-weight: bold;
                padding: 6px;
                background-color: #2c3e50;
                color: white;
                border: none;
            }
        """)
        
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.verticalHeader().setDefaultSectionSize(32)
        
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        self.tabla.setToolTip(
            "Muestra el estado de cada página:\n"
            "• Página y marco asignado\n"
            "• Presencia en memoria\n"
            "• Bits de modificación y referencia"
        )
        
        group_layout.addWidget(self.tabla)
        
        group.setLayout(group_layout)
        layout.addWidget(group)

    def obtener_combo_proceso(self):
        """Retorna el combo de procesos"""
        return self.combo_proceso
    
    def actualizar_combo_procesos(self, procesos: dict):
        """Actualiza el combo con los procesos disponibles"""
        self.combo_proceso.clear()
        for proceso_id, proceso in procesos.items():
            self.combo_proceso.addItem(f"Proceso P{proceso_id}", proceso_id)
    
    def actualizar_tabla(self, entradas: list, proceso_id: int):
        """Actualiza la tabla con las entradas de páginas"""
        self.tabla.setRowCount(len(entradas))
        
        for i, entrada in enumerate(entradas):
            # Número de página
            item_pag = QTableWidgetItem(str(entrada['numero_pagina']))
            item_pag.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_pag.setForeground(QColor("#2c3e50"))
            self.tabla.setItem(i, 0, item_pag)
            
            # Marco físico
            marco_txt = (
                str(entrada['marco_fisico'])
                if entrada['marco_fisico'] is not None else "-"
            )
            item_marco = QTableWidgetItem(marco_txt)
            item_marco.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_marco.setForeground(QColor("#2c3e50"))
            self.tabla.setItem(i, 1, item_marco)
            
            # Presente
            item_presente = QTableWidgetItem("✓" if entrada['presente'] else "✗")
            item_presente.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if entrada['presente']:
                item_presente.setBackground(QColor("#d5f4e6"))
                item_presente.setForeground(QColor("#145a32"))  # verde oscuro
            else:
                item_presente.setBackground(QColor("#fadbd8"))
                item_presente.setForeground(QColor("#922b21"))  # rojo oscuro
            self.tabla.setItem(i, 2, item_presente)
            
            # Modificada
            item_mod = QTableWidgetItem("✓" if entrada['modificada'] else "✗")
            item_mod.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_mod.setForeground(
                QColor("#1f618d") if entrada['modificada'] else QColor("#7f8c8d")
            )
            self.tabla.setItem(i, 3, item_mod)
            
            # Referenciada
            item_ref = QTableWidgetItem("✓" if entrada['referenciada'] else "✗")
            item_ref.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_ref.setForeground(
                QColor("#7d3c98") if entrada['referenciada'] else QColor("#7f8c8d")
            )
            self.tabla.setItem(i, 4, item_ref)

"""
VISTA: Estilos CSS para la aplicación
"""

def obtener_estilos():
    """Retorna los estilos CSS de la aplicación"""
    return """
    QMainWindow {
        background-color: #f5f6fa;
    }
    
    QGroupBox {
        font-weight: bold;
        border: 2px solid #dcdde1;
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 15px;
        background-color: white;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 5px 10px;
        color: #2c3e50;
    }
    
    QPushButton {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 11px;
    }
    
    QPushButton:hover {
        background-color: #2980b9;
    }
    
    QPushButton:pressed {
        background-color: #21618c;
    }
    
    QPushButton:disabled {
        background-color: #bdc3c7;
        color: #7f8c8d;
    }
    
    QPushButton#btnEjecutar {
        background-color: #27ae60;
    }
    
    QPushButton#btnEjecutar:hover {
        background-color: #229954;
    }
    
    QPushButton#btnPausa {
        background-color: #f39c12;
    }
    
    QPushButton#btnPausa:hover {
        background-color: #e67e22;
    }
    
    QPushButton#btnReset {
        background-color: #e74c3c;
    }
    
    QPushButton#btnReset:hover {
        background-color: #c0392b;
    }
    
    QSpinBox, QComboBox, QLineEdit {
        padding: 8px;
        border: 2px solid #dcdde1;
        border-radius: 5px;
        background-color: white;
        font-size: 10px;
    }
    
    QSpinBox:focus, QComboBox:focus, QLineEdit:focus {
        border: 2px solid #3498db;
    }
    
    QSlider::groove:horizontal {
        height: 8px;
        background: #dcdde1;
        border-radius: 4px;
    }
    
    QSlider::handle:horizontal {
        background: #3498db;
        width: 18px;
        height: 18px;
        margin: -5px 0;
        border-radius: 9px;
    }
    
    QSlider::handle:horizontal:hover {
        background: #2980b9;
    }
    
    QTableWidget {
        background-color: white;
        alternate-background-color: #f8f9fa;
        gridline-color: #dcdde1;
        border: 1px solid #dcdde1;
        border-radius: 5px;
    }
    
    QTableWidget::item {
        padding: 5px;
    }
    
    QTableWidget::item:selected {
        background-color: #3498db;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #34495e;
        color: white;
        padding: 8px;
        border: none;
        font-weight: bold;
    }
    
    QTextEdit {
        background-color: #2c3e50;
        color: #ecf0f1;
        border: 2px solid #34495e;
        border-radius: 5px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 10px;
        padding: 10px;
    }
    
    QLabel#lblEstadistica {
        font-size: 16px;
        font-weight: bold;
        color: #2c3e50;
        padding: 5px;
    }
    
    QLabel#lblValor {
        font-size: 20px;
        font-weight: bold;
        color: #3498db;
        padding: 5px;
    }
    """

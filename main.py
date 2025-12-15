"""
Administrador de Memoria Virtual - Patrón MVC
Punto de entrada de la aplicación
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from controllers.main_controller import MainController

def main():
    """Función principal que inicia la aplicación"""
    app = QApplication(sys.argv)
    
    # Configurar fuente predeterminada
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Crear controlador principal (MVC)
    controller = MainController()
    controller.mostrar_vista()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

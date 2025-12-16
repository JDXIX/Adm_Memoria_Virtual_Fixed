"""
Gestión de escenarios en formato JSON
"""

import json

def guardar_escenario(ruta, datos):
    """
    Guarda un escenario en un archivo JSON
    """
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)

def cargar_escenario(ruta):
    """
    Carga un escenario desde un archivo JSON
    """
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

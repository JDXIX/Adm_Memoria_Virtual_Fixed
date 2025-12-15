"""
Funciones auxiliares para la aplicación
"""

import random

def generar_color_aleatorio():
    """Genera un color aleatorio en formato hexadecimal"""
    colores = [
        "#3498db",  # Azul
        "#2ecc71",  # Verde
        "#e74c3c",  # Rojo
        "#f39c12",  # Naranja
        "#9b59b6",  # Morado
        "#1abc9c",  # Turquesa
        "#34495e",  # Gris oscuro
        "#e67e22",  # Naranja oscuro
    ]
    return random.choice(colores)

def formatear_secuencia(secuencia: list, max_length: int = 50) -> str:
    """
    Formatea una secuencia para mostrar
    
    Args:
        secuencia: Lista de números de página
        max_length: Longitud máxima del string resultante
        
    Returns:
        String formateado de la secuencia
    """
    sec_str = ",".join(map(str, secuencia))
    if len(sec_str) > max_length:
        return sec_str[:max_length] + "..."
    return sec_str

"""
Módulo de vistas (VISTA en MVC)
Contiene todos los componentes visuales
"""

from .main_view import MainView
from .memoria_view import MemoriaView, MarcoWidget
from .tabla_view import TablaView
from .simulacion_view import SimulacionView, LogWidget, EstadisticaWidget
from .styles import obtener_estilos

__all__ = [
    'MainView',
    'MemoriaView', 'MarcoWidget',
    'TablaView',
    'SimulacionView', 'LogWidget', 'EstadisticaWidget',
    'obtener_estilos'
]

"""
Módulo de modelos (MODELO en MVC)
Contiene toda la lógica de negocio
"""

from .memoria_model import MemoriaFisica, Marco, Pagina
from .proceso_model import Proceso, TablaPaginas, EntradaTablaPaginas
from .algoritmos_model import (AlgoritmoReemplazo, FIFO, LRU, 
                               NRU, CLOCK, OPT)
from .simulador_model import Simulador, EventoSimulacion

__all__ = [
    'MemoriaFisica', 'Marco', 'Pagina',
    'Proceso', 'TablaPaginas', 'EntradaTablaPaginas',
    'AlgoritmoReemplazo', 'FIFO', 'LRU', 'NRU', 'CLOCK', 'OPT',
    'Simulador', 'EventoSimulacion'
]

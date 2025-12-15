"""
MODELO: Algoritmos de reemplazo de páginas
Lógica de negocio para algoritmos
"""

from abc import ABC, abstractmethod
from typing import Optional

class AlgoritmoReemplazo(ABC):
    """Clase base para algoritmos de reemplazo"""
    
    def __init__(self):
        self.nombre = "Base"
        
    @abstractmethod
    def seleccionar_victima(self, memoria, proceso_id: Optional[int] = None):
        """Selecciona el marco a reemplazar"""
        pass
    
    def resetear(self):
        """Resetea el estado del algoritmo"""
        pass

class FIFO(AlgoritmoReemplazo):
    """First In, First Out - Reemplaza la página más antigua"""
    
    def __init__(self):
        super().__init__()
        self.nombre = "FIFO"
        
    def seleccionar_victima(self, memoria, proceso_id: Optional[int] = None):
        marcos_candidatos = memoria.obtener_marcos_ocupados()
        
        if proceso_id is not None:
            marcos_candidatos = [m for m in marcos_candidatos 
                               if m.pagina.proceso_id == proceso_id]
        
        victima = min(marcos_candidatos, key=lambda m: m.tiempo_carga)
        return victima

class LRU(AlgoritmoReemplazo):
    """Least Recently Used - Reemplaza la página menos recientemente usada"""
    
    def __init__(self):
        super().__init__()
        self.nombre = "LRU"
        
    def seleccionar_victima(self, memoria, proceso_id: Optional[int] = None):
        marcos_candidatos = memoria.obtener_marcos_ocupados()
        
        if proceso_id is not None:
            marcos_candidatos = [m for m in marcos_candidatos 
                               if m.pagina.proceso_id == proceso_id]
        
        victima = min(marcos_candidatos, key=lambda m: m.tiempo_acceso)
        return victima

class NRU(AlgoritmoReemplazo):
    """Not Recently Used - Usa bits de referencia y modificación"""
    
    def __init__(self):
        super().__init__()
        self.nombre = "NRU"
        
    def seleccionar_victima(self, memoria, proceso_id: Optional[int] = None):
        marcos_candidatos = memoria.obtener_marcos_ocupados()
        
        if proceso_id is not None:
            marcos_candidatos = [m for m in marcos_candidatos 
                               if m.pagina.proceso_id == proceso_id]
        
        def obtener_clase(marco) -> int:
            r = 1 if marco.pagina.referenciada else 0
            m = 1 if marco.pagina.modificada else 0
            return r * 2 + m
        
        victima = min(marcos_candidatos, key=obtener_clase)
        return victima

class CLOCK(AlgoritmoReemplazo):
    """Algoritmo del reloj - Variante eficiente de LRU"""
    
    def __init__(self):
        super().__init__()
        self.nombre = "CLOCK"
        self.puntero = 0
        
    def seleccionar_victima(self, memoria, proceso_id: Optional[int] = None):
        marcos_candidatos = memoria.marcos
        
        if proceso_id is not None:
            marcos_candidatos = [m for m in marcos_candidatos 
                               if not m.esta_libre() and m.pagina.proceso_id == proceso_id]
        else:
            marcos_candidatos = memoria.obtener_marcos_ocupados()
        
        if not marcos_candidatos:
            return memoria.marcos[0]
        
        intentos = 0
        max_intentos = len(marcos_candidatos) * 2
        
        while intentos < max_intentos:
            marco_actual = marcos_candidatos[self.puntero % len(marcos_candidatos)]
            
            if not marco_actual.pagina.referenciada:
                victima = marco_actual
                self.puntero = (self.puntero + 1) % len(marcos_candidatos)
                return victima
            else:
                marco_actual.pagina.referenciada = False
                self.puntero = (self.puntero + 1) % len(marcos_candidatos)
            
            intentos += 1
        
        victima = marcos_candidatos[self.puntero % len(marcos_candidatos)]
        self.puntero = (self.puntero + 1) % len(marcos_candidatos)
        return victima
    
    def resetear(self):
        self.puntero = 0

class OPT(AlgoritmoReemplazo):
    """Óptimo - Reemplaza la página que no se usará por más tiempo"""
    
    def __init__(self):
        super().__init__()
        self.nombre = "OPT"
        self.secuencia_futura = []
        self.indice_actual = 0
        
    def establecer_secuencia(self, secuencia: list, indice: int):
        """Establece la secuencia futura de accesos"""
        self.secuencia_futura = secuencia
        self.indice_actual = indice
        
    def seleccionar_victima(self, memoria, proceso_id: Optional[int] = None):
        marcos_candidatos = memoria.obtener_marcos_ocupados()
        
        if proceso_id is not None:
            marcos_candidatos = [m for m in marcos_candidatos 
                               if m.pagina.proceso_id == proceso_id]
        
        def proximo_uso(marco) -> int:
            num_pagina = marco.pagina.numero
            try:
                for i in range(self.indice_actual, len(self.secuencia_futura)):
                    if self.secuencia_futura[i] == num_pagina:
                        return i - self.indice_actual
                return float('inf')
            except:
                return float('inf')
        
        victima = max(marcos_candidatos, key=proximo_uso)
        return victima
    
    def resetear(self):
        self.secuencia_futura = []
        self.indice_actual = 0

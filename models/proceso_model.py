"""
MODELO: Gestión de procesos y tablas de páginas
Lógica de negocio para procesos
"""

from typing import Optional, Dict
from dataclasses import dataclass

@dataclass
class EntradaTablaPaginas:
    """Entrada en la tabla de páginas"""
    numero_pagina: int
    marco_fisico: Optional[int] = None
    presente: bool = False
    modificada: bool = False
    referenciada: bool = False
    
    def obtener_info(self) -> dict:
        """Retorna información para la vista"""
        return {
            'numero_pagina': self.numero_pagina,
            'marco_fisico': self.marco_fisico if self.presente else None,
            'presente': self.presente,
            'modificada': self.modificada,
            'referenciada': self.referenciada
        }

class TablaPaginas:
    """Tabla de páginas de un proceso"""
    
    def __init__(self, num_paginas: int):
        self.num_paginas = num_paginas
        self.entradas: Dict[int, EntradaTablaPaginas] = {
            i: EntradaTablaPaginas(i) for i in range(num_paginas)
        }
    
    def actualizar_entrada(self, num_pagina: int, marco: Optional[int], 
                          presente: bool, modificada: bool = False):
        """Actualiza una entrada de la tabla"""
        if num_pagina in self.entradas:
            entrada = self.entradas[num_pagina]
            entrada.marco_fisico = marco
            entrada.presente = presente
            entrada.modificada = modificada
    
    def marcar_referenciada(self, num_pagina: int):
        """Marca una página como referenciada"""
        if num_pagina in self.entradas:
            self.entradas[num_pagina].referenciada = True
    
    def limpiar_bits_referencia(self):
        """Limpia todos los bits de referencia"""
        for entrada in self.entradas.values():
            entrada.referenciada = False
    
    def obtener_entrada(self, num_pagina: int) -> Optional[EntradaTablaPaginas]:
        """Obtiene una entrada específica"""
        return self.entradas.get(num_pagina)
    
    def obtener_todas_entradas(self) -> list:
        """Retorna todas las entradas para la vista"""
        return [entrada.obtener_info() for entrada in self.entradas.values()]

class Proceso:
    """Representa un proceso del sistema"""
    
    def __init__(self, proceso_id: int, num_paginas_virtuales: int, color: str = "#3498db"):
        self.id = proceso_id
        self.num_paginas_virtuales = num_paginas_virtuales
        self.color = color
        self.tabla_paginas = TablaPaginas(num_paginas_virtuales)
        self.secuencia_accesos = []
        self.indice_acceso_actual = 0
        
        # Estadísticas
        self.total_accesos = 0
        self.page_faults = 0
        self.page_hits = 0
        
    def generar_secuencia_aleatoria(self, longitud: int):
        """Genera secuencia aleatoria de accesos"""
        import random
        self.secuencia_accesos = [
            random.randint(0, self.num_paginas_virtuales - 1) 
            for _ in range(longitud)
        ]
        self.indice_acceso_actual = 0
        
    def establecer_secuencia(self, secuencia: list):
        """Establece una secuencia específica de accesos"""
        self.secuencia_accesos = secuencia
        self.indice_acceso_actual = 0
        
    def obtener_siguiente_acceso(self) -> Optional[int]:
        """Obtiene el siguiente acceso de la secuencia"""
        if self.indice_acceso_actual < len(self.secuencia_accesos):
            acceso = self.secuencia_accesos[self.indice_acceso_actual]
            self.indice_acceso_actual += 1
            return acceso
        return None
    
    def tiene_mas_accesos(self) -> bool:
        """Verifica si quedan más accesos en la secuencia"""
        return self.indice_acceso_actual < len(self.secuencia_accesos)
    
    def registrar_hit(self):
        """Registra un page hit"""
        self.total_accesos += 1
        self.page_hits += 1
        
    def registrar_fault(self):
        """Registra un page fault"""
        self.total_accesos += 1
        self.page_faults += 1
        
    def obtener_tasa_fallos(self) -> float:
        """Calcula la tasa de fallos"""
        if self.total_accesos == 0:
            return 0.0
        return (self.page_faults / self.total_accesos) * 100
    
    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas para la vista"""
        return {
            'proceso_id': self.id,
            'total_accesos': self.total_accesos,
            'page_faults': self.page_faults,
            'page_hits': self.page_hits,
            'tasa_fallos': self.obtener_tasa_fallos()
        }
    
    def resetear_estadisticas(self):
        """Resetea las estadísticas"""
        self.total_accesos = 0
        self.page_faults = 0
        self.page_hits = 0
        self.indice_acceso_actual = 0
        
    def obtener_info_completa(self) -> dict:
        """Retorna información completa para la vista"""
        return {
            'id': self.id,
            'color': self.color,
            'num_paginas': self.num_paginas_virtuales,
            'secuencia': self.secuencia_accesos,
            'indice_actual': self.indice_acceso_actual,
            'estadisticas': self.obtener_estadisticas()
        }
    
    def __str__(self):
        return f"Proceso P{self.id} - Páginas: {self.num_paginas_virtuales}"

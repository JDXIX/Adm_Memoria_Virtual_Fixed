"""
MODELO: Gestión de memoria física
Lógica de negocio para memoria, marcos y páginas
"""

from typing import Optional
from dataclasses import dataclass

@dataclass
class Pagina:
    """Representa una página de memoria virtual"""
    numero: int
    proceso_id: int
    modificada: bool = False
    referenciada: bool = False
    
    def __str__(self):
        return f"P{self.proceso_id}-Pág{self.numero}"

class Marco:
    """Representa un marco de página en memoria física"""
    
    def __init__(self, numero: int):
        self.numero = numero
        self.pagina: Optional[Pagina] = None
        self.tiempo_carga = 0
        self.tiempo_acceso = 0
        
    def esta_libre(self) -> bool:
        """Verifica si el marco está libre"""
        return self.pagina is None
    
    def cargar_pagina(self, pagina: Pagina, tiempo: int):
        """Carga una página en el marco"""
        self.pagina = pagina
        self.tiempo_carga = tiempo
        self.tiempo_acceso = tiempo
        
    def liberar(self):
        """Libera el marco"""
        self.pagina = None
        self.tiempo_carga = 0
        self.tiempo_acceso = 0
        
    def acceder(self, tiempo: int):
        """Registra un acceso al marco"""
        self.tiempo_acceso = tiempo
        if self.pagina:
            self.pagina.referenciada = True
            
    def obtener_info(self) -> dict:
        """Retorna información del marco para la vista"""
        return {
            'numero': self.numero,
            'libre': self.esta_libre(),
            'proceso_id': self.pagina.proceso_id if self.pagina else None,
            'num_pagina': self.pagina.numero if self.pagina else None,
            'tiempo_carga': self.tiempo_carga,
            'tiempo_acceso': self.tiempo_acceso
        }
    
    def __str__(self):
        if self.esta_libre():
            return f"Marco {self.numero}: LIBRE"
        return f"Marco {self.numero}: {self.pagina}"

class MemoriaFisica:
    """Gestiona la memoria física (RAM)"""
    
    def __init__(self, num_marcos: int):
        self.num_marcos = num_marcos
        self.marcos = [Marco(i) for i in range(num_marcos)]
        
    def obtener_marco_libre(self) -> Optional[Marco]:
        """Busca y retorna un marco libre"""
        for marco in self.marcos:
            if marco.esta_libre():
                return marco
        return None
    
    def tiene_marcos_libres(self) -> bool:
        """Verifica si hay marcos libres"""
        return any(marco.esta_libre() for marco in self.marcos)
    
    def buscar_pagina(self, proceso_id: int, num_pagina: int) -> Optional[Marco]:
        """Busca una página específica en memoria"""
        for marco in self.marcos:
            if not marco.esta_libre():
                pagina = marco.pagina
                if pagina.proceso_id == proceso_id and pagina.numero == num_pagina:
                    return marco
        return None
    
    def obtener_marcos_ocupados(self) -> list:
        """Retorna lista de marcos ocupados"""
        return [m for m in self.marcos if not m.esta_libre()]
    
    def obtener_marcos_del_proceso(self, proceso_id: int) -> list:
        """Retorna marcos ocupados por un proceso específico"""
        return [m for m in self.marcos 
                if not m.esta_libre() and m.pagina.proceso_id == proceso_id]
    
    def obtener_estado_completo(self) -> list:
        """Retorna el estado completo para la vista"""
        return [marco.obtener_info() for marco in self.marcos]
    
    def resetear(self):
        """Limpia toda la memoria"""
        for marco in self.marcos:
            marco.liberar()
    
    def __str__(self):
        return "\n".join(str(marco) for marco in self.marcos)

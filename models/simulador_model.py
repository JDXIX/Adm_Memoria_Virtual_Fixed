"""
MODELO: Motor de simulación del sistema de memoria virtual
Lógica de negocio para la simulación
"""

from typing import Optional
from .memoria_model import Pagina
from .algoritmos_model import OPT

class EventoSimulacion:
    """Representa un evento durante la simulación"""
    
    def __init__(self, tipo: str, proceso_id: int, num_pagina: int, 
                 marco: Optional[int] = None, mensaje: str = ""):
        self.tipo = tipo  # "HIT", "FAULT", "CARGA", "REEMPLAZO"
        self.proceso_id = proceso_id
        self.num_pagina = num_pagina
        self.marco = marco
        self.mensaje = mensaje
        self.timestamp = 0
        
    def obtener_info(self) -> dict:
        """Retorna información del evento para la vista"""
        return {
            'tipo': self.tipo,
            'proceso_id': self.proceso_id,
            'num_pagina': self.num_pagina,
            'marco': self.marco,
            'mensaje': self.mensaje,
            'timestamp': self.timestamp
        }
        
    def __str__(self):
        return self.mensaje

class Simulador:
    """Simulador del sistema de memoria virtual"""
    
    def __init__(self, num_marcos: int, algoritmo):
        from .memoria_model import MemoriaFisica
        self.memoria = MemoriaFisica(num_marcos)
        self.algoritmo = algoritmo
        self.procesos = {}
        self.tiempo_actual = 0
        self.eventos = []
        
    def agregar_proceso(self, proceso):
        """Agrega un proceso al simulador"""
        self.procesos[proceso.id] = proceso
        
    def ejecutar_paso(self) -> Optional[EventoSimulacion]:
        """Ejecuta un paso de la simulación"""
        proceso_activo = None
        for proceso in self.procesos.values():
            if proceso.tiene_mas_accesos():
                proceso_activo = proceso
                break
        
        if not proceso_activo:
            return None
        
        num_pagina = proceso_activo.obtener_siguiente_acceso()
        if num_pagina is None:
            return None
        
        self.tiempo_actual += 1
        
        marco = self.memoria.buscar_pagina(proceso_activo.id, num_pagina)
        
        if marco:
            # PAGE HIT
            marco.acceder(self.tiempo_actual)
            proceso_activo.registrar_hit()
            proceso_activo.tabla_paginas.marcar_referenciada(num_pagina)
            
            evento = EventoSimulacion(
                "HIT",
                proceso_activo.id,
                num_pagina,
                marco.numero,
                f"✓ HIT: P{proceso_activo.id} accede a página {num_pagina} en marco {marco.numero}"
            )
            evento.timestamp = self.tiempo_actual
            self.eventos.append(evento)
            return evento
        else:
            # PAGE FAULT
            proceso_activo.registrar_fault()
            
            marco_libre = self.memoria.obtener_marco_libre()
            
            if marco_libre:
                # Hay espacio disponible
                nueva_pagina = Pagina(num_pagina, proceso_activo.id)
                marco_libre.cargar_pagina(nueva_pagina, self.tiempo_actual)
                
                proceso_activo.tabla_paginas.actualizar_entrada(
                    num_pagina, marco_libre.numero, True
                )
                
                evento = EventoSimulacion(
                    "CARGA",
                    proceso_activo.id,
                    num_pagina,
                    marco_libre.numero,
                    f"⚠ FAULT: P{proceso_activo.id} página {num_pagina} → Cargada en marco {marco_libre.numero}"
                )
                evento.timestamp = self.tiempo_actual
                self.eventos.append(evento)
                return evento
            else:
                # Necesitamos reemplazar
                if isinstance(self.algoritmo, OPT):
                    self.algoritmo.establecer_secuencia(
                        proceso_activo.secuencia_accesos,
                        proceso_activo.indice_acceso_actual
                    )
                
                marco_victima = self.algoritmo.seleccionar_victima(
                    self.memoria, proceso_activo.id
                )
                
                pagina_antigua = marco_victima.pagina
                proceso_antiguo = self.procesos[pagina_antigua.proceso_id]
                
                proceso_antiguo.tabla_paginas.actualizar_entrada(
                    pagina_antigua.numero, None, False
                )
                
                nueva_pagina = Pagina(num_pagina, proceso_activo.id)
                marco_victima.cargar_pagina(nueva_pagina, self.tiempo_actual)
                
                proceso_activo.tabla_paginas.actualizar_entrada(
                    num_pagina, marco_victima.numero, True
                )
                
                evento = EventoSimulacion(
                    "REEMPLAZO",
                    proceso_activo.id,
                    num_pagina,
                    marco_victima.numero,
                    f"⚠ FAULT: P{proceso_activo.id} página {num_pagina} → "
                    f"Reemplaza P{pagina_antigua.proceso_id}-Pág{pagina_antigua.numero} "
                    f"en marco {marco_victima.numero} ({self.algoritmo.nombre})"
                )
                evento.timestamp = self.tiempo_actual
                self.eventos.append(evento)
                return evento
    
    def ejecutar_todo(self) -> list:
        """Ejecuta toda la simulación"""
        eventos = []
        while True:
            evento = self.ejecutar_paso()
            if evento is None:
                break
            eventos.append(evento)
        return eventos
    
    def resetear(self):
        """Resetea el simulador"""
        self.memoria.resetear()
        self.tiempo_actual = 0
        self.eventos = []
        self.algoritmo.resetear()
        
        for proceso in self.procesos.values():
            proceso.resetear_estadisticas()
    
    def obtener_estadisticas(self) -> dict:
        """Obtiene estadísticas generales"""
        total_accesos = sum(p.total_accesos for p in self.procesos.values())
        total_faults = sum(p.page_faults for p in self.procesos.values())
        total_hits = sum(p.page_hits for p in self.procesos.values())
        
        tasa_fallos = (total_faults / total_accesos * 100) if total_accesos > 0 else 0
        
        return {
            "accesos_totales": total_accesos,
            "page_faults": total_faults,
            "page_hits": total_hits,
            "tasa_fallos": tasa_fallos,
            "marcos_usados": len(self.memoria.obtener_marcos_ocupados()),
            "marcos_totales": self.memoria.num_marcos
        }

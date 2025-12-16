"""
VISTA: Componentes visuales para simulación y estadísticas
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QPushButton, QSpinBox, QLineEdit,
    QTextEdit
)
from PyQt6.QtCore import Qt


class LogWidget(QTextEdit):
    """Widget para el log de eventos"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setMaximumHeight(200)

    def agregar_evento(self, mensaje: str, tipo: str = "INFO"):
        """Agrega un evento al log"""
        color_map = {
            "HIT": "#27ae60",
            "FAULT": "#e74c3c",
            "CARGA": "#f39c12",
            "REEMPLAZO": "#e67e22",
            "INFO": "#3498db"
        }

        color = color_map.get(tipo, "#ecf0f1")
        html = f'<span style="color: {color};">• {mensaje}</span><br>'
        self.insertHtml(html)

        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum()
        )

    def limpiar(self):
        """Limpia el log"""
        self.clear()


class EstadisticaWidget(QWidget):
    """Widget para mostrar una estadística"""

    def __init__(self, titulo: str, valor_inicial: str = "0", parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.lbl_titulo = QLabel(titulo)
        self.lbl_titulo.setObjectName("lblEstadistica")
        self.lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_titulo)

        self.lbl_valor = QLabel(valor_inicial)
        self.lbl_valor.setObjectName("lblValor")
        self.lbl_valor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_valor)

        self.setStyleSheet("""
            EstadisticaWidget {
                background-color: white;
                border: 2px solid #dcdde1;
                border-radius: 8px;
            }
        """)

    def actualizar_valor(self, valor):
        """Actualiza el valor mostrado"""
        self.lbl_valor.setText(str(valor))


class SimulacionView(QWidget):
    """Vista de simulación y controles"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)

        group = QGroupBox("🎮 Simulación y Estadísticas")
        group_layout = QVBoxLayout()

        # ─────────────────────────────────────────────
        # Configuración del proceso
        # ─────────────────────────────────────────────
        layout_proceso = QHBoxLayout()

        # Páginas virtuales
        box_paginas = QGroupBox("📄 Páginas Virtuales")
        box_paginas_layout = QVBoxLayout()

        self.spin_paginas = QSpinBox()
        self.spin_paginas.setMinimum(5)
        self.spin_paginas.setMaximum(50)
        self.spin_paginas.setValue(10)
        self.spin_paginas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_paginas.setFixedHeight(36)
        self.spin_paginas.setToolTip(
            "Cantidad total de páginas virtuales\n"
            "disponibles para el proceso."
        )

        box_paginas_layout.addWidget(self.spin_paginas)
        box_paginas.setLayout(box_paginas_layout)
        layout_proceso.addWidget(box_paginas)

        # Secuencia
        box_secuencia = QGroupBox("🔁 Secuencia de Referencias")
        box_seq_layout = QVBoxLayout()

        self.txt_secuencia = QLineEdit()
        self.txt_secuencia.setPlaceholderText("Ejemplo: 1,2,3,4,1,2,5")
        self.txt_secuencia.setFixedHeight(36)
        self.txt_secuencia.setToolTip(
            "Secuencia de accesos a memoria\n"
            "separada por comas."
        )

        box_seq_layout.addWidget(self.txt_secuencia)
        box_secuencia.setLayout(box_seq_layout)
        layout_proceso.addWidget(box_secuencia)

        # Botones de carga de secuencia
        self.btn_generar = QPushButton("🎲 Generar secuencia")
        self.btn_generar.setFixedHeight(36)
        self.btn_generar.setToolTip("Genera una secuencia aleatoria")
        layout_proceso.addWidget(self.btn_generar)

        self.btn_cargar = QPushButton("📥 Usar secuencia manual")
        self.btn_cargar.setFixedHeight(36)
        self.btn_cargar.setToolTip("Usa la secuencia escrita manualmente")
        layout_proceso.addWidget(self.btn_cargar)

        layout_proceso.addStretch()
        group_layout.addLayout(layout_proceso)

        # ─────────────────────────────────────────────
        # Controles de simulación
        # ─────────────────────────────────────────────
        layout_controles = QHBoxLayout()

        self.btn_ejecutar = QPushButton("▶ Ejecutar")
        self.btn_ejecutar.setObjectName("btnEjecutar")
        self.btn_ejecutar.setFixedHeight(36)
        layout_controles.addWidget(self.btn_ejecutar)

        self.btn_paso = QPushButton("⏭ Paso a Paso")
        self.btn_paso.setFixedHeight(36)
        layout_controles.addWidget(self.btn_paso)

        self.btn_pausa = QPushButton("⏸ Pausar")
        self.btn_pausa.setObjectName("btnPausa")
        self.btn_pausa.setEnabled(False)
        self.btn_pausa.setFixedHeight(36)
        layout_controles.addWidget(self.btn_pausa)

        self.btn_reset = QPushButton("🔄 Resetear")
        self.btn_reset.setObjectName("btnReset")
        self.btn_reset.setFixedHeight(36)
        layout_controles.addWidget(self.btn_reset)

        # ── NUEVOS BOTONES JSON ──
        self.btn_guardar_json = QPushButton("💾 Guardar Escenario")
        self.btn_guardar_json.setFixedHeight(36)
        self.btn_guardar_json.setToolTip("Guarda la configuración en un archivo JSON")
        layout_controles.addWidget(self.btn_guardar_json)

        self.btn_cargar_json = QPushButton("📂 Cargar Escenario")
        self.btn_cargar_json.setFixedHeight(36)
        self.btn_cargar_json.setToolTip("Carga un escenario desde un archivo JSON")
        layout_controles.addWidget(self.btn_cargar_json)

        layout_controles.addStretch()
        group_layout.addLayout(layout_controles)

        # ─────────────────────────────────────────────
        # Estadísticas
        # ─────────────────────────────────────────────
        layout_stats = QHBoxLayout()

        self.stat_accesos = EstadisticaWidget("Accesos Totales", "0")
        self.stat_faults = EstadisticaWidget("Fallos de Página", "0")
        self.stat_hits = EstadisticaWidget("Aciertos de Página", "0")
        self.stat_tasa = EstadisticaWidget("Tasa de Fallos", "0.00%")

        layout_stats.addWidget(self.stat_accesos)
        layout_stats.addWidget(self.stat_faults)
        layout_stats.addWidget(self.stat_hits)
        layout_stats.addWidget(self.stat_tasa)

        group_layout.addLayout(layout_stats)

        # Log
        lbl_log = QLabel("📝 Log de eventos:")
        group_layout.addWidget(lbl_log)

        self.log_widget = LogWidget()
        group_layout.addWidget(self.log_widget)

        group.setLayout(group_layout)
        layout.addWidget(group)

    def obtener_controles(self) -> dict:
        """Retorna un diccionario con todos los controles"""
        return {
            'spin_paginas': self.spin_paginas,
            'txt_secuencia': self.txt_secuencia,
            'btn_generar': self.btn_generar,
            'btn_cargar': self.btn_cargar,
            'btn_ejecutar': self.btn_ejecutar,
            'btn_paso': self.btn_paso,
            'btn_pausa': self.btn_pausa,
            'btn_reset': self.btn_reset,
            'btn_guardar_json': self.btn_guardar_json,
            'btn_cargar_json': self.btn_cargar_json,
            'log': self.log_widget
        }

    def actualizar_estadisticas(self, stats: dict):
        """Actualiza las estadísticas"""
        self.stat_accesos.actualizar_valor(stats["accesos_totales"])
        self.stat_faults.actualizar_valor(stats["page_faults"])
        self.stat_hits.actualizar_valor(stats["page_hits"])
        self.stat_tasa.actualizar_valor(f"{stats['tasa_fallos']:.2f}%")

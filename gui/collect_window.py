from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QSpinBox
from PyQt5.QtCore import Qt
import threading

from data.collector import collect_data_for_action
from config.settings import ACTIONS, NO_SEQUENCES

class CollectDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recopilar datos")
        self.setFixedSize(350, 250)

        # Título
        title = QLabel("Selecciona la acción a recopilar")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        # ComboBox para elegir la acción
        self.combo = QComboBox()
        self.combo.addItems(ACTIONS)
        self.combo.setFixedHeight(30)

        # SpinBox para seleccionar la secuencia inicial
        seq_label = QLabel("Secuencia inicial:")
        seq_label.setAlignment(Qt.AlignCenter)
        self.seq_spin = QSpinBox()
        self.seq_spin.setRange(0, 1000)  # Ajusta según tus necesidades
        self.seq_spin.setValue(0)
        self.seq_spin.setFixedHeight(30)

        # Botón para iniciar la recolección
        btn_start = QPushButton("Iniciar recolección")
        btn_start.setFixedHeight(40)
        btn_start.clicked.connect(self.start_collection)

        # Botón para cerrar
        btn_close = QPushButton("Volver")
        btn_close.setFixedHeight(35)
        btn_close.clicked.connect(self.close)

        # Layout
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(title)
        layout.addWidget(self.combo)
        layout.addWidget(seq_label)
        layout.addWidget(self.seq_spin)
        layout.addWidget(btn_start)
        layout.addWidget(btn_close)

        self.setLayout(layout)

    def start_collection(self):
        action = self.combo.currentText()
        start_seq = self.seq_spin.value()  # Obtenemos la secuencia inicial
        thread = threading.Thread(
            target=collect_data_for_action,
            args=(action, start_seq),
            daemon=True
        )
        thread.start()

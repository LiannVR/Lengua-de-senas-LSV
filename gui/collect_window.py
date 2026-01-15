from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QSpinBox, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import threading

from data.collector import collect_data_for_action, create_folders_for_action
from config.settings import NO_SEQUENCES
from config.actions import load_actions

ACTIONS = load_actions()

class CollectDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recopilar datos")
        self.setFixedSize(400, 300)

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

        # Input para el nombre de la acción
        action_label = QLabel("Nombre de la nueva seña:")
        action_label.setAlignment(Qt.AlignCenter)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Nombre de la nueva seña")
        self.input.setFixedHeight(30)

        # Botón para crear la acción
        btn = QPushButton("Crear acción")
        btn.clicked.connect(self.create_action)


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
        layout.addWidget(action_label)
        layout.addWidget(self.input)
        layout.addWidget(btn)
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

    def create_action(self):
        action = self.input.text().strip().lower().replace(" ", "_")

        if not action:
            QMessageBox.warning(self, "Error", "Nombre inválido")
            return

        create_folders_for_action(action)
        #print(action)

        ACTIONS = load_actions()  # Recargamos las acciones
        self.combo.clear()
        self.combo.addItems(ACTIONS)
        self.combo.setCurrentText(action)
        QMessageBox.information(self, "OK", f"'{action}' creada")
        self.input.clear()
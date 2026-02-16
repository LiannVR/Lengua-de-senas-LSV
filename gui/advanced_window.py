# gui/advanced_window.py
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PyQt5.QtCore import Qt

from gui.collect_window import CollectDataWindow
from gui.train_window import TrainModelWindow


class AdvancedWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Configuración avanzada")
        self.setFixedSize(360, 250)

        title = QLabel("Opciones avanzadas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        btn_collect = QPushButton("📦 Recolectar datos")
        btn_train = QPushButton("🧠 Entrenar modelo")
        btn_close = QPushButton("⬅ Volver")

        btn_collect.setFixedHeight(40)
        btn_train.setFixedHeight(40)
        btn_close.setFixedHeight(35)

        btn_collect.clicked.connect(self.open_collect)
        btn_train.clicked.connect(self.open_train)
        btn_close.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(btn_collect)
        layout.addWidget(btn_train)
        layout.addStretch()
        layout.addWidget(btn_close)

        self.setLayout(layout)

    def open_collect(self):
        self.collect_window = CollectDataWindow()
        self.collect_window.show()

    def open_train(self):
        self.train_window = TrainModelWindow()
        self.train_window.show()

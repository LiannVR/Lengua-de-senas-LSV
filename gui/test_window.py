# gui/test_window.py
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel
)
from PyQt5.QtCore import Qt
import threading

from realtime.inference import realtime_test


class TestModelWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Probar modelo en tiempo real")
        self.setFixedSize(350, 200)

        title = QLabel("Prueba del modelo")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        btn_start = QPushButton("🎥 Iniciar prueba")
        btn_start.setFixedHeight(40)
        btn_start.clicked.connect(self.start_test)

        btn_close = QPushButton("❌ Volver")
        btn_close.setFixedHeight(35)
        btn_close.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(title)
        layout.addWidget(btn_start)
        layout.addWidget(btn_close)

        self.setLayout(layout)

    def start_test(self):
        """
        Ejecutamos realtime_test en un hilo
        para no congelar la GUI
        """
        thread = threading.Thread(target=realtime_test, daemon=True)
        thread.start()

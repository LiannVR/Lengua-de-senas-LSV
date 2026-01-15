# gui/train_window.py
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox
)
from PyQt5.QtCore import Qt
import threading

from model.train import train_model


class TrainModelWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Entrenar modelo")
        self.setFixedSize(350, 200)

        title = QLabel("Entrenamiento del modelo")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        info = QLabel(
            "Este proceso puede tardar varios minutos.\n"
            "No cierres la aplicación durante el entrenamiento."
        )
        info.setAlignment(Qt.AlignCenter)
        info.setWordWrap(True)

        self.btn_start = QPushButton("Iniciar entrenamiento")
        self.btn_start.setFixedHeight(40)
        self.btn_start.clicked.connect(self.start_training)

        self.btn_close = QPushButton("Volver")
        self.btn_close.setFixedHeight(35)
        self.btn_close.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_close)

        self.setLayout(layout)

    def start_training(self):
        self.btn_start.setEnabled(False)

        thread = threading.Thread(
            target=self.run_training,
            daemon=True
        )
        thread.start()

    def run_training(self):
        try:
            train_model()
            QMessageBox.information(
                self,
                "Entrenamiento completado",
                "El modelo se entrenó correctamente."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )
        finally:
            self.btn_start.setEnabled(True)

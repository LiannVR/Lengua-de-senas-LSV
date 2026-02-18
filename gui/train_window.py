# gui/train_window.py
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox
)

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QMovie

from model.train import train_model


class TrainWorker(QThread):
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def run(self):
        try:
            train_model()
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))


class TrainModelWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Entrenar modelo")
        self.setFixedSize(350, 250)

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

        # 🔄 Spinner
        self.spinner_label = QLabel()
        self.spinner_label.setAlignment(Qt.AlignCenter)

        self.spinner = QMovie("gui/assets/spinner.gif")
        self.spinner.setScaledSize(QSize(32, 32))  # ← tamaño aquí
        self.spinner_label.setMovie(self.spinner)
        self.spinner_label.setVisible(False)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.spinner_label)
        layout.addWidget(self.btn_close)

        self.setLayout(layout)

        self.worker = None

    def start_training(self):
        self.btn_start.setEnabled(False)
        self.spinner_label.setVisible(True)
        self.spinner.start()

        self.worker = TrainWorker()
        self.worker.finished_signal.connect(self.training_finished)
        self.worker.error_signal.connect(self.training_error)
        self.worker.start()

    def training_finished(self):
        self.spinner.stop()
        self.spinner_label.setVisible(False)

        QMessageBox.information(
            self,
            "Entrenamiento completado",
            "El modelo se entrenó correctamente."
        )

        self.btn_start.setEnabled(True)

    def training_error(self, error_msg):
        self.spinner.stop()
        self.spinner_label.setVisible(False)

        QMessageBox.critical(
            self,
            "Error",
            error_msg
        )

        self.btn_start.setEnabled(True)


""" # gui/train_window.py
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from model.train import train_model


# 🔹 Worker que corre en segundo plano
class TrainWorker(QThread):
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def run(self):
        try:
            train_model()
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))


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

        self.worker = None

    def start_training(self):
        self.btn_start.setEnabled(False)

        self.worker = TrainWorker()
        self.worker.finished_signal.connect(self.training_finished)
        self.worker.error_signal.connect(self.training_error)
        self.worker.start()

    def training_finished(self):
        QMessageBox.information(
            self,
            "Entrenamiento completado",
            "El modelo se entrenó correctamente."
        )
        self.btn_start.setEnabled(True)

    def training_error(self, error_msg):
        QMessageBox.critical(
            self,
            "Error",
            error_msg
        )
        self.btn_start.setEnabled(True)

 """
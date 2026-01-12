import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QMessageBox
)
from PyQt5.QtCore import Qt

from data.collector import collect_data
from model.train import train_model
from realtime.inference import realtime_test


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lenguaje de Señas - LSTM")
        self.setGeometry(200, 200, 400, 350)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Reconocimiento de Lenguaje de Señas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        btn_collect = QPushButton("📸 Recolectar datos")
        btn_train = QPushButton("🧠 Entrenar modelo")
        btn_test = QPushButton("🎥 Testeo en tiempo real")

        btn_collect.clicked.connect(self.run_collector)
        btn_train.clicked.connect(self.run_training)
        btn_test.clicked.connect(self.run_realtime)

        layout.addWidget(btn_collect)
        layout.addWidget(btn_train)
        layout.addWidget(btn_test)

        self.setLayout(layout)

    # =========================
    # Actions
    # =========================

    def log(self, message):
        self.log_box.append(message)

    def run_collector(self):
        self.log("▶ Iniciando recolección de datos...")
        try:
            collect_data()
            self.log("✅ Recolección finalizada")
        except Exception as e:
            self.show_error(e)

    def run_training(self):
        self.log("▶ Entrenando modelo...")
        try:
            train_model()
            self.log("✅ Entrenamiento completado")
        except Exception as e:
            self.show_error(e)

    def run_realtime(self):
        self.log("▶ Iniciando testeo en tiempo real...")
        try:
            realtime_test()
            self.log("⏹ Testeo finalizado")
        except Exception as e:
            self.show_error(e)

    def show_error(self, error):
        QMessageBox.critical(self, "Error", str(error))
        self.log(f"❌ Error: {error}")


def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

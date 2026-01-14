# gui/app.py
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QMessageBox
)
from PyQt5.QtCore import Qt
from gui.test_window import TestModelWindow
from gui.collect_window import CollectDataWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lenguaje de Señas - Panel Principal")
        self.setFixedSize(400, 300)

        # ---------- Título ----------
        title = QLabel("Seleccione una acción")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        # ---------- Botones ----------
        btn_collect = QPushButton("📦 Recolectar datos")
        btn_train = QPushButton("🧠 Entrenar modelo")
        btn_test = QPushButton("🎥 Probar modelo")

        btn_collect.setFixedHeight(40)
        btn_train.setFixedHeight(40)
        btn_test.setFixedHeight(40)

        # ---------- Conexiones ----------
        btn_collect.clicked.connect(self.collect_clicked)
        btn_train.clicked.connect(self.train_clicked)
        btn_test.clicked.connect(self.test_clicked)

        # ---------- Layout ----------
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(title)
        layout.addWidget(btn_collect)
        layout.addWidget(btn_train)
        layout.addWidget(btn_test)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # ---------- Acciones (por ahora solo mensajes) ----------
    def collect_clicked(self):
        self.collect_window = CollectDataWindow()
        self.collect_window.show()

    def train_clicked(self):
        QMessageBox.information(self, "Entrenar", "Aquí irá el entrenamiento del modelo")

    def test_clicked(self):
        self.test_window = TestModelWindow()
        self.test_window.show()


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()


""" import sys
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
 """
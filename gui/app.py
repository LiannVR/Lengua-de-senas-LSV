# gui/app.py
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QInputDialog,
    QMessageBox,
    QLineEdit
)
from PyQt5.QtCore import Qt

from gui.test_window import TestModelWindow
from gui.advanced_window import AdvancedWindow
from config.settings import ADVANCED_PASSWORD


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lenguaje de Señas")
        self.setFixedSize(360, 220)

        title = QLabel("Reconocimiento de Lenguaje de Señas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        subtitle = QLabel("Seleccione una opción")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")

        btn_test = QPushButton("🎥 Probar modelo")
        btn_advanced = QPushButton("⚙️ Configuración avanzada")

        btn_test.setFixedHeight(45)
        btn_advanced.setFixedHeight(40)

        btn_test.clicked.connect(self.open_test)
        btn_advanced.clicked.connect(self.ask_password)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(btn_test)
        layout.addWidget(btn_advanced)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_test(self):
        self.test_window = TestModelWindow()
        self.test_window.show()

    # 🔐 Paso intermedio
    def ask_password(self):
        password, ok = QInputDialog.getText(
            self,
            "Acceso restringido",
            "Ingrese la contraseña:",
            QLineEdit.Password
        )

        if not ok:
            return

        if password == ADVANCED_PASSWORD:
            self.open_advanced()
        else:
            QMessageBox.critical(
                self,
                "Acceso denegado",
                "Contraseña incorrecta"
            )


    def open_advanced(self):
        self.advanced_window = AdvancedWindow()
        self.advanced_window.show()


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()


""" # gui/app.py
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel
)
from PyQt5.QtCore import Qt

from gui.test_window import TestModelWindow
from gui.advanced_window import AdvancedWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lenguaje de Señas")
        self.setFixedSize(360, 220)

        # ---------- Título ----------
        title = QLabel("Reconocimiento de Lenguaje de Señas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        subtitle = QLabel("Seleccione una opción")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")

        # ---------- Botones ----------
        btn_test = QPushButton("🎥 Probar modelo")
        btn_advanced = QPushButton("⚙️ Configuración avanzada")

        btn_test.setFixedHeight(45)
        btn_advanced.setFixedHeight(40)

        btn_test.clicked.connect(self.open_test)
        btn_advanced.clicked.connect(self.open_advanced)

        # ---------- Layout ----------
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(btn_test)
        layout.addWidget(btn_advanced)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_test(self):
        self.test_window = TestModelWindow()
        self.test_window.show()

    def open_advanced(self):
        self.advanced_window = AdvancedWindow()
        self.advanced_window.show()


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
 """
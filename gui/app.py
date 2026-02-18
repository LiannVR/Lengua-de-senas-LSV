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
    QLineEdit,
    QHBoxLayout,
    QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

from gui.test_window import TestModelWindow
from gui.advanced_window import AdvancedWindow
from config.settings import ADVANCED_PASSWORD


# 🔹 Ventana del Manual
class ManualDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Manual de Usuario")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        # 🔹 Imagen del manual (luego puedes cambiar la ruta)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap("gui/assets/manual.png")  # ← Aquí pondrás tu imagen después
        self.image_label.setPixmap(pixmap.scaled(
            800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

        layout.addWidget(self.image_label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lenguaje de Señas")
        self.showMaximized()

        # ---------- Botón Manual (arriba izquierda) ----------
        btn_manual = QPushButton()
        btn_manual.setIcon(QIcon.fromTheme("help-about"))
        btn_manual.setText("📖")
        btn_manual.setFixedSize(32, 32)
        btn_manual.clicked.connect(self.open_manual)

        # ---------- Título ----------
        title = QLabel("Reconocimiento de Lenguaje de Señas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
        """)

        subtitle = QLabel("Seleccione una opción")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 18px;
            color: gray;
        """)

        # ---------- Botones ----------
        btn_test = QPushButton("🎥 Probar modelo")
        btn_advanced = QPushButton("⚙️ Configuración avanzada")

        btn_test.setFixedHeight(50)
        btn_advanced.setFixedHeight(50)

        btn_test.clicked.connect(self.open_test)
        btn_advanced.clicked.connect(self.ask_password)

        # ---------- Layout principal ----------
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # 🔹 Barra superior con botón manual
        top_layout = QHBoxLayout()
        top_layout.addWidget(btn_manual)
        top_layout.addStretch()

        layout.addLayout(top_layout)

        # 🔹 Layout para centrar textos
        text_layout = QVBoxLayout()
        text_layout.addStretch()
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)
        text_layout.addStretch()

        layout.addLayout(text_layout)

        # 🔹 Botones abajo
        layout.addWidget(btn_test)
        layout.addWidget(btn_advanced)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # 📘 Abrir manual
    def open_manual(self):
        self.manual_dialog = ManualDialog()
        self.manual_dialog.exec_()

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
        self.showMaximized()

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
    run_app() """
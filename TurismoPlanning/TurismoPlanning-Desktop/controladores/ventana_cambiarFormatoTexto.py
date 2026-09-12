import sys, os
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QIcon
from vistas.cambiarFormatoTexto_ui import Ui_formato

class FormatoTexto(QWidget, Ui_formato):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Icono
        self.setWindowIcon(QIcon(os.getcwd() + "/recursos/iconos/formato-de-texto.png"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    formatoTxt = FormatoTexto()
    formatoTxt.show()
    sys.exit(app.exec())
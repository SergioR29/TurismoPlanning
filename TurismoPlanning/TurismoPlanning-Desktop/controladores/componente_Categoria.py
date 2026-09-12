import sys
from PySide6.QtWidgets import QWidget, QApplication
from vistas.componentes.componente_categoria_ui import Ui_componente_categoria

class Categoria(QWidget, Ui_componente_categoria):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    categoria = Categoria()
    categoria.show()
    sys.exit(app.exec())
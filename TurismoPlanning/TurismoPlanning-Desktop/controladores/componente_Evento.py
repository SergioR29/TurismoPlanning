import sys
from PySide6.QtWidgets import QWidget, QApplication
from vistas.componentes.componente_tarea_ui import Ui_componente_Tareas

class Evento(QWidget, Ui_componente_Tareas):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    evento = Evento()
    evento.show()
    sys.exit(app.exec())
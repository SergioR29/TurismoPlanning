import sys, os, shutil, sqlite3
from pathlib import Path
from PySide6.QtWidgets import QWidget, QApplication, QColorDialog, QMessageBox
from PySide6.QtGui import QIcon, QColor
from vistas.crearCategoria_ui import Ui_crearCategoria

class CrearCategoria(QWidget, Ui_crearCategoria):
    def __init__(self, editar=None, idC_E=None):
        super().__init__()
        self.setupUi(self)

        # Añadir los iconos
        self.setWindowIcon(QIcon(os.getcwd() + "/recursos/iconos/categorias.png"))
        self.color.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_selectorColor.png"))

        self.cerrar.setIcon(QIcon(os.getcwd() + "/recursos/iconos/cerrar.png"))
        self.guardarCategoria.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_guardar.png"))

        # Copiar la BD a la carpeta del usuario (para que no sea de sólo lectura)
        rutaBD = os.getcwd() + "/modelos/datos.db"
        userDir = Path.home()

        new_dirBD = os.path.join(userDir, "AdminTurismo")
        new_rutaBD = os.path.join(new_dirBD, "datos.db")
        os.makedirs(new_dirBD, exist_ok=True)

        if not os.path.exists(new_rutaBD):
            shutil.copy(rutaBD, new_rutaBD)

        # Conexión a la BD
        self.conexion = False
        try:
            self.conexion = sqlite3.connect(new_rutaBD)
        except sqlite3.Error as e:
            print(e.sqlite_errorcode)
            print(e.sqlite_errorname)


        # Variables auxiliares
        self.colorSeleccionado = None
        self.editarC = editar
        self.idC_E = int(idC_E) if idC_E != None else None
        
        # Acciones
        self.color.clicked.connect(self.seleccionarColor)
        self.guardarCategoria.clicked.connect(self.guardar)
    
    def guardar(self):
        # Función que permite añadir una categoría nueva al usuario
        if self.conexion:
            if len(self.nombreLineEdit.text()) > 0 and self.prioridadSpinBox.value() > 0:
                try:
                    if not self.editarC:
                        id = self.conexion.execute("SELECT MAX(ID) FROM Categorias").fetchone()
                        idC = 0
                        if id[0] != None:
                            idC = id[0] + 1
                        else:
                            idC = 1

                        self.conexion.execute("INSERT INTO Categorias VALUES (?, ?, ?, ?)", (idC, self.nombreLineEdit.text(), self.prioridadSpinBox.value(), self.colorSeleccionado,))
                        self.conexion.commit()
                        QMessageBox.information(self, "Resultado", "Categoría añadida correctamente")

                    elif self.idC_E > 0:
                        if self.colorSeleccionado != None:
                            self.conexion.execute("UPDATE Categorias SET Nombre = ?, Prioridad = ?, Color = ? WHERE ID = ?", (self.nombreLineEdit.text(), self.prioridadSpinBox.value(), self.colorSeleccionado, self.idC_E,))
                        else:
                            self.conexion.execute("UPDATE Categorias SET Nombre = ?, Prioridad = ? WHERE ID = ?", (self.nombreLineEdit.text(), self.prioridadSpinBox.value(), self.idC_E,))

                        self.conexion.commit()
                        QMessageBox.information(self, "Resultado", "Categoría editada correctamente")
                    else:
                        QMessageBox.critical(self, "Error", "No se pudo modificar la categoría, no existe")

                except sqlite3.Error as e:
                    print(e)
                    self.conexion.rollback()
                    QMessageBox.warning(self, "Aviso", "La categoría ya existe")
            else:
                QMessageBox.warning(self, "Aviso", "Faltan valores por rellenar")
        else:
            QMessageBox.critical(self, "Error", "Error al guardar la categoría")

    def seleccionarColor(self):
        # Función que permite al usuario seleccionar un color
        color = QColorDialog.getColor(QColor(255, 255, 255), self, "Seleccionar un color")
        if color.isValid():
            self.color.setStyleSheet("background-color: " + color.name() + ";color:" + color.name())
            self.color.setIcon(QIcon())
            self.colorSeleccionado = color.name()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    crear = CrearCategoria()
    crear.show()
    sys.exit(app.exec())
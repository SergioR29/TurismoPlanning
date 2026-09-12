import sys, os, shutil, sqlite3, io, base64
from pathlib import Path
from xhtml2pdf import pisa
from PySide6.QtWidgets import QWidget, QApplication, QMessageBox, QTreeWidgetItem, QComboBox, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, QBuffer, QIODevice
from controladores.ventana_crearCategoria import CrearCategoria
from vistas.gestionarCategorias_ui import Ui_categorias
from controladores.componente_Categoria import Categoria

class Categorias(QWidget, Ui_categorias):
    closing = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Añadir iconos
        self.setWindowIcon(QIcon(os.getcwd() + "/recursos/iconos/categorias.png"))

        self.editarCategoria.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_editar.png"))
        self.eliminarCategoria.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_eliminar.png"))

        self.ayuda.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ayuda.png"))

        # Variables auxiliares
        self.ventana = 0
        self.categoriaID = QComboBox()

        self.plantillaHTML = "<!DOCTYPE html><html><head><style>#contenedor{display: flex;align-items: center;}div{margin-bottom: 20px;}#color{width: 40px;height: 40px;border:5px solid black;margin-right: 10px;min-width: 40px;}#prioridad{font-family: 'Segoe UI';font-size: 27px;font-style: normal;position:relative;top: -10px;margin-right: 10px;}#nombre{font-family: 'Segoe UI';font-size: 22px;font-style: normal;vertical-align: center;position: relative;top: -10px;flex-grow: 1}</style></head><body>"
        self.plantillaPDF = """<!DOCTYPE html><html><head><style>table{margin-bottom: 20px;width:auto;height:auto;}#color{width: 40px;height:40px;border:5px solid black;min-width: 40px;}#prioridad{padding-top:10px;font-family: 'Segoe UI';font-size: 27px;width:auto;height:auto;border-bottom:1px solid black;}#nombre{padding-top:5px;width:auto;height:auto;font-family: 'Segoe UI';font-size: 20px;}</style></head><body>"""

        self.infoHTML = ""
        self.infoPDF = ""
        self.finalHTML = "</body></html>"

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

        # Configuraciones iniciales
        self.cargarCategorias()

        __qtreewidgetitem1 = QTreeWidgetItem(self.exportar)
        __qtreewidgetitem1.setIcon(0, QIcon(os.getcwd() + "/recursos/iconos/html.png"))
        __qtreewidgetitem1.setText(0, "HTML")

        __qtreewidgetitem2 = QTreeWidgetItem(self.exportar)
        __qtreewidgetitem2.setIcon(0, QIcon(os.getcwd() + "/recursos/iconos/pdf.png"))
        __qtreewidgetitem2.setText(0, "PDF")

        # Acciones
        self.editarCategoria.clicked.connect(self.editar)
        self.eliminarCategoria.clicked.connect(self.eliminar)

        self.exportar.itemClicked.connect(self.exportarListado)
        self.ayuda.clicked.connect(self.mostrarAyuda)

    def exportarListado(self, item, columna):
        # Función que exporta el listado de categorías ordenadas por prioridad en HTML o PDF
        ruta_fichero = QFileDialog.getExistingDirectory(self, "Seleccionar destino", str(Path.home()), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        formato = item.text(columna)

        if ruta_fichero:
            if len(self.infoHTML) > 0:
                if formato == "HTML":
                    plantilla = self.plantillaHTML + self.infoHTML + self.finalHTML

                    directorio_path = Path(ruta_fichero)
                    nombreHTML = "ListadoCategorias.html"
                    destinoHTML = directorio_path / nombreHTML

                    with open(destinoHTML, "w", encoding="utf-8") as exportar:
                        try:
                            exportar.write(plantilla)

                            msg_box = QMessageBox(self)
                            msg_box.setIcon(QMessageBox.Information)
                            msg_box.setWindowTitle("Resultado")
                            msg_box.setInformativeText(f"HTML exportado correctamente a:\n{destinoHTML}")
                            msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                            msg_box.exec()

                            self.infoHTML = ""
                            self.infoPDF = ""
                            self.cargarCategorias()

                        except Exception as e:
                            print(e)
                            QMessageBox.critical(self, "Error de Exportación", f"No se pudo guardar el archivo HTML.\nDetalle: {e}")
                
                elif formato == "PDF":
                    plantilla = self.plantillaPDF + self.infoPDF + self.finalHTML
                    try:
                        directorio_path = Path(ruta_fichero)
                        nombrePDF = "ListadoCategorias.pdf"
                        destinoPDF = directorio_path / nombrePDF

                        html = io.BytesIO(plantilla.encode("utf-8"))
                        output_file = open(str(destinoPDF), "wb")
                        pisa_status = pisa.CreatePDF(html, dest=output_file, encoding="utf-8")
                        output_file.close()

                        if not pisa_status.err:
                            msg_box = QMessageBox(self)
                            msg_box.setIcon(QMessageBox.Information)
                            msg_box.setWindowTitle("Resultado")
                            msg_box.setInformativeText(f"PDF exportado correctamente a:\n{destinoPDF}")
                            msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                            msg_box.exec()

                            self.infoHTML = ""
                            self.infoPDF = ""
                            self.cargarCategorias()
                        else:
                            QMessageBox.critical(self, "Error", "Error al exportar el fichero a PDF")

                    except Exception as e:
                        print(e)
                        QMessageBox.critical(self, "Error", "Error al exportar el fichero a PDF")
            else:
                QMessageBox.critical(self, "Error de Exportación", f"No se pudo exportar el archivo, no tiene contenido")

    def editar(self):
        # Función que permite el usuario editar los datos de una categoría seleccionada
        idC = self.categoriaID.itemText(self.categoriaComboBox.currentIndex())
        try:
            filas = self.conexion.execute("SELECT c.Prioridad, c.Color FROM Categorias c WHERE c.ID = ?", (idC,)).fetchall()
            prioridad = 0
            color = ""
            for f in filas:
                prioridad = int(f[0])
                color = str(f[1])

            if self.categoriaComboBox.currentIndex() != -1:
                self.ventana = CrearCategoria(True, idC)
                self.ventana.guardarCategoria.clicked.connect(self.cargarCategorias)

                self.ventana.nombreLineEdit.setText(self.categoriaComboBox.currentText())
                self.ventana.prioridadSpinBox.setValue(prioridad)

                self.ventana.color.setStyleSheet("background-color:" + color + ";color:" + color + ";")
                self.ventana.color.setIcon(QIcon())
                
                self.ventana.show()
            else:
                QMessageBox.warning(self, "Aviso", "No se ha seleccionado ninguna categoría")

        except sqlite3.Error as e:
            print(e)

    def eliminar(self):
        # Función que permite al usuario eliminar una categoría seleccionada por el mismo
        idC = self.categoriaID.itemText(self.categoriaComboBox.currentIndex())
        if self.categoriaComboBox.currentIndex() != -1:
            try:
                self.conexion.execute("DELETE FROM Categorias WHERE ID = ?", (idC,))
                self.conexion.execute("DELETE FROM Tareas WHERE Categoria = ?", (idC,))
                self.conexion.commit()

                QMessageBox.information(self, "Resultado", "Categoría " + self.categoriaComboBox.currentText() + " eliminada correctamente")
                self.cargarCategorias()

            except sqlite3.Error as e:
                print(e)
                QMessageBox.critical(self, "Error", "Error al borrar la categoría")
        else:
            QMessageBox.warning(self, "Aviso", "No se ha seleccionado ninguna categoría")

    def mostrarAyuda(self):
        # Función que ayuda al usuario
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Ayuda")
        msg_box.setInformativeText("Seleccione una categoría para editar sus datos o directamente eliminarla. Al editar o eliminar una categoría se volverán a cargar los datos automáticamente")
        msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
        msg_box.exec()

    def limpiar_layout(self, layout):
        """Elimina todos los widgets y otros ítems de un layout y los borra."""
        if layout is not None:
            """Iteramos sobre los ítems del layout.
               # Usamos takeAt(0) repetidamente hasta que el layout esté vacío.
               # takeAt(0) remueve y devuelve el primer ítem (índice 0).
            """
            while layout.count():
                item = layout.takeAt(0) # Toma el primer ítem del layout

                # Si el ítem es un widget, lo borramos.
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater() # Borra el widget de forma segura cuando el control regresa al bucle de eventos

                # Si el ítem es un layout (un layout anidado dentro de este), lo limpiamos recursivamente.
                else:
                    if item.layout() is not None:
                        self.limpiar_layout(item.layout()) # Limpia el layout anidado
                    # Si el ítem es un QSpacerItem, lo removemos (no necesita borrarse con deleteLater).
                    elif item.spacerItem() is not None:
                        layout.removeItem(item.spacerItem())

    def cargarCategorias(self):
        # Función que carga el listado de categorías creadas que puede seleccionar el usuario
        self.infoHTML = ""
        self.infoPDF = ""

        if self.conexion:
            self.categoriaComboBox.clear()
            self.categoriaID.clear()
            self.limpiar_layout(self.verticalLayout)

            filas = self.conexion.execute("SELECT c.Nombre, c.Prioridad, c.Color, C.ID FROM Categorias c ORDER BY c.Prioridad, c.Nombre").fetchall()
            for f in filas:
                self.categoriaComboBox.addItem(f[0])
                self.categoriaComboBox.setCurrentIndex(-1)

                categoria = Categoria()
                categoria.color.setStyleSheet(f"background-color:{f[2]};color:{f[2]}")
                categoria.prioridad.setText(str(f[1]) + "º)")
                categoria.nombre.setText(f[0])
            
                self.verticalLayout.addWidget(categoria)
                self.categoriaID.addItem(str(f[3]))

                # Plantilla HTML
                self.infoHTML += f"<div id=\"contenedor\"><div id=\"color\" style=\"{"background-color:" + str(f[2])}\"></div><label id=\"prioridad\"><strong>{str(f[1])}&deg)&nbsp;&nbsp;&nbsp;</strong></label><label id=\"nombre\">{str(f[0])}</label></div>"
                self.infoPDF += f"<table id=\"contenedor\"><tr><td id=\"color\" style=\"{"background-color:" + str(f[2])}\"></td></tr><tr><td id=\"prioridad\"><strong>{str(f[1])}&deg)&nbsp;&nbsp;&nbsp;</strong></td></tr><tr><td id=\"nombre\">{str(f[0])}</td></tr></table>"
        else:
            QMessageBox.critical(self, "Error", "Error de conexión a la BD")

    def closeEvent(self, event):
        # Función que el usuario al cerrar la ventana se le vuelve a la ventana de inicio
        self.closing.emit()
        super().closeEvent(event)

    def cerrarVentana(self):
        self.ventana.close()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    categorias = Categorias()
    categorias.show()
    sys.exit(app.exec())
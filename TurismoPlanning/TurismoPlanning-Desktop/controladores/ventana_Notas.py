import sys, os, io
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PySide6.QtGui import QIcon, QCloseEvent
from PySide6.QtCore import Signal
from vistas.notas_ui import Ui_notas
from controladores.ventana_cambiarFormatoTexto import FormatoTexto
from xhtml2pdf import pisa

class Notas(QMainWindow, Ui_notas):
    closing = Signal()

    def __init__(self, rutafichero=None):
        super().__init__()
        self.setupUi(self)

        # Añadir iconos
        self.actionAbrir.setIcon(QIcon(os.getcwd() + "/recursos/iconos/abrir-documento.png"))
        self.actionGuardar.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_guardar.png"))
        self.actionGuardar_como.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_guardar.png"))

        self.menuExportar.setIcon(QIcon(os.getcwd() + "/recursos/iconos/flecha_arriba.png"))
        self.actionHTML.setIcon(QIcon(os.getcwd() + "/recursos/iconos/html.png"))
        self.actionPDF.setIcon(QIcon(os.getcwd() + "/recursos/iconos/pdf.png"))

        self.actionFormato_de_texto.setIcon(QIcon(os.getcwd() + "/recursos/iconos/formato_texto.png"))
        self.actionAyuda.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ayuda.png"))
        self.setWindowIcon(QIcon(os.getcwd() + "/recursos/iconos/notas.png"))

        # Variables importantes
        self.rutafichero = rutafichero
        self.formato = None

        # Acciones
        self.texto.textChanged.connect(self.actualizarEstado)

        self.actionAbrir.triggered.connect(self.abrirNota)
        self.actionGuardar.triggered.connect(self.guardar)
        self.actionGuardar_como.triggered.connect(self.guardarComo)

        self.actionHTML.triggered.connect(self.exportarHTML)
        self.actionPDF.triggered.connect(self.exportarPDF)

        self.actionFormato_de_texto.triggered.connect(self.cambiarFormatoTXT)
        self.actionAyuda.triggered.connect(self.mostrarAyuda)
    
    def actualizarEstado(self):
        # Función que va indicando al usuario cuando el estado del fichero (cuando hay que guardar los cambios)
        self.setWindowTitle("")
        self.setWindowTitle(("Notas - " + self.rutafichero  + " *") if self.rutafichero != None else ("Notas - " + "Nuevo" + " *"))
        
    def exportarPDF(self):
        # Función que permite al usuario exportar a un fichero PDF su contenido textual
        rutafichero, _ = QFileDialog.getSaveFileName(None, "Seleccionar destino de exportación", "", "PDF (*.pdf)")
        info = f"<html><head><title>{rutafichero.split("/")[-1]}</title><style>p{{font-size:14px;font-family:{self.formato if self.formato != None else ""};}}</style></head><body><p>{self.texto.toPlainText()}</p></body></html>"
        
        if rutafichero:
            try:
                html = io.BytesIO(info.encode("utf-8"))
                output_file = open(str(rutafichero), "wb")
                pisa_status = pisa.CreatePDF(html, dest=output_file, encoding="utf-8")
                output_file.close()

                if not pisa_status.err:
                        msg_box = QMessageBox(self)
                        msg_box.setIcon(QMessageBox.Information)
                        msg_box.setWindowTitle("Resultado")
                        msg_box.setInformativeText(f"PDF exportado correctamente a:\n{rutafichero}")
                        msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                        msg_box.exec()
                else:
                    QMessageBox.critical(self, "Error", "Error al exportar el fichero a PDF")

            except Exception as e:
                print(e)
                QMessageBox.critical(self, "Error", "Error al exportar el fichero a PDF")

    def exportarHTML(self):
        # Función que permite al usuario exportar a un fichero HTML su contenido textual
        rutafichero, _ = QFileDialog.getSaveFileName(None, "Seleccionar destino de exportación", "", "HyperText Markup Language file (*.html)")
        info = f"<html><head><title>{rutafichero.split("/")[-1]}</title><style>p{{font-size:14px;font-family:{self.formato if self.formato != None else ""};}}</style></head><body><p>{self.texto.toPlainText()}</p></body></html>"
        if rutafichero:
            with open(rutafichero, "w", encoding="utf-8") as exportar:
                try:
                    exportar.write(info)

                    msg_box = QMessageBox(self)
                    msg_box.setIcon(QMessageBox.Information)
                    msg_box.setWindowTitle("Resultado")
                    msg_box.setInformativeText(f"HTML exportado correctamente a:\n{rutafichero}")
                    msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                    msg_box.exec()
                
                except Exception as e:
                    print(e)
                    QMessageBox.critical(self, "Error de Exportación", f"No se pudo guardar el archivo HTML.\nDetalle: {e}")
        
    def guardarComo(self):
        # Función que directamente permitiría seleccionar un destino de guardado del fichero
        rutafichero, _ = QFileDialog.getSaveFileName(None, "Seleccionar destino de guardado", "", "Archivos de Texto (*.txt)")
        if rutafichero:
            with open(rutafichero, "w", encoding="utf-8") as guardar:
                try:
                    guardar.write(self.texto.toPlainText())

                    self.rutafichero = rutafichero
                    self.setWindowTitle("Notas - " + self.rutafichero)

                    return True
                except Exception as e:
                    print(e)
                    msg_box = QMessageBox(self)
                    msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                    msg_box.setIcon(QMessageBox.Critical)
                    msg_box.setWindowTitle("Error")
                    msg_box.setInformativeText("Error al guardar el fichero de texto.")
                    msg_box.exec()

                    return False
        else:
            return False

    def guardar(self):
        # Función que permite al usuario guardar su contenido textual
        if self.rutafichero != None:
            with open(self.rutafichero, "w", encoding="utf-8") as guardar:
                try:
                    guardar.write(self.texto.toPlainText())
                    self.setWindowTitle("Notas - " + self.rutafichero)

                    return True
                except Exception as e:
                    print(e)
                    msg_box = QMessageBox(self)
                    msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                    msg_box.setIcon(QMessageBox.Critical)
                    msg_box.setWindowTitle("Error")
                    msg_box.setInformativeText("Error al guardar los cambios en el fichero.")
                    msg_box.exec()

                    return False
        else:
            rutafichero, _ = QFileDialog.getSaveFileName(None, "Seleccionar destino de guardado", "", "Archivos de Texto (*.txt)")
            if rutafichero:
                with open(rutafichero, "w", encoding="utf-8") as guardar:
                    try:
                        guardar.write(self.texto.toPlainText())

                        self.rutafichero = rutafichero
                        self.setWindowTitle("Notas - " + self.rutafichero)

                        return True
                    except Exception as e:
                        print(e)
                        msg_box = QMessageBox(self)
                        msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                        msg_box.setIcon(QMessageBox.Critical)
                        msg_box.setWindowTitle("Error")
                        msg_box.setInformativeText("Error al guardar el fichero de texto.")
                        msg_box.exec()

                        return False
            else:
                return False

    def abrirNota(self):
        # Función que permite al usuario editar una nota de texto
        rutafichero, _ = QFileDialog.getOpenFileName(None, "Seleccionar fichero de texto", "", "Archivos de Texto (*.txt)")
        if rutafichero:
            with open(rutafichero, "r", encoding="utf-8") as fichero:
                try:
                    contenido = fichero.read()

                    self.rutafichero = rutafichero
                    self.setWindowTitle("Notas - " + rutafichero)

                    self.texto.setText(contenido)
                except Exception as e:
                    print(e)
                    msg_box = QMessageBox(self)
                    msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                    msg_box.setIcon(QMessageBox.Critical)
                    msg_box.setWindowTitle("Error")
                    msg_box.setInformativeText("Fichero de texto no válido")
                    msg_box.exec()
        else:
            msg_box = QMessageBox(self)
            msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Aviso")
            msg_box.setInformativeText("No se ha seleccionado ningún fichero de texto.")
            msg_box.exec()

    def cambiarFormatoTXT(self):
        # Función que permite al usuario visualizar de forma diferente su texto
        self.ventana = FormatoTexto()
        self.ventana.show()
        self.ventana.ok.clicked.connect(self.nuevoFormatoTXT)
    
    def nuevoFormatoTXT(self):
        # Función que devuelve el nuevo formato de texto que el usuario haya seleccionado
        self.texto.setFont(self.ventana.formatoComboBox.currentFont())
        self.formato = self.ventana.formatoComboBox.currentFont().toString().split(",")[0]

    def mostrarAyuda(self):
        # Función que muestra una ayuda práctica al usuario
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Ayuda")
        msg_box.setInformativeText("Esta ventana es un bloc de notas con el que puede tomar apuntes y exportarlo a donde sea (txt, html, pdf).")
        msg_box.exec()

    def closeEvent(self, event : QCloseEvent):
        if self.windowTitle().find("*") == -1:
            self.closing.emit()
            super().closeEvent(event)

            event.accept()
        else:
            msg_box = QMessageBox(self)
            msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30);")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Aviso")
            msg_box.setInformativeText("El documento tiene cambios sin guardar.\n¿Desea guardar los cambios?")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            respuesta = msg_box.exec()

            if respuesta == QMessageBox.StandardButton.Yes:
                if self.guardar():
                    event.accept()
                else:
                    event.ignore()

            elif respuesta == QMessageBox.StandardButton.No:
                event.accept()
            else:
                event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    notas = Notas()
    notas.show()
    sys.exit(app.exec())
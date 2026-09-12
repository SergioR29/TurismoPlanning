import sys, os, shutil, sqlite3, io, base64
from pathlib import Path
from xhtml2pdf import pisa
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QFileDialog
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Signal, QBuffer, QIODevice, Qt, QObject, QSize
from vistas.eventosPlanificados_ui import Ui_eventos
from controladores.componente_Evento import Evento
from controladores.ventana_planificarTareas import PlanificarTareas

class EventosPlanificados(QMainWindow, Ui_eventos):
    closing = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Variables auxiliares
        self.ventana = 0
        self.titulo = ""

        # Variables HTML
        self.cabeceraHTML = "<!DOCTYPE html><html><head><style>#ic_Tarea{width:52px; height:52px;margin-right:10px;text-align:left;padding-left:5px;border:none;}#titulo{padding-top:5px;font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 20px; margin-right: 10px}#desc{font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 15px;}table{border:none;margin-bottom:20px;}td{margin-right:10px;}</style></head>"
        self.cabeceraPDF = "<!DOCTYPE html><html><head><style>#ic_Tarea{width:52px; height:52px;margin-right:10px;text-align:left;padding-left:5px;border:none;}#titulo{padding-top:5px;font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 20px; margin-right: 10px}#desc{font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 15px;border-bottom:1px solid black;}table{border:none;margin-bottom:20px;}td{margin-right:10px;}</style></head>"
        self.cuerpoHTML = ""
        self.pieHTML = "</body></html>"
        
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
        self.editarEvento.hide()
        self.eliminarEvento.hide()

        self.setWindowIcon(QIcon(os.getcwd() + "/recursos/iconos/eventos.png"))
        self.editarEvento.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_editar.png"))
        self.eliminarEvento.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_eliminar.png"))
        
        self.ayuda.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ayuda.png"))
        self.actionAyuda.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ayuda.png"))

        self.actionHTML.setIcon(QIcon(os.getcwd() + "/recursos/iconos/html.png"))
        self.actionPDF.setIcon(QIcon(os.getcwd() + "/recursos/iconos/pdf.png"))

        # Acciones
        self.categoriaComboBox.currentTextChanged.connect(self.cargarEventosCategoria)
        self.editarEvento.clicked.connect(self.editar)
        self.eliminarEvento.clicked.connect(self.eliminar)

        self.actionAyuda.triggered.connect(self.mostrarAyuda)
        self.ayuda.clicked.connect(self.mostrarAyuda)

        self.actionHTML.triggered.connect(self.exportarHTML)
        self.actionPDF.triggered.connect(self.exportarPDF)

    def exportarHTML(self):
        # Función que exporta los eventos y las tareas del usuario a formato HTML
        if self.categoriaComboBox.currentIndex() != -1:
            ruta_HTML = QFileDialog.getExistingDirectory(self, "Seleccionar destino de exportación a HTML", str(Path.home()), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

            if ruta_HTML:
                directorio_path = Path(ruta_HTML)
                nombreHTML = "Eventos - " + self.categoriaComboBox.currentText() + ".html"
                destinoHTML = directorio_path / nombreHTML

                try:
                    html = self.cabeceraHTML + self.cuerpoHTML + self.pieHTML
                    with open(destinoHTML, "w", encoding="utf-8") as f:
                        f.write(html)

                        msg_box = QMessageBox(self)
                        msg_box.setIcon(QMessageBox.Information)
                        msg_box.setWindowTitle("Resultado")
                        msg_box.setInformativeText(f"HTML exportado correctamente a:\n{destinoHTML}")
                        msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                        msg_box.exec()

                        self.cuerpoHTML = ""
                        self.cargarEventosCategoria()

                except Exception as e:
                    QMessageBox.critical(self, "Error de Exportación", f"No se pudo guardar el archivo HTML.\nDetalle: {e}")
        else:
            QMessageBox.warning(self, "Aviso", "No se ha seleccionado una categoría")

    def exportarPDF(self):
        # Función que exporta los eventos y las tareas del usuario a formato PDF
        if self.categoriaComboBox.currentIndex() != -1:
            ruta_PDF = QFileDialog.getExistingDirectory(self, "Seleccionar destino de exportación a PDF", str(Path.home()), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
            
            if ruta_PDF:
                plantilla = self.cabeceraPDF + self.cuerpoHTML + self.pieHTML
                try:
                    directorio_path = Path(ruta_PDF)
                    nombrePDF = "Eventos - " + self.categoriaComboBox.currentText() + ".pdf"
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

                        self.cuerpoHTML = ""
                        self.cargarEventosCategoria()

                except Exception as e:
                    print(e)
                    QMessageBox.critical(self, "Error", "Error al exportar el fichero a PDF")
        else:
            QMessageBox.warning(self, "Aviso", "No se ha seleccionado una categoría")

    def eliminar(self):
        # Función que elimina un evento seleccionado de uan categoría seleccionada por el usuario
        try:
            idT = self.conexion.execute("SELECT t.ID FROM Tareas t WHERE t.Titulo = ?", (self.titulo,)).fetchone()
            if idT[0] != None:
                self.conexion.execute("DELETE FROM Tareas WHERE ID = ?", (idT[0],))
                self.conexion.commit()

                QMessageBox.information(self, "Resultado", "Evento " + self.titulo + " borrado corrrectamente")
                self.cargarEventosCategoria()
            else:
                QMessageBox.critical(self, "Error", "Error al eliminar el evento " + self.titulo + ", no existe")

        except sqlite3.Error as e:
            print(e)
            print(e.sqlite_errorcode)
            print(e.sqlite_errorname)

            self.conexion.rollback()
            QMessageBox.critical(self, "Error", "Error al eliminar el evento " + self.titulo)

    def editar(self):
        # Función que edita un evento seleccionado de una categoría seleccionada por el usuario, si lo permite
        if self.titulo:
            self.ventana = PlanificarTareas(None, True, self.titulo)
            self.ventana.guardarTarea.clicked.connect(self.cargarEventosCategoria)
            self.ventana.show()
        else:
            QMessageBox.warning(self, "Aviso", "No se ha seleccionado ningún evento")

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

    def cargarEventosCategoria(self):
        # Función que carga todos los eventos asociados a una categoría correspondiente que haya seleccionado el usuario
        if self.conexion:
            self.limpiar_layout(self.verticalLayout)
            try:
                idC = self.conexion.execute("SELECT c.ID FROM Categorias c WHERE c.Nombre = ?", (self.categoriaComboBox.currentText(),)).fetchone()
                if idC[0] != None:
                    colorC = self.conexion.execute("SELECT c.Color FROM Categorias c WHERE c.ID = ?", (idC[0],)).fetchone()
                    if colorC[0] != None:
                        self.menubar.setStyleSheet(f"color: rgb(255, 255, 255);\nbackground-color: rgb(44, 44, 44);border-bottom:1px solid {colorC[0]}")
                        #self.categoriaComboBox.setStyleSheet(f"color:white; border-top: none;\n    border-left: none;\n    border-right: none;\n    border-bottom: 2px solid {colorC[0]};\nbackground-color: rgb(40, 40, 40);\npadding-left:5px;")
                    else:
                        self.menubar.setStyleSheet(f"color: rgb(255, 255, 255);\nbackground-color: rgb(44, 44, 44);")

                    eventosC = self.conexion.execute("SELECT t.Icono, t.Titulo, t.Fecha_Inicio, t.Plazo_Fecha FROM Tareas t WHERE t.Categoria = ? ORDER BY t.Plazo_Fecha, t.Prioridad", (idC[0],)).fetchall()
                    if len(eventosC) > 0:
                        for eventoC in eventosC:
                            evento = Evento()
                            self.editarEvento.hide()
                            self.eliminarEvento.hide()

                            evento.titulo.setText(eventoC[1])
                            if colorC[0] != None:
                                evento.setStyleSheet(f"border:none;")
                                evento.evento_tarea.setStyleSheet(f"QPushButton{{color:white;text-align:left;border-radius:5px;padding-left:5px;border:none;}} QPushButton:hover {{background-color: darkgray;}}QPushButton:pressed {{background-color: gray;}}")
                                evento.titulo.setStyleSheet(f"color:white;")
                                evento.plazo.setStyleSheet(f"color:white;")
                            else:
                                evento.setStyleSheet(f"border:none;")
                                evento.evento_tarea.setStyleSheet("QPushButton {color:white;text-align:left;border-radius:5px;padding-left:5px;border:none;} QPushButton:hover {background-color: darkgray;} QPushButton:pressed {background-color: gray;}")
                                evento.titulo.setStyleSheet(f"color:white;")
                                evento.plazo.setStyleSheet(f"color:white;")
                            
                            icono = eventoC[0]
                            if icono != None:
                                pixmap = QPixmap()
                                pixmap.loadFromData(icono, "PNG")

                                if not pixmap.isNull():
                                    evento.evento_tarea.setIcon(pixmap)
                                    evento.evento_tarea.setIconSize(QSize(45, 42))
                            else:
                                evento.evento_tarea.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_icono.png"))
                                evento.evento_tarea.setIconSize(QSize(45, 42))

                            fechaInicio = eventoC[2]
                            FI = ""
                            if fechaInicio != None:
                                FI = fechaInicio + " hasta el "

                            plazoFecha = eventoC[3]
                            evento.plazo.setText(FI + plazoFecha)

                            # Evento listo para visualizar
                            self.verticalLayout.addWidget(evento)
                            evento.evento_tarea.clicked.connect(self.editarEvento.show)
                            evento.evento_tarea.clicked.connect(self.eliminarEvento.show)
                            evento.evento_tarea.clicked.connect(self.al_clicar_evento_tarea)

                            # Información para el HTML
                            icTarea_URL = ""
                            if icono != None:
                                binary_data1 = bytes(icono)

                                base64_encoded_data1 = base64.b64encode(binary_data1)
                                base64_string1 = base64_encoded_data1.decode('ascii')

                                mime_type = "image/png"
                                icTarea_URL = f"data:{mime_type};base64,{base64_string1}"

                            descF = FI + plazoFecha
                            self.cuerpoHTML += f"<table id=\"contenedor\"><tr><td><img id=\"ic_Tarea\" src=\"{icTarea_URL}\"/></td></tr><tr><td id=\"titulo\"><strong>{eventoC[1]}</strong></td></tr><tr><td id=\"desc\">{descF}</td></tr></table>"
                    else:
                        QMessageBox.warning(self, "Aviso", "La categoría " + self.categoriaComboBox.currentText() + " no tiene eventos asociados")
                else:
                    QMessageBox.critical(self, "Error", "Categoría no encontrada")

            except Exception as e:
                print(e)
                QMessageBox.critical(self, "Error", "Error al cargar los eventos de la categoría " + self.categoriaComboBox.currentText())
        else:
            QMessageBox.critical(self, "Error", "Error de conexión a la BD")

    def cargarCategorias(self):
        # Función que carga el desplegable de todas las categorías de la cuáles el usuario puede seleccionar una para ver sus tareas programadas
        if self.conexion:
            self.categoriaComboBox.clear()
            self.editarEvento.hide()
            self.eliminarEvento.hide()
            try:
                filas = self.conexion.execute("SELECT c.Nombre FROM Categorias c").fetchall()
                for f in filas:
                    self.categoriaComboBox.addItem(f[0])
                    self.categoriaComboBox.setCurrentIndex(-1)

            except Exception as e:
                print(e)
        else:
            QMessageBox.critical(self, "Error", "Error de conexión a la BD")

    def mostrarAyuda(self):
        # Función que muestra una ayuda práctica al usuario
        QMessageBox.information(self, "Ayuda", "Al pulsar hacia el icono de un evento aparecerán al lado del desplegable de categorías 2 botones (Editar y Eliminar). Primero hay que seleccionar una categoría de eventos.")

    def al_clicar_evento_tarea(self):
        # Función que devuelve el título del evento seleccionado. self.sender() devuelve el objeto que emitió la señal, que es el QPushButton evento_tarea
        boton_pulsado = self.sender()
        if boton_pulsado and isinstance(boton_pulsado, QPushButton):
            evento_widget_pulsado = boton_pulsado.parent()
            titulo = evento_widget_pulsado.titulo.text()
            self.titulo = titulo

    def closeEvent(self, event):
    # Función que el usuario al cerrar la ventana se le vuelve a la ventana de inicio
        self.closing.emit()
        super().closeEvent(event)

    def cerrarVentana(self):
        self.ventana.close()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    eventos = EventosPlanificados()
    eventos.show()
    sys.exit(app.exec())
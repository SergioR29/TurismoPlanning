import sys, os, sqlite3, shutil, base64, io
from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Signal, QBuffer, QIODevice
from xhtml2pdf import pisa
from modelos.InitialisationError import InitialisationError
from vistas.verSitios_ui import Ui_manejarSitios
from controladores.ventana_Actualidad import Actualidad
from controladores.ventana_planificarTareas import PlanificarTareas

class VerSitios(QMainWindow, Ui_manejarSitios):
    closing = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Variables auxiliares
        self.ventana = 0
        self.desc_C = ""
        self.desc_S = ""

        # Configuraciones menores
        self.aviso_ciudadNoSeleccionada.hide()
        self.planificar_visita.hide()
        self.ubiClima_sitio.hide()
        self.frame_sitios.hide()
        self.aviso_sitio.hide()

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

        # Configurar iconos
        self.setWindowIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_SitiosVentana.png"))
        self.planificar_visita.setIcon(QIcon(os.getcwd() + "/recursos/iconos/visita_turismo.png"))
        self.ubiClima_sitio.setIcon(QIcon(os.getcwd() + "/recursos/iconos/UbiClima.png"))
        self.actionHTML.setIcon(QIcon(os.getcwd() + "/recursos/iconos/html.png"))
        self.actionPDF.setIcon(QIcon(os.getcwd() + "/recursos/iconos/pdf.png"))

        # Configuraciones importantes
        self.ciudades = self.cargarCiudades()

        # Acciones
        self.ciudadComboBox.currentTextChanged.connect(self.cargarSitiosCiudad)
        self.sitioComboBox.currentTextChanged.connect(self.cargarSitio)
        self.actionHTML.triggered.connect(self.exportarHTML)
        self.actionPDF.triggered.connect(self.exportarPDF)
        self.planificar_visita.clicked.connect(self.planificarVisita)
        self.ubiClima_sitio.clicked.connect(self.verUbicSitio)

    def vaciarDatos(self):
        # Función que vacía los datos ingresados de una visita al cancelarla
        self.ventana.descT.setPlainText("")

    def planificarVisita(self):
        # Función que ayuda al usuario a planificar una visita al sitio seleccionado
        self.ventana = PlanificarTareas()
        self.ventana.closing.connect(self.cerrarVentana)
        self.ventana.cerrar.clicked.connect(self.vaciarDatos)

        self.ventana.tituloLineEdit.setText("Visita a " + (self.sitioComboBox.currentText() if len(self.sitioComboBox.currentText()) > 0 else self.ciudadComboBox.currentText()))
        if self.sitioComboBox.currentIndex() == -1:
            try:
                ciudad = self.conexion.execute("SELECT c.Descripcion FROM Ciudades c WHERE c.Nombre = ?", (self.ciudadComboBox.currentText(),)).fetchone()
                if ciudad[0] != None:
                    self.ventana.descT.setPlainText(str(ciudad[0]))
                self.ventana.show()

            except sqlite3.Error as e:
                print(e)
            except Exception as e:
                print(e)
        else:
            self.ventana.descT.setPlainText(self.desc_Sitio.toPlainText())
            self.ventana.show()

    def verUbicSitio(self):
        # Función que permite al usuario ver el clima y la ubicación actual en un mapa
        try:
            self.ventana = Actualidad(self.ciudadComboBox.currentText())
            self.ventana.closing.connect(self.cerrarVentana)
            self.ventana.show()
        except Exception as e:
            print(e)

    def exportarHTML(self):
        # Función que permitirá exportar la información de la ciudad y del sitio seleccionados en un documento HTML
        if self.ciudadComboBox.currentIndex() != -1 and self.sitioComboBox.currentIndex() != -1:
            buffer1 = QBuffer()
            buffer1.open(QIODevice.WriteOnly)

            buffer2 = QBuffer()
            buffer2.open(QIODevice.WriteOnly)

            self.img_Ciudad.pixmap().save(buffer1, "PNG")
            self.img_Sitio.pixmap().save(buffer2, "PNG")

            byte_array1 = buffer1.data()
            binary_data1 = bytes(byte_array1)
            buffer1.close()

            byte_array2 = buffer2.data()
            binary_data2 = bytes(byte_array2)
            buffer2.close()

            base64_encoded_data1 = base64.b64encode(binary_data1)
            base64_string1 = base64_encoded_data1.decode('ascii')

            base64_encoded_data2 = base64.b64encode(binary_data2)
            base64_string2 = base64_encoded_data2.decode('ascii')

            mime_type = "image/png"
            imgCiudad_URL = f"data:{mime_type};base64,{base64_string1}"
            imgSitio_URL = f"data:{mime_type};base64,{base64_string2}"

            info = "<!DOCTYPE html> " + "<html>" + "<head>" + "<title>" + self.nombreCiudad.text() + "-" + self.nombreSitio.text() + "</title>" + "<style>" + "img{width:241px;height:181px;vertical-align:middle;object-fit:contain;}" + "div{width:241px;text-align:center;}" + "#desc_Ciudad{width:723px;text-align:left;}" + "#desc_Sitio{width:723px;text-align:left;}" + "h3{font-size:20px;}" + "p{font-size:14px;}" + "</style>" + "</head>" + "<body><div id=\"Ciudad\"><img src=\"" + imgCiudad_URL + "\"/><br/><h3 id=\"nombreCiudad\">" + self.nombreCiudad.text() + "</h3><br/></div><div id=\"desc_Ciudad\"><p>" + self.desc_C + "</p></div><br/><br/><br/><br/><div id=\"Sitio\">" + "<img src=\"" + imgSitio_URL + "\"/><br/><h3 id=\"nombreSitio\">" + self.nombreSitio.text() + "</h3><br/></div><div id=\"desc_Sitio\"><p>" + self.desc_S + "</p></div></body></html>"
            ruta_HTML = QFileDialog.getExistingDirectory(self, "Seleccionar destino de exportación a HTML", str(Path.home()), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

            if ruta_HTML:
                directorio_path = Path(ruta_HTML)
                nombreHTML = self.ciudadComboBox.currentText() + "-" + self.sitioComboBox.currentText() + ".html"
                destinoHTML = directorio_path / nombreHTML

                try:
                    with open(destinoHTML, "w", encoding="utf-8") as f:
                        f.write(info)

                        msg_box = QMessageBox(self)
                        msg_box.setIcon(QMessageBox.Information)
                        msg_box.setWindowTitle("Resultado")
                        msg_box.setInformativeText(f"HTML exportado correctamente a:\n{destinoHTML}")
                        msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                        msg_box.exec()

                except Exception as e:
                    QMessageBox.critical(self, "Error de Exportación", f"No se pudo guardar el archivo HTML.\nDetalle: {e}")
        else:
            QMessageBox.information(None, "Aviso", "No se ha seleccionado ninguna ciudad y sitio")

    def exportarPDF(self):
        # Función que permite al usuario exportar un PDF con información de la ciudad y sitio elegidos
        if self.ciudadComboBox.currentIndex() != -1 and self.sitioComboBox.currentIndex() != -1:
            ruta_PDF = QFileDialog.getExistingDirectory(None, "Seleccionar destino de exportación a PDF", str(Path.home()), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
            
            if ruta_PDF:
                directorio_path = Path(ruta_PDF)
                nombrePDF = self.ciudadComboBox.currentText() + "-" + self.sitioComboBox.currentText() + ".pdf"
                ficheroSalida = directorio_path / nombrePDF

                #Convertir las imágenes a Base64 para que sean visibles
                buffer1 = QBuffer()
                buffer1.open(QIODevice.WriteOnly)

                buffer2 = QBuffer()
                buffer2.open(QIODevice.WriteOnly)

                self.img_Ciudad.pixmap().save(buffer1, "PNG")
                self.img_Sitio.pixmap().save(buffer2, "PNG")

                byte_array1 = buffer1.data()
                binary_data1 = bytes(byte_array1)
                buffer1.close()

                byte_array2 = buffer2.data()
                binary_data2 = bytes(byte_array2)
                buffer2.close()

                base64_encoded_data1 = base64.b64encode(binary_data1)
                base64_string1 = base64_encoded_data1.decode('ascii')

                base64_encoded_data2 = base64.b64encode(binary_data2)
                base64_string2 = base64_encoded_data2.decode('ascii')

                mime_type = "image/png"
                imgCiudad_URL = f"data:{mime_type};base64,{base64_string1}"
                imgSitio_URL = f"data:{mime_type};base64,{base64_string2}"

                info = "<!DOCTYPE html> " + "<html>" + "<head>" + "<title>" + self.nombreCiudad.text() + "-" + self.nombreSitio.text() + "</title>" + "<style>" + "img{width:241px;height:181px;vertical-align:middle;object-fit:contain;}" + "div{width:241px;text-align:center;}" + "#desc_Ciudad{width:723px;text-align:left;}" + "#desc_Sitio{width:723px;text-align:left;}" + "h3{font-size:20px;}" + "p{font-size:14px;}" + "</style>" + "</head>" + "<body><div id=\"Ciudad\"><img src=\"" + imgCiudad_URL + "\"/><br/><h3 id=\"nombreCiudad\">" + self.nombreCiudad.text() + "</h3><br/></div><div id=\"desc_Ciudad\"><p>" + self.desc_C + "</p></div><br/><br/><br/><br/><div id=\"Sitio\">" + "<img src=\"" + imgSitio_URL + "\"/><br/><h3 id=\"nombreSitio\">" + self.nombreSitio.text() + "</h3><br/></div><div id=\"desc_Sitio\"><p>" + self.desc_S + "</p></div></body></html>"
                try:
                    html = io.BytesIO(info.encode("utf-8"))
                    output_file = open(str(ficheroSalida), "wb")
                    pisa_status = pisa.CreatePDF(html, dest=output_file, encoding="utf-8")
                    output_file.close()

                    if not pisa_status.err:
                        msg_box = QMessageBox(self)
                        msg_box.setIcon(QMessageBox.Information)
                        msg_box.setWindowTitle("Resultado")
                        msg_box.setInformativeText(f"PDF exportado correctamente a:\n{ficheroSalida}")
                        msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                        msg_box.exec()
                    else:
                        QMessageBox.critical(None, "Error", "Error al exportar el fichero a PDF")

                except Exception as e:
                    print(e)
                    QMessageBox.critical(None, "Error", "Error al exportar el fichero a PDF")
        else:
            QMessageBox.information(None, "Aviso", "No se ha seleccionado ninguna ciudad y sitio")

    def cargarSitio(self):
        # Función que oculta el mensaje de ciudad no seleccionada cuando el usuario selecciona un sitio
        self.aviso_ciudadNoSeleccionada.hide()
        if self.sitioComboBox.currentIndex() != -1:
            self.frame_sitios.show()
            self.planificar_visita.show()
            self.ubiClima_sitio.show()
            self.nombreSitio.setText(self.sitioComboBox.currentText())
            self.nombreCiudad.setText(self.ciudadComboBox.currentText())

            idC = self.conexion.execute("SELECT c.ID FROM Ciudades c WHERE c.Nombre = ?", (self.ciudadComboBox.currentText(),)).fetchone()
            idCiudad = int(idC[0])

            sitio = self.conexion.execute("SELECT c.Descripcion, c.Imagen, s.Descripcion, s.Imagen FROM Ciudades c, Sitios s WHERE s.Nombre = ? AND s.Ciudad = ? AND s.Ciudad = c.ID", (self.sitioComboBox.currentText(), idCiudad,)).fetchone()
            if sitio:
                self.aviso_sitio.hide()

                descC = sitio[0]
                imagenC = sitio[1]
                descS = sitio[2]
                imagenS = sitio[3]

                # Sacar imagen de la BD
                pixmapC = QPixmap()
                pixmapC.loadFromData(imagenC, "PNG")

                pixmapS = QPixmap()
                pixmapS.loadFromData(imagenS, "PNG")

                if not pixmapC.isNull():
                    self.img_Ciudad.setPixmap(pixmapC)
                    self.img_Ciudad.setScaledContents(True)

                if not pixmapS.isNull():
                    self.img_Sitio.setPixmap(pixmapS)
                    self.img_Sitio.setScaledContents(True)

                self.desc_C = self.ciudadComboBox.currentText() + ": " + str(descC)
                self.desc_S = self.sitioComboBox.currentText() + ": " + str(descS)
                self.desc_Sitio.setPlainText(self.desc_C + "\n\n\n" + self.desc_S)

                self.desc_C = str(descC)
                self.desc_S = str(descS)
    
    def cargarSitiosCiudad(self):
        # Función que carga los sitios de la ciudad elegida
        if self.ciudades > 0:
            self.planificar_visita.show()
            self.ubiClima_sitio.show()

            self.sitioComboBox.clear()
            self.frame_sitios.hide()
            self.aviso_ciudadNoSeleccionada.hide()
            self.aviso_sitio.hide()

            cID = self.conexion.execute("SELECT c.ID FROM Ciudades c WHERE c.Nombre = ?", (self.ciudadComboBox.currentText(),))
            ciudadID = cID.fetchone()

            if ciudadID:
                self.IDCiudad = int(ciudadID[0])

                sitios = self.conexion.execute("SELECT s.Nombre FROM Sitios s WHERE s.Ciudad = ? ORDER BY s.Nombre", (int(ciudadID[0]),)).fetchall()
                for sitio in sitios:
                    self.sitioComboBox.addItem(sitio[0])
                    self.frame_sitios.hide()
                    self.sitioComboBox.setCurrentIndex(-1)

                if self.sitioComboBox.count() > 0:
                    self.aviso_ciudadNoSeleccionada.hide()

                    self.aviso_sitio.setText("SELECCIONE UN SITIO")
                    self.aviso_sitio.show()
                else:
                    self.aviso_ciudadNoSeleccionada.hide()

                    self.aviso_sitio.setText(self.ciudadComboBox.currentText() + " NO TIENE SITIOS ASOCIADOS")
                    self.aviso_sitio.show()
            else:
                self.aviso_sitio.setText(self.ciudadComboBox.currentText() + " NO TIENE SITIOS ASOCIADOS")
                self.aviso_sitio.show()
                self.frame_sitios.hide()

    def cargarCiudades(self):
        # Función que carga las ciudades guardadas en la BD
        if self.conexion:
            ciudades = self.conexion.execute("SELECT Nombre FROM Ciudades ORDER BY Nombre")
            for ciudad in ciudades.fetchall():
                self.ciudadComboBox.addItem(ciudad[0])
                self.frame_sitios.hide()
                self.ciudadComboBox.setCurrentIndex(-1)

            if self.ciudadComboBox.count() > 0:
                self.aviso_ciudadNoSeleccionada.show()
                return self.ciudadComboBox.count()
            else:
                QMessageBox.warning(None, "Aviso", "No hay sitios disponibles")
                raise InitialisationError("No hay sitios disponibles")
        else:
            QMessageBox.warning(None, "Aviso", "Error de conexión a la BD")
            raise InitialisationError("Error de conexión a la BD.")

    def closeEvent(self, event):
        # Función que el usuario al cerrar la ventana se le vuelve a la ventana de inicio
        self.closing.emit()
        super().closeEvent(event)

    def cerrarVentana(self):
        self.ventana.close()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    verSitios = VerSitios()
    verSitios.show()
    sys.exit(app.exec())
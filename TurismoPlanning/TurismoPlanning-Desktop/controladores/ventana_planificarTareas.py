import sys, os, shutil, sqlite3, io, base64
from pathlib import Path
from xhtml2pdf import pisa
from PySide6.QtWidgets import QWidget, QApplication, QMessageBox, QTreeWidgetItem, QFileDialog
from PySide6.QtCore import Signal, QDate, QTime, QBuffer, QIODevice, QSize
from PySide6.QtGui import QIcon, QPixmap, Qt
from controladores.ventana_crearCategoria import CrearCategoria
from vistas.planificarEventos_ui import Ui_planificarTareas

class PlanificarTareas(QWidget, Ui_planificarTareas):
    closing = Signal()

    def __init__(self, fecha=None, editar=None, title=None):
        super().__init__()
        self.setupUi(self)

        # Variables auxiliares
        self.ventana = 0
        self.fecha = fecha if fecha != None else None
        self.icono = None
        self.icTF = False

        self.idT = 0
        self.editarT = editar
        self.tituloT = title
        self.icSeleccionado = False
        
        self.categoriaAnteriorID = 0
        self.FI_Tiene = False
        self.HI_Tiene = False
        self.HF_Tiene = False

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
        __qtreewidgetitem1 = QTreeWidgetItem(self.exportar)
        __qtreewidgetitem1.setIcon(0, QIcon(os.getcwd() + "/recursos/iconos/html.png"))
        __qtreewidgetitem1.setText(0, "HTML")

        __qtreewidgetitem2 = QTreeWidgetItem(self.exportar)
        __qtreewidgetitem2.setIcon(0, QIcon(os.getcwd() + "/recursos/iconos/pdf.png"))
        __qtreewidgetitem2.setText(0, "PDF")

        self.exportar.hide()
        self.refrescar.hide()

        self.cargarCategorias()
        self.adaptar()

        self.horaDeFinalizacionTimeEdit.setMaximumTime(QTime(23, 59))
        self.horaDeFinalizacionTimeEdit.setTime(QTime(23, 59))
        self.prioridadSpinBox.setMinimum(1)
        
        # Añadir iconos
        self.setWindowIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_planificar.png"))
        if not self.editarT or not self.icTF:
            self.icono_seleccionar.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_icono.png"))

        self.crearCategoria.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_add.png"))
        self.refrescar.setIcon(QIcon(os.getcwd() + "/recursos/iconos/refrescar.png"))
        self.cerrar.setIcon(QIcon(os.getcwd() + "/recursos/iconos/cerrar.png"))
        self.guardarTarea.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_guardar.png"))
        self.ayuda.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ayuda.png"))

        # Acciones
        self.icono_seleccionar.clicked.connect(self.seleccionarImagen)
        self.crearCategoria.clicked.connect(self.crearCat)
        self.refrescar.clicked.connect(self.cargarCategorias)
        self.guardarTarea.clicked.connect(self.guardar)
        self.exportar.itemClicked.connect(self.exportarTarea)
        self.ayuda.clicked.connect(self.mostrarAyuda)
        
    def mostrarAyuda(self):
        # Función que muestra una ayuda práctica al usuario
        QMessageBox.information(self, "Ayuda", "Las casillas que dicen \"¿Incluir?\" preguntan si tener o no en cuenta esos campos que están al lado izquierdo de cada casilla. Por ejemplo, ¿quiero incluir la fecha de inicio del evento?")

    def exportarTarea(self, item, columna):
        # Función que exporta la tarea programada del usuario a HTML o PDF
        buffer1 = QBuffer()
        buffer1.open(QIODevice.WriteOnly)
        self.icono_seleccionar.icon().pixmap(50, 50).save(buffer1, "PNG")

        byte_array1 = buffer1.data()
        binary_data1 = bytes(byte_array1)
        buffer1.close()

        base64_encoded_data1 = base64.b64encode(binary_data1)
        base64_string1 = base64_encoded_data1.decode('ascii')

        mime_type = "image/png"
        icTarea_URL = f"data:{mime_type};base64,{base64_string1}"

        formato = item.text(columna)
        html = f"<html><head><style>*{{font-family:Aptos}}h2{{margin-left:32px;margin-bottom:25px;font-size:20px;}}label{{margin-right: 2px;font-size:14px;}}h3{{font-size:17px}}data{{font-size:14px;}}textarea{{font-size:14px;font-family:Aptos}}img{{width:50px;height:50px;object-fit:contain;}}</style></head><body><img src=\"{icTarea_URL}\"/><h2>{self.tituloLineEdit.text()}</h2><label>Fecha de Inicio:  </label><data>{self.fechaDeInicioDateEdit.date().toString("dd/MM/yyyy") if self.incluir_FI.isChecked() or self.FI_Tiene else ""}</data><br/><label>Fecha de Finalización:  </label><data>{self.fechaDeFinalizacionDateEdit.date().toString("dd/MM/yyyy")}</data><br/><br/><label>Hora de Inicio:  </label><data>{self.horaDeInicioTimeEdit.time().toString("HH:mm") if self.incluir_HI.isChecked() or self.HI_Tiene else ""}</data><br/><label>Hora de Finalización:  </label><data>{self.horaDeFinalizacionTimeEdit.time().toString("HH:mm") if self.incluir_HF.isChecked() or self.HF_Tiene else ""}</data><br/><br/><label>Categoría:  </label><data>{self.categoriaComboBox.currentText()}</data><br/><label>Prioridad:  </label><data>{self.prioridadSpinBox.value()}</data><br/><br/><h3>DESCRIPCIÓN</h3><textarea cols=\"100\" rows=\"28\" readonly=\"\">{self.descT.toPlainText()}</textarea></body></html>"

        ruta_fichero = QFileDialog.getExistingDirectory(self, "Seleccionar destino de exportación", str(Path.home()), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if ruta_fichero:
            if formato == "HTML":
                directorio_path = Path(ruta_fichero)
                nombreHTML = self.tituloLineEdit.text() + ".html"
                destinoHTML = directorio_path / nombreHTML
                try:
                    with open(destinoHTML, "w", encoding="utf-8") as h:
                        h.write(html)

                        msg_box = QMessageBox(self)
                        msg_box.setIcon(QMessageBox.Information)
                        msg_box.setWindowTitle("Resultado")
                        msg_box.setInformativeText(f"HTML exportado correctamente a:\n{destinoHTML}")
                        msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                        msg_box.exec()

                except Exception as e:
                    print(e)
                    QMessageBox.critical(None, "Error", "Error al exportar tarea a HTML")

            elif formato == "PDF":
                try:
                    directorio_path = Path(ruta_fichero)
                    nombrePDF = self.tituloLineEdit.text() + ".pdf"
                    destinoPDF = directorio_path / nombrePDF

                    html = io.BytesIO(html.encode("utf-8"))
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
                    else:
                        QMessageBox.critical(None, "Error", "Error al exportar el fichero a PDF")

                except Exception as e:
                    print(e)
                    QMessageBox.critical(None, "Error", "Error al exportar el fichero a PDF")

    def guardar(self):
        # Función que guarda una tarea programada por el usuario
        if self.conexion:
            if len(self.tituloLineEdit.text()) > 0 and self.categoriaComboBox.currentIndex() != -1 and self.prioridadSpinBox.value() > 0:
                if self.fechaDeInicioDateEdit.date() > self.fechaDeFinalizacionDateEdit.date():
                    QMessageBox.warning(None, "Aviso", "La fecha de inicio no puede ser más lejana que la fecha de finalización del evento")
                    return False
                
                elif self.fechaDeInicioDateEdit.date() == self.fechaDeFinalizacionDateEdit.date():
                    if self.horaDeInicioTimeEdit.time() > self.horaDeFinalizacionTimeEdit.time():
                        QMessageBox.warning(None, "Aviso", "La hora de inicio no puede ser más lejana que la hora de finalización del evento")
                        return False
                
                if not self.editarT:
                    # Insertar
                    try:
                        id = self.conexion.execute("SELECT MAX(ID) FROM Tareas").fetchone()
                        idT = 0
                        if id[0] != None:
                            idT = id[0] + 1
                        else:
                            idT = 1

                        id = self.conexion.execute("SELECT c.ID FROM Categorias c WHERE c.Nombre = ?", (self.categoriaComboBox.currentText(),)).fetchone()
                        idC = 0
                        if id[0] != None:
                            idC = id[0]
                        else:
                            idC = None

                        self.conexion.execute("INSERT INTO Tareas VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (idT, self.tituloLineEdit.text(), self.icono, self.descT.toPlainText(), self.fechaDeInicioDateEdit.date().toString("dd/MM/yyyy") if self.incluir_FI.isChecked() else None, self.horaDeInicioTimeEdit.time().toString("HH:mm") if self.incluir_HI.isChecked() else None, self.fechaDeFinalizacionDateEdit.date().toString("dd/MM/yyyy"), self.horaDeFinalizacionTimeEdit.time().toString("dd/MM/yyyy") if self.incluir_HF.isChecked() else None, self.prioridadSpinBox.value(), idC,))
                        self.conexion.commit()

                        QMessageBox.information(None, "Resultado", "Tarea programada correctamente para el " + self.fechaDeFinalizacionDateEdit.date().toString("dd/MM/yyyy"))
                        self.exportar.show()

                    except sqlite3.IntegrityError as e:
                        print(e)
                        self.conexion.rollback()
                        QMessageBox.warning(None, "Aviso", "Ya existe otra tarea con ese título")

                    except sqlite3.Error as e:
                        print(e)
                        self.conexion.rollback()
                        QMessageBox.critical(None, "Error", "Error al programar el evento")
                else:
                    # Modificar
                    try:
                        tareaM = self.conexion.execute("SELECT t.ID, t.Icono, t.Descripcion, t.Fecha_Inicio, t.Hora_Inicio, t.Plazo_Fecha, t.Plazo_Hora, t.Prioridad FROM Tareas t WHERE t.ID = ?", (self.idT,)).fetchone()
                        if tareaM[0] != None:
                            idT = tareaM[0]
                            icono = tareaM[1]
                            FI = tareaM[3]
                            HI = tareaM[4]
                            HF = tareaM[6]

                            idCat = self.conexion.execute("SELECT c.ID FROM Categorias c WHERE c.Nombre = ?", (self.categoriaComboBox.currentText(),)).fetchone()
                            
                            buffer = QBuffer()
                            buffer.open(QIODevice.WriteOnly)

                            ic = self.icono_seleccionar.icon().pixmap(32, 32).save(buffer, "PNG")
                            if not ic:
                                buffer.close()
                            elif self.icSeleccionado:
                                byte_array = buffer.data()
                                buffer.close()
                                self.icono = bytes(byte_array)

                            self.conexion.execute("UPDATE Tareas SET Titulo = ?, Icono = ?, Descripcion = ?, Fecha_Inicio = ?, Hora_Inicio = ?, Plazo_Fecha = ?, Plazo_Hora = ?, Prioridad = ?, Categoria = ? WHERE ID = ?", (self.tituloLineEdit.text(), self.icono if self.icono != None else icono, self.descT.toPlainText(), self.fechaDeInicioDateEdit.date().toString("dd/MM/yyyy") if self.incluir_FI.isChecked() else FI, self.horaDeInicioTimeEdit.time().toString("HH:mm") if self.incluir_HI.isChecked() else HI, self.fechaDeFinalizacionDateEdit.date().toString("dd/MM/yyyy"), self.horaDeFinalizacionTimeEdit.time().toString("HH:mm") if self.incluir_HF.isChecked() else HF, self.prioridadSpinBox.value(), idCat[0] if idCat[0] != None and self.categoriaComboBox.currentIndex() != -1 else self.categoriaAnteriorID, idT,))
                            self.conexion.commit()

                            QMessageBox.information(self, "Resultado", "Evento modificado con éxito")
                            self.exportar.show()

                    except sqlite3.IntegrityError as e:
                        print(e)
                        self.conexion.rollback()
                        QMessageBox.warning(None, "Aviso", "Ya existe otra tarea con ese título")

                    except sqlite3.Error as e:
                        print(e)
                        self.conexion.rollback()
                        QMessageBox.critical(None, "Error", "Error al modificar el evento")        
            else:
                QMessageBox.warning(None, "Aviso", "Faltan valores por rellenar")
        else:
            QMessageBox.critical(None, "Error", "Error de conexión a la BD")

    def cargarCategorias(self):
        # Función que carga el listado de categorías creadas que puede seleccionar el usuario
        if self.conexion:
            self.categoriaComboBox.clear()

            filas = self.conexion.execute("SELECT c.Nombre FROM Categorias c").fetchall()
            for f in filas:
                self.categoriaComboBox.addItem(f[0])
                self.categoriaComboBox.setCurrentIndex(-1)

            self.refrescar.hide()
        else:
            QMessageBox.critical(None, "Error", "Error de conexión a la BD")

    def crearCat(self):
        # Función que permite al usuario crear una nueva categoría
        self.ventana = CrearCategoria()
        self.ventana.cerrar.clicked.connect(self.refrescar.hide)
        self.ventana.guardarCategoria.clicked.connect(self.cargarCategorias)
        self.ventana.guardarCategoria.clicked.connect(self.refrescar.show)
        self.ventana.show()

    def seleccionarImagen(self):
        # Función que permite al usuario seleccionar una imagen para añadir una ciudad
        ruta_imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar icono", "", "Archivos de Imagen (*.png *.jpg *.jpeg *.bmp)")
        if ruta_imagen:
            icono = QIcon(ruta_imagen)
            self.icono_seleccionar.setIcon(icono)
            # Convertimos la imagen para que sea insertable en la BD
            buffer = QBuffer()
            abrir = buffer.open(QIODevice.WriteOnly)
            if abrir:
                pixmap = icono.pixmap(32, 32)
                guardado = pixmap.save(buffer, "PNG")
                if not guardado:
                    buffer.close()
                else:
                    byte_array = buffer.data()
                    buffer.close()
                    self.icono = bytes(byte_array)

                    self.icSeleccionado = True


    def adaptar(self):
        # Función que adapta el formulario a la fecha pulsada en el calendario de la ventana main
        if self.fecha:
            self.fechaDeInicioDateEdit.setMinimumDate(QDate.currentDate())
            self.fechaDeInicioDateEdit.setDate(self.fecha if self.fecha != None else QDate.currentDate())
            self.fechaDeFinalizacionDateEdit.setMinimumDate(QDate.currentDate())
            self.fechaDeFinalizacionDateEdit.setDate(self.fecha if self.fecha != None else QDate.currentDate())
        else:
            self.fechaDeInicioDateEdit.setMinimumDate(QDate.currentDate())
            self.fechaDeInicioDateEdit.setDate(QDate.currentDate())
            self.fechaDeFinalizacionDateEdit.setMinimumDate(QDate.currentDate())
            self.fechaDeFinalizacionDateEdit.setDate(QDate.currentDate())

        if self.editarT:
            try:
                tareaM = self.conexion.execute("SELECT t.ID, t.Icono, t.Descripcion, t.Fecha_Inicio, t.Hora_Inicio, t.Plazo_Fecha, t.Plazo_Hora, t.Prioridad, t.Categoria FROM Tareas t WHERE t.Titulo = ?", (self.tituloT,)).fetchone()
                if tareaM[0] != None:
                    self.idT = tareaM[0]
                    icono = tareaM[1]
                    desc = tareaM[2]
                    FI = tareaM[3]
                    HI = tareaM[4]
                    FF = tareaM[5]
                    HF = tareaM[6]
                    prioridad = tareaM[7]
                    self.categoriaAnteriorID = tareaM[8]

                    if FI != None:
                        self.FI_Tiene = True
                    if HI != None:
                        self.HI_Tiene = True
                    if HF != None:
                        self.HF_Tiene = True

                    categoriaNombre = ""
                    if self.categoriaAnteriorID > 0:
                        categoriaNombre = self.conexion.execute("SELECT c.Nombre FROM Categorias c WHERE c.ID = ?", (self.categoriaAnteriorID,)).fetchone()
                        if categoriaNombre[0] != None:
                            indice = self.categoriaComboBox.findText(categoriaNombre[0])
                            self.categoriaComboBox.setCurrentIndex(indice)

                    self.tituloLineEdit.setText(self.tituloT)
                    # Cargar icono
                    if icono != None:
                        pixmap = QPixmap()
                        if pixmap.loadFromData(icono, "PNG"):
                            scaled_pixmap = pixmap.scaled(QSize(44, 44),
                                      Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
                            
                            icon = QIcon(scaled_pixmap)
                            self.icono_seleccionar.setIcon(icon)
                            self.icTF = True
                        else:
                            self.icTF = False
                    else:
                        self.icTF = False
                    
                    self.descT.setPlainText(desc)
                    self.fechaDeInicioDateEdit.setDate(QDate().fromString(FI, "dd/MM/yyyy"))
                    self.fechaDeFinalizacionDateEdit.setDate(QDate().fromString(FF, "dd/MM/yyyy"))
                    self.horaDeInicioTimeEdit.setTime(QTime().fromString(HI, "HH:mm"))
                    self.horaDeFinalizacionTimeEdit.setTime(QTime().fromString(HF, "HH:mm"))
                    self.prioridadSpinBox.setValue(prioridad)

                    self.exportar.show()

            except sqlite3.Error as e:
                print(e)
                self.conexion.rollback()
                QMessageBox.critical(None, "Error", "Error al cargar el evento")     

    def closeEvent(self, event):
        # Función que el usuario al cerrar la ventana se le vuelve a la ventana de inicio
        self.closing.emit()
        super().closeEvent(event)

    def cerrarVentana(self):
        self.descT.setPlainText("")

        self.ventana.close()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    planificar = PlanificarTareas()
    planificar.show()
    sys.exit(app.exec())
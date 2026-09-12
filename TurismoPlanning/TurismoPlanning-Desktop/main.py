import sys, os, shutil, sqlite3
from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDate
from modelos.InitialisationError import InitialisationError
from vistas.main_ui import Ui_main
from controladores.ventana_sitiosTuristicos import VerSitios
from controladores.ventana_Actualidad import Actualidad
from controladores.ventana_Notas import Notas
from controladores.ventana_planificarTareas import PlanificarTareas
from controladores.ventana_gestionarCategorias import Categorias
from controladores.ventana_eventosProgramados import EventosPlanificados

class Main(QMainWindow, Ui_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Variables auxiliares
        self.ventana = 0
        
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
        self.setWindowIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_main.png"))
        self.actionSitios.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_Sitios.png"))
        self.actionActualidad.setIcon(QIcon(os.getcwd() + "/recursos/iconos/UbiClima.png"))
        self.actionCrear.setIcon(QIcon(os.getcwd() + "/recursos/iconos/crearNota.png"))
        self.actionAbrir.setIcon(QIcon(os.getcwd() + "/recursos/iconos/abrir-documento.png"))
        self.actionCreditos.setIcon(QIcon(os.getcwd() + "/recursos/iconos/informacion.png"))
        self.actionAyuda.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ayuda.png"))
        self.verEventos.setIcon(QIcon(os.getcwd() + "/recursos/iconos/eventos.png"))
        self.priorizarCategorias.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_ordenarCategorias.png"))
        self.planificarTarea.setIcon(QIcon(os.getcwd() + "/recursos/iconos/ic_planificar"))

        self.calendarioEventos.setMinimumDate(QDate.currentDate())
        self.eventosPasados()

        # Acciones
        self.actionSitios.triggered.connect(self.verSitios)
        self.actionActualidad.triggered.connect(self.verUbiClimaActual)

        self.actionCrear.triggered.connect(self.crearNota)
        self.actionAbrir.triggered.connect(self.abrirNota)

        self.calendarioEventos.clicked.connect(self.planificarEvento)
        self.planificarTarea.clicked.connect(self.planificarEvento)

        self.priorizarCategorias.clicked.connect(self.listadoCategorias)
        self.verEventos.clicked.connect(self.eventosPlanificados)

        self.actionCreditos.triggered.connect(self.mostrarCreditos)
        self.actionAyuda.triggered.connect(self.mostrarAyuda)
    
    def eventosPasados(self):
        # Función que busca elementos pasados de fecha y los elimina
        if self.conexion:
            fechaHoy = QDate.currentDate().toString("dd/MM/yyyy")
            try:
                self.conexion.execute("DELETE FROM Tareas WHERE Plazo_Fecha < ?", (fechaHoy,))
                self.conexion.commit()

            except sqlite3.Error as e:
                print(e)
                QMessageBox.critical(self, "Error", "Error al eliminar eventos pasados de fecha")
        else:
            QMessageBox.critical(self, "Error", f"Error al conectarse a la BD")

    def eventosPlanificados(self):
        # Función que permite al usuario ver los eventos planificados según la categoría
        if self.conexion:
            try:
                idE = self.conexion.execute("SELECT MAX(ID) FROM Categorias").fetchone()
                if idE[0] != None:
                    self.ventana = EventosPlanificados()
                    self.ventana.closing.connect(self.cerrarVentana)
                    self.ventana.show()
                else:
                    QMessageBox.warning(self, "Aviso", "No hay eventos programados, planifica uno primero")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar: {e}")
        else:
            QMessageBox.critical(self, "Error", f"Error al conectarse a la BD")

    def listadoCategorias(self):
        # Función que permite al usuario ver las categorías ordenadas por prioridad con todos sus datos y editarlas o eliminarlas
        if self.conexion:
            try:
                idC = self.conexion.execute("SELECT MAX(ID) FROM Categorias").fetchone()
                if idC[0] != None:
                    self.ventana = Categorias()
                    self.ventana.closing.connect(self.cerrarVentana)
                    self.ventana.show()
                else:
                    QMessageBox.warning(self, "Aviso", "No hay categorías creadas, planifica un evento primero")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar: {e}")
        else:
            QMessageBox.critical(self, "Error", f"Error al conectarse a la BD")

    def planificarEvento(self, fecha=None):
        # Función que le permite al usuario planificar una tarea programada o evento
        self.ventana = PlanificarTareas(fecha)
        self.ventana.closing.connect(self.cerrarVentana)
        self.ventana.show()

    def abrirNota(self):
        # Función que permite al usuario editar una nota de texto
        rutafichero, _ = QFileDialog.getOpenFileName(None, "Seleccionar fichero de texto", "", "Archivos de Texto (*.txt)")
        if rutafichero:
            with open(rutafichero, "r", encoding="utf-8") as fichero:
                try:
                    contenido = fichero.read()

                    self.ventana = Notas(rutafichero)
                    self.ventana.setWindowTitle("Notas - " + rutafichero)
                    self.ventana.texto.setText(contenido)
                    self.ventana.closing.connect(self.cerrarVentana)
                    self.ventana.show()
                    
                except Exception as e:
                    print(e)
                    msg_box = QMessageBox(self)
                    msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
                    msg_box.setIcon(QMessageBox.Critical)
                    msg_box.setWindowTitle("Error")
                    msg_box.setInformativeText("Fichero de texto no válido")
                    msg_box.exec()

    def crearNota(self):
        # Función que permite al usuario crear una nota de texto
        self.ventana = Notas()
        self.ventana.closing.connect(self.cerrarVentana)
        self.ventana.show()

    def verUbiClimaActual(self):
        # Función que permitirá al usuario ver la ubicación y clima actual en un mapa
        try:
            self.ventana = Actualidad()
            self.ventana.closing.connect(self.cerrarVentana)
            self.ventana.show()
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Error", f"Error al cargar: {e}")

    def verSitios(self):
        # Función que permitirá al usuario ver ciudades y sitios asociados, incluso su ubicación y clima en un mapa
        if self.conexion:
            try:
                idS = self.conexion.execute("SELECT MAX(ID) FROM Sitios s").fetchone()
                if idS[0] != None:
                    self.ventana = VerSitios()
                    self.ventana.closing.connect(self.cerrarVentana)
                    self.ventana.show()
                else:
                    QMessageBox.warning(self, "Aviso", "No hay sitios turísticos disponibles")

            except InitialisationError as e:
                print(e)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar: {e}")
        else:
            QMessageBox.critical(self, "Error", f"Error al cargar: {e}")

    def mostrarCreditos(self):
        # Función que muestra al usuario información adicional sobre el programa
        info = "Esta aplicación ha sido diseñada para ayudar al usuario a organizarse en su día a día. También se le muestran unos sitios turísticos de interés al usuario además de poder orientarse mediante un mapa y tomar apuntes.\n\nAutor: Sergio Romero Tejedor\nVersión: 1.0\nFecha de Lanzamiento: 29/05/2025" 
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Créditos")
        msg_box.setInformativeText(info)
        msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
        msg_box.exec()
    
    def mostrarAyuda(self):
        # Función que muestra una ayuda práctica al usuario a utilizar el programa
        info = "1. Calendario: Haz clic a un día del calendario para planificar un evento con el día seleccionado automáticamente.\n\n2. Gestionar categorías: Este botón naranja es para ver ordenadas por prioridad las categorías del usuario y que pueda editar sus datos o directamente eliminarlas e incluso crear otras nuevas.\n\n3. Planificar: Este botón morado es para que el usuario pueda planificar sus eventos cuando quiera.\n\n4. Turismo: Este menú es para que el usuario pueda ver sitios turísticos de su interés agrupados por ciudades. Y también puede ver la ubicación y clima según donde esté, e incluso la de un sitio que haya seleccionado antes."
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Ayuda")
        msg_box.setInformativeText(info)
        msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
        msg_box.exec()

    def cerrarVentana(self):
        self.ventana.close()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())
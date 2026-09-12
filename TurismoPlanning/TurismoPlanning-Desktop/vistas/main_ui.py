# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QFrame, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QWidget)

class Ui_main(object):
    def setupUi(self, main):
        if not main.objectName():
            main.setObjectName(u"main")
        main.setWindowModality(Qt.WindowModality.WindowModal)
        main.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main.sizePolicy().hasHeightForWidth())
        main.setSizePolicy(sizePolicy)
        main.setMaximumSize(QSize(800, 600))
        main.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        main.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u"../recursos/iconos/ic_main.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        main.setWindowIcon(icon)
        main.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);")
        main.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.actionSitios = QAction(main)
        self.actionSitios.setObjectName(u"actionSitios")
        icon1 = QIcon()
        icon1.addFile(u"../recursos/iconos/ic_Sitios.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionSitios.setIcon(icon1)
        font = QFont()
        font.setPointSize(10)
        self.actionSitios.setFont(font)
        self.actionSitios.setIconVisibleInMenu(True)
        self.actionCrear = QAction(main)
        self.actionCrear.setObjectName(u"actionCrear")
        icon2 = QIcon()
        icon2.addFile(u"../recursos/iconos/crearNota.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionCrear.setIcon(icon2)
        font1 = QFont()
        self.actionCrear.setFont(font1)
        self.actionAbrir = QAction(main)
        self.actionAbrir.setObjectName(u"actionAbrir")
        icon3 = QIcon()
        icon3.addFile(u"../recursos/iconos/abrir-documento.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionAbrir.setIcon(icon3)
        self.actionAbrir.setFont(font1)
        self.actionCreditos = QAction(main)
        self.actionCreditos.setObjectName(u"actionCreditos")
        icon4 = QIcon()
        icon4.addFile(u"../recursos/iconos/informacion.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionCreditos.setIcon(icon4)
        self.actionCreditos.setFont(font1)
        self.actionAyuda = QAction(main)
        self.actionAyuda.setObjectName(u"actionAyuda")
        icon5 = QIcon()
        icon5.addFile(u"../recursos/iconos/ayuda.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionAyuda.setIcon(icon5)
        self.actionAyuda.setFont(font1)
        self.actionActualidad = QAction(main)
        self.actionActualidad.setObjectName(u"actionActualidad")
        icon6 = QIcon()
        icon6.addFile(u"../recursos/iconos/UbiClima.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionActualidad.setIcon(icon6)
        self.centralwidget = QWidget(main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 801, 567))
        self.frame.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.frame.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(30, 30, 30);")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.planificarTarea = QPushButton(self.frame)
        self.planificarTarea.setObjectName(u"planificarTarea")
        self.planificarTarea.setGeometry(QRect(670, 30, 121, 41))
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        self.planificarTarea.setFont(font2)
        self.planificarTarea.setStyleSheet(u"background-color: rgb(170, 0, 255);\n"
"color: rgb(0, 0, 0);")
        icon7 = QIcon()
        icon7.addFile(u"../recursos/iconos/ic_planificar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.planificarTarea.setIcon(icon7)
        self.planificarTarea.setIconSize(QSize(32, 24))
        self.calendarioEventos = QCalendarWidget(self.frame)
        self.calendarioEventos.setObjectName(u"calendarioEventos")
        self.calendarioEventos.setGeometry(QRect(10, 100, 781, 461))
        font3 = QFont()
        font3.setPointSize(12)
        self.calendarioEventos.setFont(font3)
        self.calendarioEventos.setStyleSheet(u"/* Cambiar el color de fondo del widget */\n"
"QCalendarWidget {\n"
"    background-color: lightblue;\n"
"}\n"
"\n"
"/* Estilizar el encabezado del mes/a\u00f1o */\n"
"QCalendarWidget QWidget#qt_calendar_navigationbar {\n"
"    background-color: rgb(0, 85, 255);\n"
"    color: white;\n"
"}\n"
"\n"
"/* Estilizar los botones de navegaci\u00f3n */\n"
"QCalendarWidget QToolButton {\n"
"    background-color: rgb(30, 30, 30);\n"
"    color: white;\n"
"    border: 3px solid rgb(255, 255, 0);\n"
"	border-radius: 10px;\n"
"    width:100px;\n"
"    height:40px;\n"
"	margin:5px;\n"
"	icon-size: 40px 40px;\n"
"	\n"
"	font: 700 14pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* Estilizar el d\u00eda actual */\n"
"QCalendarWidget QDateText[current=\"true\"] {\n"
"    background-color: yellow;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* Estilizar los fines de semana */\n"
"QCalendarWidget QDateText[weekend=\"true\"] {\n"
"    color: red;\n"
"}\n"
"\n"
"/* Estilizar la celda seleccionada */\n"
"QCalendarWidget QAbstractItemView:focus {\n"
""
                        "    outline: none; /* Eliminar el borde de foco predeterminado */\n"
"}\n"
"\n"
"QCalendarWidget QAbstractItemView::item:selected {\n"
"    background-color: blue;\n"
"    color: white;\n"
"}\n"
"\n"
"/* A\u00f1adir un borde a las celdas de los d\u00edas (esto es m\u00e1s complejo y puede no funcionar perfectamente en todos los estilos base) */\n"
"QCalendarWidget QAbstractItemView::item {\n"
"    border: 3px solid rgb(111, 111, 111);\n"
"} ")
        self.calendarioEventos.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        self.calendarioEventos.setGridVisible(True)
        self.calendarioEventos.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
        self.calendarioEventos.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.LongDayNames)
        self.calendarioEventos.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendarioEventos.setNavigationBarVisible(True)
        self.calendarioEventos.setDateEditEnabled(True)
        self.verEventos = QPushButton(self.frame)
        self.verEventos.setObjectName(u"verEventos")
        self.verEventos.setGeometry(QRect(10, 30, 191, 41))
        self.verEventos.setFont(font2)
        self.verEventos.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"background-color: rgb(0, 170, 255);")
        icon8 = QIcon()
        icon8.addFile(u"../recursos/iconos/eventos.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.verEventos.setIcon(icon8)
        self.verEventos.setIconSize(QSize(32, 24))
        self.priorizarCategorias = QPushButton(self.frame)
        self.priorizarCategorias.setObjectName(u"priorizarCategorias")
        self.priorizarCategorias.setGeometry(QRect(300, 30, 211, 41))
        self.priorizarCategorias.setFont(font2)
        self.priorizarCategorias.setStyleSheet(u"background-color: orange;\n"
"color: rgb(0, 0, 0);")
        icon9 = QIcon()
        icon9.addFile(u"../recursos/iconos/ic_ordenarCategorias.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.priorizarCategorias.setIcon(icon9)
        self.priorizarCategorias.setIconSize(QSize(32, 32))
        main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        font4 = QFont()
        font4.setPointSize(9)
        self.menubar.setFont(font4)
        self.menubar.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(40, 40, 40);\n"
"border-bottom:2px solid blue;")
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menuSitios = QMenu(self.menubar)
        self.menuSitios.setObjectName(u"menuSitios")
        self.menuSitios.setGeometry(QRect(267, 147, 153, 100))
        self.menuSitios.setFont(font)
        self.menuSitios.setTearOffEnabled(False)
        self.menuSitios.setSeparatorsCollapsible(False)
        self.menuSitios.setToolTipsVisible(False)
        self.menuNotas = QMenu(self.menubar)
        self.menuNotas.setObjectName(u"menuNotas")
        self.menuNotas.setFont(font)
        self.menuM_s_informaci_n = QMenu(self.menubar)
        self.menuM_s_informaci_n.setObjectName(u"menuM_s_informaci_n")
        self.menuM_s_informaci_n.setFont(font)
        main.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuSitios.menuAction())
        self.menubar.addAction(self.menuNotas.menuAction())
        self.menubar.addAction(self.menuM_s_informaci_n.menuAction())
        self.menuSitios.addAction(self.actionSitios)
        self.menuSitios.addAction(self.actionActualidad)
        self.menuNotas.addAction(self.actionCrear)
        self.menuNotas.addAction(self.actionAbrir)
        self.menuM_s_informaci_n.addSeparator()
        self.menuM_s_informaci_n.addAction(self.actionCreditos)
        self.menuM_s_informaci_n.addAction(self.actionAyuda)

        self.retranslateUi(main)

        QMetaObject.connectSlotsByName(main)
    # setupUi

    def retranslateUi(self, main):
        main.setWindowTitle(QCoreApplication.translate("main", u"Principal", None))
        self.actionSitios.setText(QCoreApplication.translate("main", u"Sitios", None))
#if QT_CONFIG(tooltip)
        self.actionSitios.setToolTip(QCoreApplication.translate("main", u"Ver sitios", None))
#endif // QT_CONFIG(tooltip)
        self.actionCrear.setText(QCoreApplication.translate("main", u"Crear", None))
        self.actionAbrir.setText(QCoreApplication.translate("main", u"Abrir", None))
        self.actionCreditos.setText(QCoreApplication.translate("main", u"Cr\u00e9ditos", None))
        self.actionAyuda.setText(QCoreApplication.translate("main", u"Ayuda", None))
        self.actionActualidad.setText(QCoreApplication.translate("main", u"Actualidad", None))
        self.planificarTarea.setText(QCoreApplication.translate("main", u" Planificar", None))
        self.verEventos.setText(QCoreApplication.translate("main", u" Eventos planficados", None))
        self.priorizarCategorias.setText(QCoreApplication.translate("main", u" Gestionar categor\u00edas", None))
        self.menuSitios.setTitle(QCoreApplication.translate("main", u"Turismo", None))
        self.menuNotas.setTitle(QCoreApplication.translate("main", u"Notas", None))
        self.menuM_s_informaci_n.setTitle(QCoreApplication.translate("main", u"M\u00e1s informaci\u00f3n", None))
    # retranslateUi


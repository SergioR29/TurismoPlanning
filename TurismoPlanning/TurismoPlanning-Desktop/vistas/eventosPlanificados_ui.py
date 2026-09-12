# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'eventosPlanificados.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QScrollArea,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

class Ui_eventos(object):
    def setupUi(self, eventos):
        if not eventos.objectName():
            eventos.setObjectName(u"eventos")
        eventos.setWindowModality(Qt.WindowModality.WindowModal)
        eventos.resize(800, 600)
        eventos.setMaximumSize(QSize(800, 600))
        icon = QIcon()
        icon.addFile(u"../recursos/iconos/eventos.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        eventos.setWindowIcon(icon)
        eventos.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(27, 27, 27);")
        self.actionHTML = QAction(eventos)
        self.actionHTML.setObjectName(u"actionHTML")
        icon1 = QIcon()
        icon1.addFile(u"../recursos/iconos/html.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionHTML.setIcon(icon1)
        font = QFont()
        font.setPointSize(10)
        self.actionHTML.setFont(font)
        self.actionPDF = QAction(eventos)
        self.actionPDF.setObjectName(u"actionPDF")
        icon2 = QIcon()
        icon2.addFile(u"../recursos/iconos/pdf.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionPDF.setIcon(icon2)
        self.actionPDF.setFont(font)
        self.actionAyuda = QAction(eventos)
        self.actionAyuda.setObjectName(u"actionAyuda")
        icon3 = QIcon()
        icon3.addFile(u"../recursos/iconos/ayuda.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionAyuda.setIcon(icon3)
        self.actionAyuda.setFont(font)
        self.centralwidget = QWidget(eventos)
        self.centralwidget.setObjectName(u"centralwidget")
        self.formLayoutWidget = QWidget(self.centralwidget)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(30, 29, 321, 31))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.categoriaLabel = QLabel(self.formLayoutWidget)
        self.categoriaLabel.setObjectName(u"categoriaLabel")
        self.categoriaLabel.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.categoriaLabel)

        self.categoriaComboBox = QComboBox(self.formLayoutWidget)
        self.categoriaComboBox.setObjectName(u"categoriaComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categoriaComboBox.sizePolicy().hasHeightForWidth())
        self.categoriaComboBox.setSizePolicy(sizePolicy)
        self.categoriaComboBox.setStyleSheet(u"color:white; border-top: none;\n"
"    border-left: none;\n"
"    border-right: none;\n"
"    border-bottom: 2px solid blue;\n"
"background-color: rgb(40, 40, 40);\n"
"padding-left:5px;")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.categoriaComboBox)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 100, 731, 21))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(99, 150, 591, 391))
        self.scrollArea.setStyleSheet(u"QScrollArea {border:none;}\n"
"\n"
"/* Estilo general para la barra de scroll vertical DENTRO de un QScrollArea */\n"
"            QScrollArea QScrollBar:vertical {\n"
"                border: none; /* Sin borde */\n"
"                background: #2a2a2a; /* Color de fondo del riel (gris muy oscuro) */\n"
"                width: 12px; /* Ancho de la barra vertical */\n"
"                /* margin: 0px 0 0px 0; /* Sin margen si no hay botones de flecha visibles */\n"
"            }\n"
"\n"
"            /* Estilo para el \"handle\" (la parte que arrastras) de la barra vertical */\n"
"            QScrollArea QScrollBar::handle:vertical {\n"
"                background: #606060; /* Color del handle (gris medio) */\n"
"                min-height: 20px; /* Altura m\u00ednima del handle */\n"
"                border-radius: 6px; /* Esquinas redondeadas para el handle */\n"
"                border: none; /* Sin borde en el handle */\n"
"            }\n"
"\n"
"            /* Estilo al pasar el rat\u00f3n por el handle "
                        "*/\n"
"            QScrollArea QScrollBar::handle:vertical:hover {\n"
"                background: #828282; /* Color del handle al pasar el rat\u00f3n (gris m\u00e1s claro) */\n"
"            }\n"
"\n"
"            /* Estilo cuando se pulsa el handle */\n"
"            QScrollArea QScrollBar::handle:vertical:pressed {\n"
"                background: #939393; /* Color del handle al pulsar (gris a\u00fan m\u00e1s claro) */\n"
"            }\n"
"\n"
"            /* Estilo para las \u00e1reas \"page\" (el riel entre el handle y las flechas) */\n"
"            /* Normalmente no necesitan un color de fondo propio si QScrollBar:vertical ya lo tiene */\n"
"            QScrollArea QScrollBar::add-page:vertical, QScrollArea QScrollBar::sub-page:vertical {\n"
"                background: none;\n"
"            }\n"
"\n"
"            /* Estilo para los botones de flecha (si est\u00e1n visibles) */\n"
"            /* Si no quieres botones de flecha, puedes ocultarlos o no definirlos */\n"
"            QScrollArea QScrollBar"
                        "::add-line:vertical, QScrollArea QScrollBar::sub-line:vertical {\n"
"                border: none;\n"
"                background: #3a3a3a; /* Color de fondo de los botones (gris oscuro) */\n"
"                height: 0px; /* Ocultar botones de flecha estableciendo altura a 0 */\n"
"                subcontrol-position: top; /* Posici\u00f3n de sub-line (irrelevante si height es 0) */\n"
"                subcontrol-origin: margin;\n"
"            }\n"
"             QScrollArea QScrollBar::sub-line:vertical { subcontrol-position: top; }\n"
"             QScrollArea QScrollBar::add-line:vertical { subcontrol-position: bottom; }\n"
"\n"
"\n"
"            /* Estilo para las flechas DENTRO de los botones (irrelevante si los botones est\u00e1n ocultos) */\n"
"             QScrollArea QScrollBar::up-arrow:vertical, QScrollArea QScrollBar::down-arrow:vertical {\n"
"                 width: 0px; /* Ocultar flechas estableciendo ancho/alto a 0 */\n"
"                 height: 0px;\n"
"                 background: none;\n"
""
                        "             }\n"
"\n"
"            /* Puedes a\u00f1adir estilos similares para QScrollBar:horizontal */\n"
"            \n"
"            QScrollArea QScrollBar:horizontal {\n"
"                border: none;\n"
"                background: #2a2a2a;\n"
"                height: 12px;\n"
"            }\n"
"            QScrollArea QScrollBar::handle:horizontal {\n"
"                background: #606060;\n"
"                min-width: 20px;\n"
"                border-radius: 6px;\n"
"                border: none;\n"
"            }\n"
"            QScrollArea QScrollBar::handle:horizontal:hover { background: #828282; }\n"
"            QScrollArea QScrollBar::handle:horizontal:pressed { background: #939393; }\n"
"            QScrollArea QScrollBar::add-page:horizontal, QScrollArea QScrollBar::sub-page:horizontal { background: none; }\n"
"            QScrollArea QScrollBar::add-line:horizontal, QScrollArea QScrollBar::sub-line:horizontal { border: none; background: #3a3a3a; width: 0px; }\n"
"            QScrollArea QS"
                        "crollBar::left-arrow:horizontal, QScrollArea QScrollBar::right-arrow:horizontal { width: 0px; height: 0px; background: none; }\n"
"            ")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 591, 18))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy1)
        self.scrollAreaWidgetContents.setStyleSheet(u"border:none;")
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.eliminarEvento = QToolButton(self.centralwidget)
        self.eliminarEvento.setObjectName(u"eliminarEvento")
        self.eliminarEvento.setGeometry(QRect(410, 32, 31, 31))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.eliminarEvento.sizePolicy().hasHeightForWidth())
        self.eliminarEvento.setSizePolicy(sizePolicy2)
        self.eliminarEvento.setStyleSheet(u"background-color: rgb(26, 26, 26);border:none;")
        icon4 = QIcon()
        icon4.addFile(u"../recursos/iconos/ic_eliminar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.eliminarEvento.setIcon(icon4)
        self.eliminarEvento.setIconSize(QSize(26, 26))
        self.editarEvento = QToolButton(self.centralwidget)
        self.editarEvento.setObjectName(u"editarEvento")
        self.editarEvento.setGeometry(QRect(370, 30, 31, 31))
        sizePolicy2.setHeightForWidth(self.editarEvento.sizePolicy().hasHeightForWidth())
        self.editarEvento.setSizePolicy(sizePolicy2)
        self.editarEvento.setStyleSheet(u"background-color: rgb(26, 26, 26);border:none;")
        icon5 = QIcon()
        icon5.addFile(u"../recursos/iconos/ic_editar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.editarEvento.setIcon(icon5)
        self.editarEvento.setIconSize(QSize(32, 32))
        self.ayuda = QToolButton(self.centralwidget)
        self.ayuda.setObjectName(u"ayuda")
        self.ayuda.setGeometry(QRect(750, 510, 40, 40))
        sizePolicy2.setHeightForWidth(self.ayuda.sizePolicy().hasHeightForWidth())
        self.ayuda.setSizePolicy(sizePolicy2)
        self.ayuda.setStyleSheet(u"background-color: rgb(26, 26, 26);border:none;")
        self.ayuda.setIcon(icon3)
        self.ayuda.setIconSize(QSize(40, 40))
        eventos.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(eventos)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menubar.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(44, 44, 44);")
        self.menuExportar = QMenu(self.menubar)
        self.menuExportar.setObjectName(u"menuExportar")
        self.menuExportar.setStyleSheet(u"color:white;border:2px solid black;")
        self.menuM_s_informaci_n = QMenu(self.menubar)
        self.menuM_s_informaci_n.setObjectName(u"menuM_s_informaci_n")
        self.menuM_s_informaci_n.setFont(font)
        self.menuM_s_informaci_n.setStyleSheet(u"color:white;border: 2px solid black")
        eventos.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuExportar.menuAction())
        self.menubar.addAction(self.menuM_s_informaci_n.menuAction())
        self.menuExportar.addAction(self.actionHTML)
        self.menuExportar.addAction(self.actionPDF)
        self.menuM_s_informaci_n.addAction(self.actionAyuda)

        self.retranslateUi(eventos)

        QMetaObject.connectSlotsByName(eventos)
    # setupUi

    def retranslateUi(self, eventos):
        eventos.setWindowTitle(QCoreApplication.translate("eventos", u"Eventos planificados", None))
        self.actionHTML.setText(QCoreApplication.translate("eventos", u"HTML", None))
        self.actionPDF.setText(QCoreApplication.translate("eventos", u"PDF", None))
        self.actionAyuda.setText(QCoreApplication.translate("eventos", u"Ayuda", None))
        self.categoriaLabel.setText(QCoreApplication.translate("eventos", u"Categor\u00eda", None))
        self.label.setText(QCoreApplication.translate("eventos", u"EVENTOS Y TAREAS", None))
        self.eliminarEvento.setText(QCoreApplication.translate("eventos", u"...", None))
        self.editarEvento.setText(QCoreApplication.translate("eventos", u"...", None))
        self.ayuda.setText(QCoreApplication.translate("eventos", u"...", None))
        self.menuExportar.setTitle(QCoreApplication.translate("eventos", u"Exportar", None))
        self.menuM_s_informaci_n.setTitle(QCoreApplication.translate("eventos", u"M\u00e1s informaci\u00f3n", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'verSitios.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QWidget)

class Ui_manejarSitios(object):
    def setupUi(self, manejarSitios):
        if not manejarSitios.objectName():
            manejarSitios.setObjectName(u"manejarSitios")
        manejarSitios.resize(849, 706)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(manejarSitios.sizePolicy().hasHeightForWidth())
        manejarSitios.setSizePolicy(sizePolicy)
        manejarSitios.setMaximumSize(QSize(849, 706))
        icon = QIcon()
        icon.addFile(u"../recursos/iconos/ic_SitiosVentana.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        manejarSitios.setWindowIcon(icon)
        manejarSitios.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.actionHTML = QAction(manejarSitios)
        self.actionHTML.setObjectName(u"actionHTML")
        icon1 = QIcon()
        icon1.addFile(u"../recursos/iconos/html.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionHTML.setIcon(icon1)
        self.actionPDF = QAction(manejarSitios)
        self.actionPDF.setObjectName(u"actionPDF")
        icon2 = QIcon()
        icon2.addFile(u"../recursos/iconos/pdf.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionPDF.setIcon(icon2)
        self.centralwidget = QWidget(manejarSitios)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 849, 671))
        self.frame.setStyleSheet(u"background-color: rgb(26, 26, 26);\n"
"color: rgb(255, 255, 255);\n"
"border:0px")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayoutWidget = QWidget(self.frame)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(30, 40, 271, 71))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(13)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.ciudadLabel = QLabel(self.formLayoutWidget)
        self.ciudadLabel.setObjectName(u"ciudadLabel")
        font = QFont()
        font.setPointSize(10)
        self.ciudadLabel.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.ciudadLabel)

        self.ciudadComboBox = QComboBox(self.formLayoutWidget)
        self.ciudadComboBox.setObjectName(u"ciudadComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ciudadComboBox.sizePolicy().hasHeightForWidth())
        self.ciudadComboBox.setSizePolicy(sizePolicy1)
        self.ciudadComboBox.setFont(font)
        self.ciudadComboBox.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(45, 45, 45);\n"
"border-bottom: 2px solid rgb(0, 170, 255);\n"
"border-left:none;\n"
"border-right:none;\n"
"border-top:none;\n"
"padding-left:5px;\n"
"padding-right:5px;")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.ciudadComboBox)

        self.sitioLabel = QLabel(self.formLayoutWidget)
        self.sitioLabel.setObjectName(u"sitioLabel")
        self.sitioLabel.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.sitioLabel)

        self.sitioComboBox = QComboBox(self.formLayoutWidget)
        self.sitioComboBox.setObjectName(u"sitioComboBox")
        sizePolicy1.setHeightForWidth(self.sitioComboBox.sizePolicy().hasHeightForWidth())
        self.sitioComboBox.setSizePolicy(sizePolicy1)
        self.sitioComboBox.setFont(font)
        self.sitioComboBox.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-bottom: 2px solid rgb(170, 85, 255);\n"
"border-left:none;\n"
"border-right:none;\n"
"border-top:none;\n"
"background-color: rgb(45, 45, 45);\n"
"padding-left:5px;\n"
"padding-right:5px;")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.sitioComboBox)

        self.frame_sitios = QFrame(self.frame)
        self.frame_sitios.setObjectName(u"frame_sitios")
        self.frame_sitios.setGeometry(QRect(30, 140, 791, 561))
        self.frame_sitios.setStyleSheet(u"background-color: rgb(26, 26, 26);\n"
"color: rgb(255, 255, 255);\n"
"border:0px;\n"
"border-radius:15px")
        self.frame_sitios.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_sitios.setFrameShadow(QFrame.Shadow.Raised)
        self.img_Sitio = QLabel(self.frame_sitios)
        self.img_Sitio.setObjectName(u"img_Sitio")
        self.img_Sitio.setGeometry(QRect(500, 20, 241, 181))
        self.img_Sitio.setStyleSheet(u"background-color: rgb(53, 53, 53);\n"
"border: 5px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 145, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 10px")
        self.frame_3 = QFrame(self.frame_sitios)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(30, 300, 731, 211))
        self.frame_3.setStyleSheet(u"border-radius:15px;\n"
"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 145, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border:none;")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.desc_Sitio = QPlainTextEdit(self.frame_3)
        self.desc_Sitio.setObjectName(u"desc_Sitio")
        self.desc_Sitio.setGeometry(QRect(10, 10, 711, 191))
        self.desc_Sitio.setFont(font)
        self.desc_Sitio.setStyleSheet(u"background-color: rgb(54, 54, 54);color:white;border-radius:0px;border:none;")
        self.desc_Sitio.setReadOnly(True)
        self.label_2 = QLabel(self.frame_sitios)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(40, 259, 711, 41))
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(True)
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"color: white;border:none;")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nombreSitio = QLabel(self.frame_sitios)
        self.nombreSitio.setObjectName(u"nombreSitio")
        self.nombreSitio.setGeometry(QRect(500, 210, 241, 20))
        self.nombreSitio.setFont(font)
        self.nombreSitio.setStyleSheet(u"color:white;border:none;")
        self.nombreSitio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_Ciudad = QLabel(self.frame_sitios)
        self.img_Ciudad.setObjectName(u"img_Ciudad")
        self.img_Ciudad.setGeometry(QRect(50, 20, 241, 181))
        self.img_Ciudad.setStyleSheet(u"background-color: rgb(53, 53, 53);\n"
"border: 5px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 145, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 10px")
        self.nombreCiudad = QLabel(self.frame_sitios)
        self.nombreCiudad.setObjectName(u"nombreCiudad")
        self.nombreCiudad.setGeometry(QRect(50, 200, 241, 31))
        sizePolicy.setHeightForWidth(self.nombreCiudad.sizePolicy().hasHeightForWidth())
        self.nombreCiudad.setSizePolicy(sizePolicy)
        self.nombreCiudad.setFont(font)
        self.nombreCiudad.setStyleSheet(u"color:white;border:none;")
        self.nombreCiudad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.aviso_ciudadNoSeleccionada = QLabel(self.frame)
        self.aviso_ciudadNoSeleccionada.setObjectName(u"aviso_ciudadNoSeleccionada")
        self.aviso_ciudadNoSeleccionada.setGeometry(QRect(320, 45, 211, 21))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.aviso_ciudadNoSeleccionada.sizePolicy().hasHeightForWidth())
        self.aviso_ciudadNoSeleccionada.setSizePolicy(sizePolicy2)
        font2 = QFont()
        font2.setBold(True)
        self.aviso_ciudadNoSeleccionada.setFont(font2)
        self.aviso_ciudadNoSeleccionada.setStyleSheet(u"color: rgb(255, 255, 0);")
        self.aviso_ciudadNoSeleccionada.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.ubiClima_sitio = QPushButton(self.frame)
        self.ubiClima_sitio.setObjectName(u"ubiClima_sitio")
        self.ubiClima_sitio.setGeometry(QRect(660, 80, 161, 31))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(True)
        self.ubiClima_sitio.setFont(font3)
        self.ubiClima_sitio.setStyleSheet(u"color:black;\n"
"background-color: qlineargradient(spread:pad, x1:0.225, y1:0.206, x2:0.643, y2:0.589, stop:0.21978 rgba(0, 255, 68, 255), stop:1 rgba(243, 255, 0, 255));\n"
"border-radius:15px")
        icon3 = QIcon()
        icon3.addFile(u"../recursos/iconos/UbiClima.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ubiClima_sitio.setIcon(icon3)
        self.ubiClima_sitio.setIconSize(QSize(32, 24))
        self.aviso_sitio = QLabel(self.frame)
        self.aviso_sitio.setObjectName(u"aviso_sitio")
        self.aviso_sitio.setGeometry(QRect(320, 90, 321, 21))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.aviso_sitio.sizePolicy().hasHeightForWidth())
        self.aviso_sitio.setSizePolicy(sizePolicy3)
        self.aviso_sitio.setFont(font2)
        self.aviso_sitio.setStyleSheet(u"color: rgb(255, 255, 0);")
        self.aviso_sitio.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.planificar_visita = QPushButton(self.frame)
        self.planificar_visita.setObjectName(u"planificar_visita")
        self.planificar_visita.setGeometry(QRect(660, 35, 161, 31))
        self.planificar_visita.setFont(font3)
        self.planificar_visita.setStyleSheet(u"border-radius:15px;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 87, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:black;")
        icon4 = QIcon()
        icon4.addFile(u"../recursos/iconos/visita_turismo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.planificar_visita.setIcon(icon4)
        self.planificar_visita.setIconSize(QSize(30, 30))
        manejarSitios.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(manejarSitios)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 849, 33))
        self.menubar.setFont(font)
        self.menubar.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(45, 45, 45);")
        self.menuExportar = QMenu(self.menubar)
        self.menuExportar.setObjectName(u"menuExportar")
        self.menuExportar.setStyleSheet(u"color:white;border:2px solid black;")
        manejarSitios.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuExportar.menuAction())
        self.menuExportar.addAction(self.actionHTML)
        self.menuExportar.addAction(self.actionPDF)

        self.retranslateUi(manejarSitios)

        QMetaObject.connectSlotsByName(manejarSitios)
    # setupUi

    def retranslateUi(self, manejarSitios):
        manejarSitios.setWindowTitle(QCoreApplication.translate("manejarSitios", u"Sitios", None))
        self.actionHTML.setText(QCoreApplication.translate("manejarSitios", u"HTML", None))
        self.actionPDF.setText(QCoreApplication.translate("manejarSitios", u"PDF", None))
        self.ciudadLabel.setText(QCoreApplication.translate("manejarSitios", u"Ciudad", None))
        self.sitioLabel.setText(QCoreApplication.translate("manejarSitios", u"Sitio", None))
        self.img_Sitio.setText("")
        self.desc_Sitio.setPlainText("")
        self.label_2.setText(QCoreApplication.translate("manejarSitios", u"DESCRIPCI\u00d3N", None))
        self.nombreSitio.setText(QCoreApplication.translate("manejarSitios", u"Nombre del sitio seleccionado", None))
        self.img_Ciudad.setText("")
        self.nombreCiudad.setText(QCoreApplication.translate("manejarSitios", u"Nombre de la ciudad seleccionada", None))
        self.aviso_ciudadNoSeleccionada.setText(QCoreApplication.translate("manejarSitios", u"SELECCIONE UNA CIUDAD", None))
        self.ubiClima_sitio.setText(QCoreApplication.translate("manejarSitios", u" Ubicaci\u00f3n y Clima", None))
        self.aviso_sitio.setText(QCoreApplication.translate("manejarSitios", u"SELECCIONE UN SITIO", None))
        self.planificar_visita.setText(QCoreApplication.translate("manejarSitios", u"Planificar Visita", None))
        self.menuExportar.setTitle(QCoreApplication.translate("manejarSitios", u"Exportar", None))
    # retranslateUi


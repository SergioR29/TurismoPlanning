# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'actualidad.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget)

class Ui_actualidad(object):
    def setupUi(self, actualidad):
        if not actualidad.objectName():
            actualidad.setObjectName(u"actualidad")
        actualidad.setWindowModality(Qt.WindowModality.WindowModal)
        actualidad.resize(815, 533)
        actualidad.setMaximumSize(QSize(815, 533))
        icon = QIcon()
        icon.addFile(u"../recursos/iconos/ic_menu_actualidad.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        actualidad.setWindowIcon(icon)
        actualidad.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(25, 25, 25);")
        self.label = QLabel(actualidad)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(11, 0, 801, 36))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color:white;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mapaUbiCiudad = QWebEngineView(actualidad)
        self.mapaUbiCiudad.setObjectName(u"mapaUbiCiudad")
        self.mapaUbiCiudad.setGeometry(QRect(10, 40, 801, 451))
        self.mapaUbiCiudad.setStyleSheet(u"color:white;")
        self.mapaUbiCiudad.setUrl(QUrl(u"about:blank"))
        self.ok = QPushButton(actualidad)
        self.ok.setObjectName(u"ok")
        self.ok.setGeometry(QRect(370, 500, 75, 24))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.ok.setFont(font1)
        self.ok.setStyleSheet(u"color: black;\n"
"background-color: rgb(0, 170, 255);")

        self.retranslateUi(actualidad)
        self.ok.clicked.connect(actualidad.hide)

        QMetaObject.connectSlotsByName(actualidad)
    # setupUi

    def retranslateUi(self, actualidad):
        actualidad.setWindowTitle(QCoreApplication.translate("actualidad", u"Actualidad", None))
        self.label.setText(QCoreApplication.translate("actualidad", u"UBICACI\u00d3N", None))
        self.ok.setText(QCoreApplication.translate("actualidad", u"OK", None))
    # retranslateUi


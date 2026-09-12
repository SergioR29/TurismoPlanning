# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cambiarFormatoTexto.ui'
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
from PySide6.QtWidgets import (QApplication, QFontComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QWidget)

class Ui_formato(object):
    def setupUi(self, formato):
        if not formato.objectName():
            formato.setObjectName(u"formato")
        formato.setWindowModality(Qt.WindowModality.WindowModal)
        formato.resize(296, 133)
        formato.setMaximumSize(QSize(296, 133))
        icon = QIcon()
        icon.addFile(u"../recursos/iconos/formato-de-texto.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        formato.setWindowIcon(icon)
        formato.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(30, 30, 30);")
        self.verticalLayoutWidget = QWidget(formato)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 30, 251, 31))
        self.horizontalLayout = QHBoxLayout(self.verticalLayoutWidget)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.formatoLabel = QLabel(self.verticalLayoutWidget)
        self.formatoLabel.setObjectName(u"formatoLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.formatoLabel.sizePolicy().hasHeightForWidth())
        self.formatoLabel.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        self.formatoLabel.setFont(font)
        self.formatoLabel.setStyleSheet(u"color:white;")

        self.horizontalLayout.addWidget(self.formatoLabel)

        self.formatoComboBox = QFontComboBox(self.verticalLayoutWidget)
        self.formatoComboBox.setObjectName(u"formatoComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.formatoComboBox.sizePolicy().hasHeightForWidth())
        self.formatoComboBox.setSizePolicy(sizePolicy1)
        self.formatoComboBox.setFont(font)
        self.formatoComboBox.setStyleSheet(u"color:white;\n"
"background-color: rgb(45, 45, 45);\n"
"border:none;\n"
"border-bottom:2px solid blue;")
        font1 = QFont()
        self.formatoComboBox.setCurrentFont(font1)

        self.horizontalLayout.addWidget(self.formatoComboBox)

        self.ok = QPushButton(formato)
        self.ok.setObjectName(u"ok")
        self.ok.setGeometry(QRect(110, 100, 75, 24))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.ok.setFont(font2)
        self.ok.setStyleSheet(u"color:black;\n"
"background-color: rgb(0, 170, 255)")

        self.retranslateUi(formato)
        self.ok.clicked.connect(formato.close)

        QMetaObject.connectSlotsByName(formato)
    # setupUi

    def retranslateUi(self, formato):
        formato.setWindowTitle(QCoreApplication.translate("formato", u"Formato", None))
        self.formatoLabel.setText(QCoreApplication.translate("formato", u"Formato", None))
        self.ok.setText(QCoreApplication.translate("formato", u"OK", None))
    # retranslateUi


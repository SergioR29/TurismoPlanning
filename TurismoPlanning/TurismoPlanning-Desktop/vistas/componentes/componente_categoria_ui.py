# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'componente_categoria.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QSizePolicy, QWidget)

class Ui_componente_categoria(object):
    def setupUi(self, componente_categoria):
        if not componente_categoria.objectName():
            componente_categoria.setObjectName(u"componente_categoria")
        componente_categoria.resize(251, 40)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(componente_categoria.sizePolicy().hasHeightForWidth())
        componente_categoria.setSizePolicy(sizePolicy)
        componente_categoria.setMaximumSize(QSize(16777215, 40))
        componente_categoria.setStyleSheet(u"border:none;")
        self.horizontalLayout = QHBoxLayout(componente_categoria)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.color = QLabel(componente_categoria)
        self.color.setObjectName(u"color")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.color.sizePolicy().hasHeightForWidth())
        self.color.setSizePolicy(sizePolicy1)
        self.color.setMinimumSize(QSize(40, 40))
        self.color.setMaximumSize(QSize(40, 40))
        font = QFont()
        font.setPointSize(9)
        self.color.setFont(font)
        self.color.setStyleSheet(u"background-color:red;border:5px solid black;")

        self.horizontalLayout.addWidget(self.color)

        self.prioridad = QLabel(componente_categoria)
        self.prioridad.setObjectName(u"prioridad")
        sizePolicy1.setHeightForWidth(self.prioridad.sizePolicy().hasHeightForWidth())
        self.prioridad.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(True)
        self.prioridad.setFont(font1)
        self.prioridad.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.prioridad)

        self.nombre = QLabel(componente_categoria)
        self.nombre.setObjectName(u"nombre")
        sizePolicy.setHeightForWidth(self.nombre.sizePolicy().hasHeightForWidth())
        self.nombre.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(13)
        font2.setBold(False)
        self.nombre.setFont(font2)
        self.nombre.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.nombre)


        self.retranslateUi(componente_categoria)

        QMetaObject.connectSlotsByName(componente_categoria)
    # setupUi

    def retranslateUi(self, componente_categoria):
        componente_categoria.setWindowTitle(QCoreApplication.translate("componente_categoria", u"Form", None))
        self.color.setText("")
        self.prioridad.setText(QCoreApplication.translate("componente_categoria", u"1\u00ba)", None))
        self.nombre.setText(QCoreApplication.translate("componente_categoria", u"Desarrollo memoria", None))
    # retranslateUi


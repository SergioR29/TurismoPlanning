# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'componente_tarea.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_componente_Tareas(object):
    def setupUi(self, componente_Tareas):
        if not componente_Tareas.objectName():
            componente_Tareas.setObjectName(u"componente_Tareas")
        componente_Tareas.resize(400, 55)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(componente_Tareas.sizePolicy().hasHeightForWidth())
        componente_Tareas.setSizePolicy(sizePolicy)
        componente_Tareas.setMaximumSize(QSize(16777215, 55))
        self.horizontalLayout = QHBoxLayout(componente_Tareas)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.evento_tarea = QPushButton(componente_Tareas)
        self.evento_tarea.setObjectName(u"evento_tarea")
        sizePolicy.setHeightForWidth(self.evento_tarea.sizePolicy().hasHeightForWidth())
        self.evento_tarea.setSizePolicy(sizePolicy)
        self.evento_tarea.setMaximumSize(QSize(52, 52))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.evento_tarea.setFont(font)
        self.evento_tarea.setStyleSheet(u"color:white;text-align:left;border-radius:5px;background-color:darkred;\n"
"padding-left:5px;border:none;")
        icon = QIcon()
        icon.addFile(u"../../recursos/iconos/ic_planificar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.evento_tarea.setIcon(icon)
        self.evento_tarea.setIconSize(QSize(44, 44))

        self.horizontalLayout.addWidget(self.evento_tarea)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.titulo = QLabel(componente_Tareas)
        self.titulo.setObjectName(u"titulo")
        sizePolicy.setHeightForWidth(self.titulo.sizePolicy().hasHeightForWidth())
        self.titulo.setSizePolicy(sizePolicy)
        self.titulo.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.titulo.setFont(font1)
        self.titulo.setStyleSheet(u"color:white;")

        self.verticalLayout.addWidget(self.titulo)

        self.plazo = QLabel(componente_Tareas)
        self.plazo.setObjectName(u"plazo")
        sizePolicy.setHeightForWidth(self.plazo.sizePolicy().hasHeightForWidth())
        self.plazo.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.plazo.setFont(font2)
        self.plazo.setStyleSheet(u"color:white;")

        self.verticalLayout.addWidget(self.plazo)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(componente_Tareas)

        self.evento_tarea.setDefault(False)


        QMetaObject.connectSlotsByName(componente_Tareas)
    # setupUi

    def retranslateUi(self, componente_Tareas):
        componente_Tareas.setWindowTitle(QCoreApplication.translate("componente_Tareas", u"Form", None))
        self.evento_tarea.setText("")
        self.titulo.setText(QCoreApplication.translate("componente_Tareas", u"T\u00edtulo de la tarea o evento", None))
        self.plazo.setText(QCoreApplication.translate("componente_Tareas", u"29/11/2025 hasta el 29/12/2025", None))
    # retranslateUi


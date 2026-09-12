# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'crearCategoria.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QFormLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpinBox,
    QToolButton, QWidget)

class Ui_crearCategoria(object):
    def setupUi(self, crearCategoria):
        if not crearCategoria.objectName():
            crearCategoria.setObjectName(u"crearCategoria")
        crearCategoria.setWindowModality(Qt.WindowModality.WindowModal)
        crearCategoria.resize(399, 183)
        crearCategoria.setMinimumSize(QSize(0, 0))
        crearCategoria.setMaximumSize(QSize(399, 183))
        icon = QIcon()
        icon.addFile(u"../recursos/iconos/categorias.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        crearCategoria.setWindowIcon(icon)
        crearCategoria.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(21, 21, 21);")
        self.formLayoutWidget = QWidget(crearCategoria)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(19, 20, 361, 59))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(12)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.nombreLabel = QLabel(self.formLayoutWidget)
        self.nombreLabel.setObjectName(u"nombreLabel")
        font = QFont()
        font.setPointSize(10)
        self.nombreLabel.setFont(font)
        self.nombreLabel.setStyleSheet(u"color:white;")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.nombreLabel)

        self.nombreLineEdit = QLineEdit(self.formLayoutWidget)
        self.nombreLineEdit.setObjectName(u"nombreLineEdit")
        font1 = QFont()
        font1.setBold(False)
        self.nombreLineEdit.setFont(font1)
        self.nombreLineEdit.setStyleSheet(u"color:white;\n"
"background-color: rgb(30, 30, 30);\n"
"    border-top: none;\n"
"    border-left: none;\n"
"    border-right: none;\n"
"    border-bottom: 2px solid blue;\n"
"\n"
"padding-left:5px;\n"
"")
        self.nombreLineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        self.nombreLineEdit.setCursorPosition(0)
        self.nombreLineEdit.setClearButtonEnabled(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.nombreLineEdit)

        self.prioridadLabel = QLabel(self.formLayoutWidget)
        self.prioridadLabel.setObjectName(u"prioridadLabel")
        self.prioridadLabel.setFont(font)
        self.prioridadLabel.setStyleSheet(u"color:white;")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.prioridadLabel)

        self.prioridadSpinBox = QSpinBox(self.formLayoutWidget)
        self.prioridadSpinBox.setObjectName(u"prioridadSpinBox")
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(True)
        self.prioridadSpinBox.setFont(font2)
        self.prioridadSpinBox.setStyleSheet(u"color:white;\n"
"background-color: rgb(30, 30, 30);\n"
"    border-top: none;\n"
"    border-left: none;\n"
"    border-right: none;\n"
"    border-bottom: 2px solid blue;")
        self.prioridadSpinBox.setWrapping(False)
        self.prioridadSpinBox.setFrame(True)
        self.prioridadSpinBox.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.prioridadSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.prioridadSpinBox.setAccelerated(False)
        self.prioridadSpinBox.setProperty(u"showGroupSeparator", False)
        self.prioridadSpinBox.setMinimum(1)
        self.prioridadSpinBox.setMaximum(999999999)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.prioridadSpinBox)

        self.cerrar = QPushButton(crearCategoria)
        self.cerrar.setObjectName(u"cerrar")
        self.cerrar.setGeometry(QRect(80, 145, 91, 31))
        font3 = QFont()
        font3.setBold(True)
        self.cerrar.setFont(font3)
        self.cerrar.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"background-color: rgb(0, 170, 255);")
        icon1 = QIcon()
        icon1.addFile(u"../recursos/iconos/cerrar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cerrar.setIcon(icon1)
        self.cerrar.setIconSize(QSize(20, 20))
        self.guardarCategoria = QPushButton(crearCategoria)
        self.guardarCategoria.setObjectName(u"guardarCategoria")
        self.guardarCategoria.setGeometry(QRect(230, 145, 91, 31))
        self.guardarCategoria.setFont(font3)
        self.guardarCategoria.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"background-color: rgb(0, 170, 255);")
        icon2 = QIcon()
        icon2.addFile(u"../recursos/iconos/ic_guardar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.guardarCategoria.setIcon(icon2)
        self.color = QToolButton(crearCategoria)
        self.color.setObjectName(u"color")
        self.color.setGeometry(QRect(75, 92, 31, 31))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color.sizePolicy().hasHeightForWidth())
        self.color.setSizePolicy(sizePolicy)
        self.color.setStyleSheet(u"background-color: rgb(21, 21, 21);border:none;")
        icon3 = QIcon()
        icon3.addFile(u"../recursos/iconos/ic_selectorColor.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.color.setIcon(icon3)
        self.color.setIconSize(QSize(26, 26))
        self.label = QLabel(crearCategoria)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 92, 51, 31))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        self.label.setFont(font4)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.retranslateUi(crearCategoria)
        self.cerrar.clicked.connect(crearCategoria.hide)

        QMetaObject.connectSlotsByName(crearCategoria)
    # setupUi

    def retranslateUi(self, crearCategoria):
        crearCategoria.setWindowTitle(QCoreApplication.translate("crearCategoria", u"Crear categor\u00eda", None))
        self.nombreLabel.setText(QCoreApplication.translate("crearCategoria", u"Nombre", None))
        self.prioridadLabel.setText(QCoreApplication.translate("crearCategoria", u"Prioridad", None))
        self.cerrar.setText(QCoreApplication.translate("crearCategoria", u" Cerrar", None))
        self.guardarCategoria.setText(QCoreApplication.translate("crearCategoria", u"  Guardar", None))
        self.color.setText(QCoreApplication.translate("crearCategoria", u"...", None))
        self.label.setText(QCoreApplication.translate("crearCategoria", u"Color", None))
    # retranslateUi


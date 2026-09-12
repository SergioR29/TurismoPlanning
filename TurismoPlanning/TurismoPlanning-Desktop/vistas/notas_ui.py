# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'notas.ui'
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QTextEdit, QWidget)

class Ui_notas(object):
    def setupUi(self, notas):
        if not notas.objectName():
            notas.setObjectName(u"notas")
        notas.resize(799, 600)
        notas.setMaximumSize(QSize(799, 600))
        icon = QIcon()
        icon.addFile(u"../recursos/iconos/notas.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        notas.setWindowIcon(icon)
        notas.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(27, 27, 27);")
        self.actionFormato_de_texto = QAction(notas)
        self.actionFormato_de_texto.setObjectName(u"actionFormato_de_texto")
        icon1 = QIcon()
        icon1.addFile(u"../recursos/iconos/formato_texto.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionFormato_de_texto.setIcon(icon1)
        self.actionGuardar = QAction(notas)
        self.actionGuardar.setObjectName(u"actionGuardar")
        icon2 = QIcon()
        icon2.addFile(u"../recursos/iconos/ic_guardar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionGuardar.setIcon(icon2)
        self.actionGuardar_como = QAction(notas)
        self.actionGuardar_como.setObjectName(u"actionGuardar_como")
        self.actionGuardar_como.setIcon(icon2)
        self.actionHTML = QAction(notas)
        self.actionHTML.setObjectName(u"actionHTML")
        icon3 = QIcon()
        icon3.addFile(u"../recursos/iconos/html.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionHTML.setIcon(icon3)
        self.actionPDF = QAction(notas)
        self.actionPDF.setObjectName(u"actionPDF")
        icon4 = QIcon()
        icon4.addFile(u"../recursos/iconos/pdf.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionPDF.setIcon(icon4)
        self.actionAyuda = QAction(notas)
        self.actionAyuda.setObjectName(u"actionAyuda")
        icon5 = QIcon()
        icon5.addFile(u"../recursos/iconos/ayuda.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionAyuda.setIcon(icon5)
        self.actionAbrir = QAction(notas)
        self.actionAbrir.setObjectName(u"actionAbrir")
        icon6 = QIcon()
        icon6.addFile(u"../recursos/iconos/abrir-documento.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionAbrir.setIcon(icon6)
        self.actionSalir = QAction(notas)
        self.actionSalir.setObjectName(u"actionSalir")
        self.centralwidget = QWidget(notas)
        self.centralwidget.setObjectName(u"centralwidget")
        self.texto = QTextEdit(self.centralwidget)
        self.texto.setObjectName(u"texto")
        self.texto.setGeometry(QRect(0, 0, 801, 571))
        self.texto.setStyleSheet(u"color:white;border-radius:0px;\n"
"background-color: rgb(53, 53, 53);")
        notas.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(notas)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 799, 33))
        font = QFont()
        font.setPointSize(10)
        self.menubar.setFont(font)
        self.menubar.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(34, 34, 34);\n"
"border-left:none;\n"
"border-right:none;\n"
"border-top:none;\n"
"border-bottom:2px solid blue;")
        self.menuArchivo = QMenu(self.menubar)
        self.menuArchivo.setObjectName(u"menuArchivo")
        self.menuExportar = QMenu(self.menuArchivo)
        self.menuExportar.setObjectName(u"menuExportar")
        icon7 = QIcon()
        icon7.addFile(u"../recursos/iconos/flecha_arriba.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menuExportar.setIcon(icon7)
        self.menuAjustes = QMenu(self.menubar)
        self.menuAjustes.setObjectName(u"menuAjustes")
        notas.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuAjustes.menuAction())
        self.menuArchivo.addAction(self.actionAbrir)
        self.menuArchivo.addAction(self.actionGuardar)
        self.menuArchivo.addAction(self.actionGuardar_como)
        self.menuArchivo.addAction(self.menuExportar.menuAction())
        self.menuArchivo.addAction(self.actionSalir)
        self.menuExportar.addAction(self.actionHTML)
        self.menuExportar.addAction(self.actionPDF)
        self.menuAjustes.addAction(self.actionFormato_de_texto)
        self.menuAjustes.addAction(self.actionAyuda)

        self.retranslateUi(notas)
        self.actionSalir.triggered.connect(notas.hide)

        QMetaObject.connectSlotsByName(notas)
    # setupUi

    def retranslateUi(self, notas):
        notas.setWindowTitle(QCoreApplication.translate("notas", u"Notas", None))
        self.actionFormato_de_texto.setText(QCoreApplication.translate("notas", u"Formato de texto", None))
#if QT_CONFIG(shortcut)
        self.actionFormato_de_texto.setShortcut(QCoreApplication.translate("notas", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.actionGuardar.setText(QCoreApplication.translate("notas", u"Guardar", None))
#if QT_CONFIG(shortcut)
        self.actionGuardar.setShortcut(QCoreApplication.translate("notas", u"Ctrl+G", None))
#endif // QT_CONFIG(shortcut)
        self.actionGuardar_como.setText(QCoreApplication.translate("notas", u"Guardar como", None))
#if QT_CONFIG(shortcut)
        self.actionGuardar_como.setShortcut(QCoreApplication.translate("notas", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.actionHTML.setText(QCoreApplication.translate("notas", u"HTML", None))
#if QT_CONFIG(shortcut)
        self.actionHTML.setShortcut(QCoreApplication.translate("notas", u"Ctrl+H", None))
#endif // QT_CONFIG(shortcut)
        self.actionPDF.setText(QCoreApplication.translate("notas", u"PDF", None))
#if QT_CONFIG(shortcut)
        self.actionPDF.setShortcut(QCoreApplication.translate("notas", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.actionAyuda.setText(QCoreApplication.translate("notas", u"Ayuda", None))
#if QT_CONFIG(shortcut)
        self.actionAyuda.setShortcut(QCoreApplication.translate("notas", u"Alt+Y", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbrir.setText(QCoreApplication.translate("notas", u"Abrir", None))
#if QT_CONFIG(shortcut)
        self.actionAbrir.setShortcut(QCoreApplication.translate("notas", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionSalir.setText(QCoreApplication.translate("notas", u"Salir", None))
#if QT_CONFIG(shortcut)
        self.actionSalir.setShortcut(QCoreApplication.translate("notas", u"Alt+S", None))
#endif // QT_CONFIG(shortcut)
        self.menuArchivo.setTitle(QCoreApplication.translate("notas", u"Archivo", None))
        self.menuExportar.setTitle(QCoreApplication.translate("notas", u"Exportar", None))
        self.menuAjustes.setTitle(QCoreApplication.translate("notas", u"Ajustes", None))
    # retranslateUi


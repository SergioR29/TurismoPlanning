# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gestionarCategorias.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QFormLayout, QHeaderView, QLabel, QScrollArea,
    QSizePolicy, QToolButton, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_categorias(object):
    def setupUi(self, categorias):
        if not categorias.objectName():
            categorias.setObjectName(u"categorias")
        categorias.setWindowModality(Qt.WindowModality.WindowModal)
        categorias.resize(434, 505)
        categorias.setMaximumSize(QSize(434, 505))
        icon = QIcon()
        icon.addFile(u"../recursos/iconos/categorias.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        categorias.setWindowIcon(icon)
        categorias.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(26, 26, 26);")
        self.formLayoutWidget = QWidget(categorias)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(20, 20, 301, 31))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.categoriaLabel = QLabel(self.formLayoutWidget)
        self.categoriaLabel.setObjectName(u"categoriaLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categoriaLabel.sizePolicy().hasHeightForWidth())
        self.categoriaLabel.setSizePolicy(sizePolicy)
        self.categoriaLabel.setStyleSheet(u"color:white;")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.categoriaLabel)

        self.categoriaComboBox = QComboBox(self.formLayoutWidget)
        self.categoriaComboBox.setObjectName(u"categoriaComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.categoriaComboBox.sizePolicy().hasHeightForWidth())
        self.categoriaComboBox.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(10)
        self.categoriaComboBox.setFont(font)
        self.categoriaComboBox.setStyleSheet(u"color:white;\n"
"background-color: rgb(40, 40, 40);\n"
"border-left:none;\n"
"border-right:none;\n"
"border-top:none;\n"
"border-bottom: 2px solid blue;\n"
"padding-left:5px;")
        self.categoriaComboBox.setMaxVisibleItems(999999999)
        self.categoriaComboBox.setIconSize(QSize(16, 16))
        self.categoriaComboBox.setDuplicatesEnabled(False)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.categoriaComboBox)

        self.editarCategoria = QToolButton(categorias)
        self.editarCategoria.setObjectName(u"editarCategoria")
        self.editarCategoria.setGeometry(QRect(350, 15, 31, 31))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.editarCategoria.sizePolicy().hasHeightForWidth())
        self.editarCategoria.setSizePolicy(sizePolicy2)
        self.editarCategoria.setStyleSheet(u"background-color: rgb(26, 26, 26);border:none;")
        icon1 = QIcon()
        icon1.addFile(u"../recursos/iconos/ic_editar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.editarCategoria.setIcon(icon1)
        self.editarCategoria.setIconSize(QSize(32, 32))
        self.eliminarCategoria = QToolButton(categorias)
        self.eliminarCategoria.setObjectName(u"eliminarCategoria")
        self.eliminarCategoria.setGeometry(QRect(390, 17, 31, 31))
        sizePolicy2.setHeightForWidth(self.eliminarCategoria.sizePolicy().hasHeightForWidth())
        self.eliminarCategoria.setSizePolicy(sizePolicy2)
        self.eliminarCategoria.setStyleSheet(u"background-color: rgb(26, 26, 26);border:none;")
        icon2 = QIcon()
        icon2.addFile(u"../recursos/iconos/ic_eliminar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.eliminarCategoria.setIcon(icon2)
        self.eliminarCategoria.setIconSize(QSize(26, 26))
        self.label = QLabel(categorias)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 70, 431, 51))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"color:white;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.exportar = QTreeWidget(categorias)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font2);
        __qtreewidgetitem.setBackground(0, QColor(0, 170, 255));
        __qtreewidgetitem.setForeground(0, brush);
        self.exportar.setHeaderItem(__qtreewidgetitem)
        self.exportar.setObjectName(u"exportar")
        self.exportar.setGeometry(QRect(90, 400, 256, 91))
        self.exportar.setStyleSheet(u"QTreeWidget::item {\n"
"    padding: 5px;\n"
"}")
        self.exportar.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.exportar.setProperty(u"showDropIndicator", True)
        self.exportar.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.exportar.setItemsExpandable(True)
        self.exportar.setExpandsOnDoubleClick(True)
        self.exportar.header().setVisible(True)
        self.exportar.header().setCascadingSectionResizes(False)
        self.exportar.header().setHighlightSections(False)
        self.exportar.header().setProperty(u"showSortIndicator", False)
        self.exportar.header().setStretchLastSection(True)
        self.ayuda = QToolButton(categorias)
        self.ayuda.setObjectName(u"ayuda")
        self.ayuda.setGeometry(QRect(390, 460, 31, 31))
        sizePolicy2.setHeightForWidth(self.ayuda.sizePolicy().hasHeightForWidth())
        self.ayuda.setSizePolicy(sizePolicy2)
        self.ayuda.setStyleSheet(u"background-color: rgb(26, 26, 26);border:none;")
        icon3 = QIcon()
        icon3.addFile(u"../recursos/iconos/ayuda.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ayuda.setIcon(icon3)
        self.ayuda.setIconSize(QSize(32, 32))
        self.scrollArea = QScrollArea(categorias)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(20, 139, 401, 221))
        self.scrollArea.setStyleSheet(u"QScrollArea {\n"
"	color: rgb(255, 255, 255);\n"
"	border:2px solid blue;\n"
"}\n"
"\n"
"/* Estilo general para la barra de scroll vertical DENTRO de un QScrollArea */\n"
"            QScrollArea QScrollBar:vertical {\n"
"                border: none; /* Sin borde */\n"
"                background: #2a2a2a; /* Color de fondo del riel (gris muy oscuro) */\n"
"                width: 12px; /* Ancho de la barra vertical */\n"
"                /* margin: 0px 0 0px 0; /* Sin margen si no hay botones de flecha visibles */\n"
"            }\n"
"\n"
"             /* Estilo para el \"handle\" (la parte que arrastras) de la barra vertical */\n"
"            QScrollArea QScrollBar::handle:vertical {\n"
"                background: #606060; /* Color del handle (gris medio) */\n"
"                min-height: 20px; /* Altura m\u00ednima del handle */\n"
"                border-radius: 6px; /* Esquinas redondeadas para el handle */\n"
"                border: none; /* Sin borde en el handle */\n"
"            }\n"
"\n"
"     "
                        "       /* Estilo al pasar el rat\u00f3n por el handle */\n"
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
"            /* Si no quieres botones de flecha, puedes ocultarlos o n"
                        "o definirlos */\n"
"            QScrollArea QScrollBar::add-line:vertical, QScrollArea QScrollBar::sub-line:vertical {\n"
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
"                 h"
                        "eight: 0px;\n"
"                 background: none;\n"
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
"            QScrollArea QScrollBar::add-line:horizontal, QScrollArea QScrollBar::sub-line:horizontal { border: none; background"
                        ": #3a3a3a; width: 0px; }\n"
"            QScrollArea QScrollBar::left-arrow:horizontal, QScrollArea QScrollBar::right-arrow:horizontal { width: 0px; height: 0px; background: none; }\n"
"            ")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 397, 18))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy3)
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(categorias)

        QMetaObject.connectSlotsByName(categorias)
    # setupUi

    def retranslateUi(self, categorias):
        categorias.setWindowTitle(QCoreApplication.translate("categorias", u"Categor\u00edas", None))
        self.categoriaLabel.setText(QCoreApplication.translate("categorias", u"Categor\u00eda", None))
        self.categoriaComboBox.setPlaceholderText("")
        self.editarCategoria.setText(QCoreApplication.translate("categorias", u"...", None))
        self.eliminarCategoria.setText(QCoreApplication.translate("categorias", u"...", None))
        self.label.setText(QCoreApplication.translate("categorias", u"CATEGOR\u00cdAS ORDENADAS\n"
"POR PRIORIDAD", None))
        ___qtreewidgetitem = self.exportar.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("categorias", u"Exportar a", None));
        self.ayuda.setText(QCoreApplication.translate("categorias", u"...", None))
    # retranslateUi


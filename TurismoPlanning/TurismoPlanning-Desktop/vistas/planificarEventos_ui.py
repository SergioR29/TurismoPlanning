# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'planificarEventos.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QAbstractSpinBox, QApplication,
    QCheckBox, QComboBox, QDateEdit, QDateTimeEdit,
    QFormLayout, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpinBox, QTimeEdit, QToolButton,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_planificarTareas(object):
    def setupUi(self, planificarTareas):
        if not planificarTareas.objectName():
            planificarTareas.setObjectName(u"planificarTareas")
        planificarTareas.setWindowModality(Qt.WindowModality.WindowModal)
        planificarTareas.resize(812, 692)
        planificarTareas.setMaximumSize(QSize(812, 692))
        icon = QIcon()
        icon.addFile(u"../recursos/iconos/ic_planificar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        planificarTareas.setWindowIcon(icon)
        planificarTareas.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(26, 26, 26);")
        self.tituloLineEdit = QLineEdit(planificarTareas)
        self.tituloLineEdit.setObjectName(u"tituloLineEdit")
        self.tituloLineEdit.setGeometry(QRect(60, 10, 741, 41))
        font = QFont()
        font.setPointSize(12)
        font.setWeight(QFont.DemiBold)
        self.tituloLineEdit.setFont(font)
        self.tituloLineEdit.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(35, 35, 35);\n"
"\n"
"    border-top: none;\n"
"    border-left: none;\n"
"    border-right: none;\n"
"    border-bottom: 2px solid blue;\n"
"\n"
"padding-left:5px;\n"
"")
        self.tituloLineEdit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.icono_seleccionar = QToolButton(planificarTareas)
        self.icono_seleccionar.setObjectName(u"icono_seleccionar")
        self.icono_seleccionar.setGeometry(QRect(10, 10, 41, 41))
        self.icono_seleccionar.setStyleSheet(u"color:white;border:none;")
        icon1 = QIcon()
        icon1.addFile(u"../recursos/iconos/ic_icono.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.icono_seleccionar.setIcon(icon1)
        self.icono_seleccionar.setIconSize(QSize(44, 44))
        self.formLayoutWidget = QWidget(planificarTareas)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(60, 100, 251, 61))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.fechaDeInicioLabel = QLabel(self.formLayoutWidget)
        self.fechaDeInicioLabel.setObjectName(u"fechaDeInicioLabel")
        font1 = QFont()
        font1.setPointSize(10)
        self.fechaDeInicioLabel.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.fechaDeInicioLabel)

        self.fechaDeFinalizacionLabel = QLabel(self.formLayoutWidget)
        self.fechaDeFinalizacionLabel.setObjectName(u"fechaDeFinalizacionLabel")
        self.fechaDeFinalizacionLabel.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.fechaDeFinalizacionLabel)

        self.fechaDeFinalizacionDateEdit = QDateEdit(self.formLayoutWidget)
        self.fechaDeFinalizacionDateEdit.setObjectName(u"fechaDeFinalizacionDateEdit")
        self.fechaDeFinalizacionDateEdit.setFont(font1)
        self.fechaDeFinalizacionDateEdit.setStyleSheet(u"color:white; border-top: none;\n"
"    border-left: none;\n"
"    border-right: none;\n"
"    border-bottom: 2px solid blue;\n"
"background-color: rgb(40, 40, 40);")
        self.fechaDeFinalizacionDateEdit.setCalendarPopup(True)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.fechaDeFinalizacionDateEdit)

        self.fechaDeInicioDateEdit = QDateEdit(self.formLayoutWidget)
        self.fechaDeInicioDateEdit.setObjectName(u"fechaDeInicioDateEdit")
        self.fechaDeInicioDateEdit.setFont(font1)
        self.fechaDeInicioDateEdit.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(40, 40, 40);\n"
"\n"
" border-top: none;\n"
"    border-left: none;\n"
"    border-right: none;\n"
"    border-bottom: 2px solid blue;")
        self.fechaDeInicioDateEdit.setCalendarPopup(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.fechaDeInicioDateEdit)

        self.formLayoutWidget_2 = QWidget(planificarTareas)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(460, 90, 251, 80))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.formLayout_2.setVerticalSpacing(15)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horaDeInicioLabel = QLabel(self.formLayoutWidget_2)
        self.horaDeInicioLabel.setObjectName(u"horaDeInicioLabel")
        self.horaDeInicioLabel.setFont(font1)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.horaDeInicioLabel)

        self.horaDeFinalizacionLabel = QLabel(self.formLayoutWidget_2)
        self.horaDeFinalizacionLabel.setObjectName(u"horaDeFinalizacionLabel")
        self.horaDeFinalizacionLabel.setFont(font1)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.horaDeFinalizacionLabel)

        self.horaDeInicioTimeEdit = QTimeEdit(self.formLayoutWidget_2)
        self.horaDeInicioTimeEdit.setObjectName(u"horaDeInicioTimeEdit")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(False)
        self.horaDeInicioTimeEdit.setFont(font2)
        self.horaDeInicioTimeEdit.setStyleSheet(u"color:white; \n"
"border-top: none;\n"
"    border-left: none;\n"
"    border-right: none;\n"
"    border-bottom: 2px solid blue;\n"
"background-color: rgb(40, 40, 40);")
        self.horaDeInicioTimeEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horaDeInicioTimeEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.horaDeInicioTimeEdit.setCalendarPopup(False)
        self.horaDeInicioTimeEdit.setTimeSpec(Qt.TimeSpec.LocalTime)
        self.horaDeInicioTimeEdit.setTime(QTime(0, 0, 0))

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.horaDeInicioTimeEdit)

        self.horaDeFinalizacionTimeEdit = QTimeEdit(self.formLayoutWidget_2)
        self.horaDeFinalizacionTimeEdit.setObjectName(u"horaDeFinalizacionTimeEdit")
        self.horaDeFinalizacionTimeEdit.setFont(font2)
        self.horaDeFinalizacionTimeEdit.setStyleSheet(u"color:white; \n"
"border-top: none;\n"
"    border-left: none;\n"
"    border-right: none;\n"
"    border-bottom: 2px solid blue;\n"
"background-color: rgb(40, 40, 40);")
        self.horaDeFinalizacionTimeEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horaDeFinalizacionTimeEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.horaDeFinalizacionTimeEdit.setCurrentSection(QDateTimeEdit.Section.HourSection)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.horaDeFinalizacionTimeEdit)

        self.horizontalLayoutWidget = QWidget(planificarTareas)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(62, 220, 371, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.categoriaLabel = QLabel(self.horizontalLayoutWidget)
        self.categoriaLabel.setObjectName(u"categoriaLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categoriaLabel.sizePolicy().hasHeightForWidth())
        self.categoriaLabel.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.categoriaLabel)

        self.categoriaComboBox = QComboBox(self.horizontalLayoutWidget)
        self.categoriaComboBox.setObjectName(u"categoriaComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.categoriaComboBox.sizePolicy().hasHeightForWidth())
        self.categoriaComboBox.setSizePolicy(sizePolicy1)
        self.categoriaComboBox.setFont(font1)
        self.categoriaComboBox.setStyleSheet(u"color:white; border-top: none;\n"
"    border-left: none;\n"
"    border-right: none;\n"
"    border-bottom: 2px solid blue;\n"
"background-color: rgb(40, 40, 40);\n"
"padding-left:5px;\n"
"padding-right:5px;")

        self.horizontalLayout.addWidget(self.categoriaComboBox)

        self.crearCategoria = QToolButton(self.horizontalLayoutWidget)
        self.crearCategoria.setObjectName(u"crearCategoria")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(20)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.crearCategoria.sizePolicy().hasHeightForWidth())
        self.crearCategoria.setSizePolicy(sizePolicy2)
        self.crearCategoria.setStyleSheet(u"border:none;margin-left:7px;")
        icon2 = QIcon()
        icon2.addFile(u"../recursos/iconos/ic_add.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.crearCategoria.setIcon(icon2)
        self.crearCategoria.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.crearCategoria)

        self.frame = QFrame(planificarTareas)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(52, 380, 701, 221))
        self.frame.setStyleSheet(u"border:10px solid blue;background-color: blue;border-radius:15px;")
        self.descT = QPlainTextEdit(self.frame)
        self.descT.setObjectName(u"descT")
        self.descT.setGeometry(QRect(10, 10, 681, 201))
        self.descT.setFont(font1)
        self.descT.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(48, 48, 48);\n"
"border-radius:0px;\n"
"border:none;\n"
"padding:1px;")
        self.cerrar = QPushButton(planificarTareas)
        self.cerrar.setObjectName(u"cerrar")
        self.cerrar.setGeometry(QRect(240, 630, 111, 41))
        font3 = QFont()
        font3.setPointSize(11)
        font3.setBold(True)
        self.cerrar.setFont(font3)
        self.cerrar.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"background-color: rgb(0, 170, 255);")
        icon3 = QIcon()
        icon3.addFile(u"../recursos/iconos/cerrar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cerrar.setIcon(icon3)
        self.cerrar.setIconSize(QSize(24, 25))
        self.guardarTarea = QPushButton(planificarTareas)
        self.guardarTarea.setObjectName(u"guardarTarea")
        self.guardarTarea.setGeometry(QRect(470, 630, 111, 41))
        self.guardarTarea.setFont(font3)
        self.guardarTarea.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"background-color: rgb(0, 170, 255);")
        icon4 = QIcon()
        icon4.addFile(u"../recursos/iconos/ic_guardar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.guardarTarea.setIcon(icon4)
        self.guardarTarea.setIconSize(QSize(20, 24))
        self.label = QLabel(planificarTareas)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(70, 350, 671, 23))
        font4 = QFont()
        font4.setPointSize(15)
        font4.setBold(True)
        self.label.setFont(font4)
        self.label.setStyleSheet(u"color:white;border:none")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayoutWidget_2 = QWidget(planificarTareas)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(62, 260, 331, 31))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.prioridadLabel = QLabel(self.horizontalLayoutWidget_2)
        self.prioridadLabel.setObjectName(u"prioridadLabel")
        sizePolicy.setHeightForWidth(self.prioridadLabel.sizePolicy().hasHeightForWidth())
        self.prioridadLabel.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.prioridadLabel)

        self.prioridadSpinBox = QSpinBox(self.horizontalLayoutWidget_2)
        self.prioridadSpinBox.setObjectName(u"prioridadSpinBox")
        sizePolicy1.setHeightForWidth(self.prioridadSpinBox.sizePolicy().hasHeightForWidth())
        self.prioridadSpinBox.setSizePolicy(sizePolicy1)
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(True)
        self.prioridadSpinBox.setFont(font5)
        self.prioridadSpinBox.setStyleSheet(u"color:white; border-top: none;\n"
"    border-left: none;\n"
"    border-right: none;\n"
"    border-bottom: 2px solid blue;\n"
"background-color: rgb(40, 40, 40);")
        self.prioridadSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.prioridadSpinBox.setMinimum(1)

        self.horizontalLayout_2.addWidget(self.prioridadSpinBox)

        self.exportar = QTreeWidget(planificarTareas)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font5);
        __qtreewidgetitem.setBackground(0, QColor(0, 170, 255));
        __qtreewidgetitem.setForeground(0, brush);
        self.exportar.setHeaderItem(__qtreewidgetitem)
        self.exportar.setObjectName(u"exportar")
        self.exportar.setGeometry(QRect(500, 220, 256, 91))
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
        self.incluir_FI = QCheckBox(planificarTareas)
        self.incluir_FI.setObjectName(u"incluir_FI")
        self.incluir_FI.setGeometry(QRect(320, 100, 78, 20))
        self.incluir_FI.setStyleSheet(u"\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border-radius: 7.5px; /* Bordes redondeados */\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    background-color: black;\n"
"    border: 2px solid blue; /* Color de la casilla sin marcar */\n"
"    border-radius: 7.5px; /* Bordes redondeados */\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: aqua; /* Color de la casilla marcada */\n"
"    border: 2px solid blue;\n"
"    border-radius: 7.5px; /* Bordes redondeados */\n"
"}")
        self.incluir_HI = QCheckBox(planificarTareas)
        self.incluir_HI.setObjectName(u"incluir_HI")
        self.incluir_HI.setGeometry(QRect(720, 95, 71, 20))
        self.incluir_HI.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border-radius: 7.5px; /* Bordes redondeados */\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    background-color: black;\n"
"    border: 2px solid blue; /* Color de la casilla sin marcar */\n"
"    border-radius: 7.5px; /* Bordes redondeados */\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: aqua; /* Color de la casilla marcada */\n"
"    border: 2px solid blue;\n"
"    border-radius: 7.5px; /* Bordes redondeados */\n"
"}")
        self.incluir_HF = QCheckBox(planificarTareas)
        self.incluir_HF.setObjectName(u"incluir_HF")
        self.incluir_HF.setGeometry(QRect(720, 140, 78, 20))
        self.incluir_HF.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border-radius: 7.5px; /* Bordes redondeados */\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    background-color: black;\n"
"    border: 2px solid blue; /* Color de la casilla sin marcar */\n"
"    border-radius: 7.5px; /* Bordes redondeados */\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: aqua; /* Color de la casilla marcada */\n"
"    border: 2px solid blue;\n"
"    border-radius: 7.5px; /* Bordes redondeados */\n"
"}")
        self.refrescar = QToolButton(planificarTareas)
        self.refrescar.setObjectName(u"refrescar")
        self.refrescar.setGeometry(QRect(13, 220, 31, 31))
        sizePolicy2.setHeightForWidth(self.refrescar.sizePolicy().hasHeightForWidth())
        self.refrescar.setSizePolicy(sizePolicy2)
        self.refrescar.setStyleSheet(u"border:none;margin-left:7px;")
        icon5 = QIcon()
        icon5.addFile(u"../recursos/iconos/refrescar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.refrescar.setIcon(icon5)
        self.refrescar.setIconSize(QSize(24, 24))
        self.ayuda = QToolButton(planificarTareas)
        self.ayuda.setObjectName(u"ayuda")
        self.ayuda.setGeometry(QRect(760, 640, 40, 40))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.ayuda.sizePolicy().hasHeightForWidth())
        self.ayuda.setSizePolicy(sizePolicy3)
        self.ayuda.setStyleSheet(u"background-color: rgb(26, 26, 26);border:none;")
        icon6 = QIcon()
        icon6.addFile(u"../recursos/iconos/ayuda.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ayuda.setIcon(icon6)
        self.ayuda.setIconSize(QSize(40, 40))

        self.retranslateUi(planificarTareas)
        self.cerrar.clicked.connect(planificarTareas.close)

        QMetaObject.connectSlotsByName(planificarTareas)
    # setupUi

    def retranslateUi(self, planificarTareas):
        planificarTareas.setWindowTitle(QCoreApplication.translate("planificarTareas", u"Planificar evento", None))
        self.tituloLineEdit.setPlaceholderText(QCoreApplication.translate("planificarTareas", u"Agregar un T\u00edtulo", None))
        self.icono_seleccionar.setText("")
        self.fechaDeInicioLabel.setText(QCoreApplication.translate("planificarTareas", u"Fecha de Inicio", None))
        self.fechaDeFinalizacionLabel.setText(QCoreApplication.translate("planificarTareas", u"Fecha de Finalizaci\u00f3n", None))
        self.horaDeInicioLabel.setText(QCoreApplication.translate("planificarTareas", u"Hora de Inicio", None))
        self.horaDeFinalizacionLabel.setText(QCoreApplication.translate("planificarTareas", u"Hora de Finalizaci\u00f3n", None))
        self.horaDeInicioTimeEdit.setDisplayFormat(QCoreApplication.translate("planificarTareas", u"H:mm", None))
        self.horaDeFinalizacionTimeEdit.setDisplayFormat(QCoreApplication.translate("planificarTareas", u"H:mm", None))
        self.categoriaLabel.setText(QCoreApplication.translate("planificarTareas", u"Categor\u00eda", None))
        self.crearCategoria.setText("")
        self.cerrar.setText(QCoreApplication.translate("planificarTareas", u" Cerrar", None))
        self.guardarTarea.setText(QCoreApplication.translate("planificarTareas", u"  Guardar", None))
        self.label.setText(QCoreApplication.translate("planificarTareas", u"DESCRIPCI\u00d3N", None))
        self.prioridadLabel.setStyleSheet(QCoreApplication.translate("planificarTareas", u"0", None))
        self.prioridadLabel.setText(QCoreApplication.translate("planificarTareas", u"Prioridad ", None))
        ___qtreewidgetitem = self.exportar.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("planificarTareas", u"Exportar a", None));
        self.incluir_FI.setText(QCoreApplication.translate("planificarTareas", u"\u00bfIncluir?", None))
        self.incluir_HI.setText(QCoreApplication.translate("planificarTareas", u"\u00bfIncluir?", None))
        self.incluir_HF.setText(QCoreApplication.translate("planificarTareas", u"\u00bfIncluir?", None))
        self.refrescar.setText("")
        self.ayuda.setText(QCoreApplication.translate("planificarTareas", u"...", None))
    # retranslateUi


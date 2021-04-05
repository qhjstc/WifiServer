# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gauge.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(887, 642)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 110, 601, 491))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.graph_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.graph_layout.setContentsMargins(0, 0, 0, 0)
        self.graph_layout.setObjectName("graph_layout")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(680, 140, 171, 471))
        self.layoutWidget.setObjectName("layoutWidget")
        self.buttonLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setObjectName("buttonLayout")
        self.start_button = QtWidgets.QPushButton(self.layoutWidget)
        self.start_button.setObjectName("start_button")
        self.buttonLayout.addWidget(self.start_button)
        self.button1 = QtWidgets.QPushButton(self.layoutWidget)
        self.button1.setObjectName("button1")
        self.buttonLayout.addWidget(self.button1)
        self.button2 = QtWidgets.QPushButton(self.layoutWidget)
        self.button2.setObjectName("button2")
        self.buttonLayout.addWidget(self.button2)
        self.button3 = QtWidgets.QPushButton(self.layoutWidget)
        self.button3.setObjectName("button3")
        self.buttonLayout.addWidget(self.button3)
        self.button4 = QtWidgets.QPushButton(self.layoutWidget)
        self.button4.setObjectName("button4")
        self.buttonLayout.addWidget(self.button4)
        self.button6 = QtWidgets.QPushButton(self.layoutWidget)
        self.button6.setObjectName("pushButton_2")
        self.buttonLayout.addWidget(self.button6)
        self.button5 = QtWidgets.QPushButton(self.layoutWidget)
        self.button5.setObjectName("button5")
        self.buttonLayout.addWidget(self.button5)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 10, 601, 93))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.title_layout = QtWidgets.QVBoxLayout()
        self.title_layout.setObjectName("title_layout")
        self.title_list = QtWidgets.QListWidget(self.layoutWidget1)
        self.title_list.setObjectName("title_list")
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(26)
        item.setFont(font)
        self.title_list.addItem(item)
        self.title_layout.addWidget(self.title_list)
        self.horizontalLayout.addLayout(self.title_layout)
        self.amplitude = QtWidgets.QListView(self.layoutWidget1)
        self.amplitude.setObjectName("amplitude")
        self.horizontalLayout.addWidget(self.amplitude)
        self.listView_2 = QtWidgets.QListView(self.layoutWidget1)
        self.listView_2.setObjectName("listView_2")
        self.horizontalLayout.addWidget(self.listView_2)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(680, 10, 171, 81))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ip_text = QtWidgets.QPlainTextEdit(self.widget)
        self.ip_text.setObjectName("ip_text")
        self.verticalLayout.addWidget(self.ip_text)
        self.port_text = QtWidgets.QPlainTextEdit(self.widget)
        self.port_text.setObjectName("port_text")
        self.verticalLayout.addWidget(self.port_text)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.start_button.setText(_translate("Form", "start_button"))
        self.button1.setText(_translate("Form", "50mV"))
        self.button2.setText(_translate("Form", "500mV"))
        self.button3.setText(_translate("Form", "5V"))
        self.button4.setText(_translate("Form", "50V"))
        self.button6.setText(_translate("Form", "50uA"))
        self.button5.setText(_translate("Form", "50mA"))
        __sortingEnabled = self.title_list.isSortingEnabled()
        self.title_list.setSortingEnabled(False)
        item = self.title_list.item(0)
        item.setText(_translate("Form", "Gauge"))
        self.title_list.setSortingEnabled(__sortingEnabled)
        self.ip_text.setPlainText(_translate("Form", "input ip address"))
        self.port_text.setPlainText(_translate("Form", "input ip port"))


class MyGraphWindows(QtWidgets.QMainWindow, Ui_Form):

    def __init__(self):
        super(MyGraphWindows, self).__init__()

        self.x = []
        self.y = []
        self.setupUi(self)        # 初始化窗口
        self.p1, self.p2 = self.set_graph_ui()   # 设置绘图窗口

    def set_graph_ui(self):
        pg.setConfigOptions(antialias=True)
        win = pg.GraphicsLayoutWidget()         # 创建pg layout?

        self.graph_layout.addWidget(win)

        p1 = win.addPlot(title="波形图")
        p1.setLabel('left', text='meg', color='#ffffff')  # y轴设置函数
        p1.addLegend()

        win.nextRow()  # layout换行，采用垂直排列，不添加此行则默认水平排列
        p2 = win.addPlot(title="频谱")
        p2.setLabel('left', text='meg', color='#ffffff')  # y轴设置函数
        p2.addLegend()
        return p1, p2


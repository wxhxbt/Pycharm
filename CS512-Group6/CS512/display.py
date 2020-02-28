# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'display.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
import test
from GeneticAlgorithm import *
import sip
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time


class Display_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Display_MainWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 10, 291, 41))
        self.pushButton.setObjectName("pushButton")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(330, 0, 871, 881))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 70, 71, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 100, 71, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(100, 70, 211, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 100, 211, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 140, 291, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 190, 291, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.pushButton.clicked.connect(self.display_maps)
        self.pushButton_2.clicked.connect(self.add_start_and_stop_points)
        self.pushButton_3.clicked.connect(self.display_results)

        '''self.F = MyFigure(width=6, height=5, dpi=100)
        self.gridlayout = QGridLayout(self.groupBox)
        self.gridlayout.addWidget(self.F, 0, 1)'''

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Display Maps"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.label.setText(_translate("MainWindow", "Start Point"))
        self.label_2.setText(_translate("MainWindow", "Stop Points"))
        self.pushButton_2.setText(_translate("MainWindow", "Add Start And Stop Points"))
        self.pushButton_3.setText(_translate("MainWindow", "Display Results"))

    def display_maps(self):

        self.F = MyFigure(width=6, height=5, dpi=100)
        data = test.data_load()
        x = []
        y = []
        text = []
        for i in data.values():
            x.append(i[0])
            y.append(i[1])
        for i in data.keys():
            text.append(i)

        self.axes = self.F.fig.add_subplot(111)
        plt.scatter(x, y)
        for i in range(len(x)):
            plt.annotate(text[i], xy=(x[i], y[i]), xytext=(x[i] + 50, y[i] + 50))
        self.gridlayout = QGridLayout(self.groupBox)
        self.gridlayout.addWidget(self.F, 0, 1)
        self.F.fig.suptitle("Map")


    def add_start_and_stop_points(self):
        test.START_POINT = ''
        test.STOP_POINTS = []
        Start_point = self.lineEdit.text()
        Stop_points = self.lineEdit_2.text()
        Stop_points.replace(" ", "")
        Stop_points_list = Stop_points.split()
        l = [i for i in range(1, 49)]
        l_new = [str(x) for x in l]
        print(l_new)
        if Start_point in l_new and set(Stop_points_list).issubset(set(l_new)):
            test.START_POINT = Start_point
            test.STOP_POINTS = Stop_points_list
            QMessageBox().information(None, "Information", "Adding points completes")
        else:
            QMessageBox().warning(None, "Warning", "Wrong input of points")


    def display_results(self):
        QMessageBox().information(None, "Information", "Computing...")
        path = test.run_test()
        self.F = MyFigure(width=6, height=5, dpi=100)
        data = test.data_load()
        x = []
        y = []
        text = []
        for i in data.values():
            x.append(i[0])
            y.append(i[1])
        for i in data.keys():
            text.append(i)
        x1 = []
        y1 = []
        for i in path:
            if i in data.keys():
                x1.append(data[i][0])
                y1.append(data[i][1])
        self.axes = self.F.fig.add_subplot(111)
        plt.scatter(x, y)
        for i in range(len(x)):
            plt.annotate(text[i], xy=(x[i], y[i]), xytext=(x[i] + 50, y[i] + 50))
        plt.plot(x1, y1, 'm.-.', linewidth=1)
        self.F.fig.suptitle(path)
        self.F.show()







class MyFigure(FigureCanvas):
    def __init__(self, width, height, dpi):
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        super(MyFigure, self).__init__(self.fig)

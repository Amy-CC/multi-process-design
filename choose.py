# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(558, 333)
        self.processname = QtWidgets.QLabel(Dialog)
        self.processname.setGeometry(QtCore.QRect(30, 30, 180, 30))
        self.processname.setObjectName("processname")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(460, 60, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(460, 110, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.name = QtWidgets.QLineEdit(Dialog)
        self.name.setGeometry(QtCore.QRect(260, 30, 111, 31))
        self.name.setObjectName("name")
        self.starttime = QtWidgets.QLabel(Dialog)
        self.starttime.setGeometry(QtCore.QRect(30, 90, 181, 41))
        self.starttime.setObjectName("starttime")
        self.runtime = QtWidgets.QLabel(Dialog)
        self.runtime.setGeometry(QtCore.QRect(30, 160, 180, 30))
        self.runtime.setObjectName("runtime")
        self.begin = QtWidgets.QDoubleSpinBox(Dialog)
        self.begin.setGeometry(QtCore.QRect(260, 90, 111, 31))
        self.begin.setObjectName("begin")
        self.running = QtWidgets.QDoubleSpinBox(Dialog)
        self.running.setGeometry(QtCore.QRect(260, 160, 111, 31))
        self.running.setObjectName("running")
        self.runtime_2 = QtWidgets.QLabel(Dialog)
        self.runtime_2.setGeometry(QtCore.QRect(30, 220, 180, 30))
        self.runtime_2.setObjectName("runtime_2")
        self.memorynum = QtWidgets.QDoubleSpinBox(Dialog)
        self.memorynum.setGeometry(QtCore.QRect(260, 220, 111, 31))
        self.memorynum.setObjectName("memorynum")
        self.runtime_3 = QtWidgets.QLabel(Dialog)
        self.runtime_3.setGeometry(QtCore.QRect(30, 280, 221, 30))
        self.runtime_3.setObjectName("runtime_3")
        self.machinenum = QtWidgets.QSpinBox(Dialog)
        self.machinenum.setGeometry(QtCore.QRect(270, 280, 101, 31))
        self.machinenum.setObjectName("machinenum")

        self.retranslateUi(Dialog)
        self.pushButton_2.clicked.connect(Dialog.reject)
        self.pushButton.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.pushButton, self.pushButton_2)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.processname.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:18pt;\">请输入作业名</span></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "OK"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))
        self.starttime.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:18pt;\">请输入到达时间</span></p></body></html>"))
        self.runtime.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:18pt;\">请输入运行时间</span></p></body></html>"))
        self.runtime_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:18pt;\">请输入作业大小</span></p></body></html>"))
        self.runtime_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:18pt;\">请输入需磁带机数量</span></p></body></html>"))


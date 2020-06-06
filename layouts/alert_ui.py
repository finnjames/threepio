# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'alert.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 110)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.close_button = QtWidgets.QPushButton(Dialog)
        self.close_button.setObjectName("close_button")
        self.gridLayout.addWidget(self.close_button, 2, 1, 1, 1)
        self.alert = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Sans")
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.alert.setFont(font)
        self.alert.setAlignment(QtCore.Qt.AlignCenter)
        self.alert.setObjectName("alert")
        self.gridLayout.addWidget(self.alert, 0, 0, 1, 2)

        self.retranslateUi(Dialog)
        self.close_button.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.close_button.setText(_translate("Dialog", "Close"))
        self.alert.setText(_translate("Dialog", "!!!"))

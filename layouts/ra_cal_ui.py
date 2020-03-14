# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ra_cal.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(363, 99)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.dialog_button_box = QtWidgets.QDialogButtonBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Sans")
        self.dialog_button_box.setFont(font)
        self.dialog_button_box.setOrientation(QtCore.Qt.Horizontal)
        self.dialog_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dialog_button_box.setCenterButtons(False)
        self.dialog_button_box.setObjectName("dialog_button_box")
        self.gridLayout.addWidget(self.dialog_button_box, 3, 1, 1, 2)
        self.sidereal_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Sans")
        font.setPointSize(16)
        self.sidereal_label.setFont(font)
        self.sidereal_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.sidereal_label.setObjectName("sidereal_label")
        self.gridLayout.addWidget(self.sidereal_label, 0, 1, 1, 1)
        self.sidereal_value = QtWidgets.QTimeEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Mono")
        self.sidereal_value.setFont(font)
        self.sidereal_value.setObjectName("sidereal_value")
        self.gridLayout.addWidget(self.sidereal_value, 0, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.dialog_button_box.rejected.connect(Dialog.reject)
        self.dialog_button_box.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.sidereal_label.setText(_translate("Dialog", "Current Sidereal Time"))
        self.sidereal_value.setDisplayFormat(_translate("Dialog", "HH:mm:ss"))

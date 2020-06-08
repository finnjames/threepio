# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ra_cal.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 100)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.sidereal_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        font.setPointSize(13)
        self.sidereal_label.setFont(font)
        self.sidereal_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.sidereal_label.setObjectName("sidereal_label")
        self.gridLayout.addWidget(self.sidereal_label, 2, 2, 1, 1)
        self.sidereal_value = QtWidgets.QTimeEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        self.sidereal_value.setFont(font)
        self.sidereal_value.setObjectName("sidereal_value")
        self.gridLayout.addWidget(self.sidereal_value, 2, 3, 1, 1)
        self.button_frame = QtWidgets.QFrame(Dialog)
        self.button_frame.setObjectName("button_frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.button_frame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cancel_button = QtWidgets.QPushButton(self.button_frame)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        self.cancel_button.setFont(font)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout_2.addWidget(self.cancel_button, 1, 1, 1, 1)
        self.ok_button = QtWidgets.QPushButton(self.button_frame)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        self.ok_button.setFont(font)
        self.ok_button.setDefault(True)
        self.ok_button.setObjectName("ok_button")
        self.gridLayout_2.addWidget(self.ok_button, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.button_frame, 3, 2, 1, 2)

        self.retranslateUi(Dialog)
        self.cancel_button.clicked.connect(Dialog.reject)
        self.ok_button.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "RA Calibration"))
        self.sidereal_label.setText(_translate("Dialog", "Current Sidereal Time"))
        self.sidereal_value.setDisplayFormat(_translate("Dialog", "HH:mm:ss"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))
        self.ok_button.setText(_translate("Dialog", "Set RA"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quit.ui'
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
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        self.cancel_button.setFont(font)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 2, 2, 1, 1)
        self.ok_button = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        self.ok_button.setFont(font)
        self.ok_button.setDefault(True)
        self.ok_button.setObjectName("ok_button")
        self.gridLayout.addWidget(self.ok_button, 2, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.sidereal_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        self.sidereal_label.setFont(font)
        self.sidereal_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.sidereal_label.setWordWrap(True)
        self.sidereal_label.setObjectName("sidereal_label")
        self.gridLayout.addWidget(self.sidereal_label, 0, 0, 1, 4)

        self.retranslateUi(Dialog)
        self.cancel_button.clicked.connect(Dialog.close)
        self.ok_button.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.ok_button, self.cancel_button)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Quit?"))
        self.cancel_button.setText(_translate("Dialog", "No, go back"))
        self.ok_button.setText(_translate("Dialog", "Yes, Quit"))
        self.sidereal_label.setText(_translate("Dialog", "Are you sure you want to quit? Incomplete observations may not be usable."))

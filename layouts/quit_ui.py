# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quit.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 110)
        Dialog.setModal(True)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.sidereal_label = QtWidgets.QLabel(Dialog)
        self.sidereal_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.sidereal_label.setWordWrap(True)
        self.sidereal_label.setObjectName("sidereal_label")
        self.gridLayout_2.addWidget(self.sidereal_label, 1, 1, 1, 1)
        self.button_frame = QtWidgets.QFrame(Dialog)
        self.button_frame.setObjectName("button_frame")
        self.gridLayout = QtWidgets.QGridLayout(self.button_frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.ok_button = QtWidgets.QPushButton(self.button_frame)
        self.ok_button.setObjectName("ok_button")
        self.gridLayout.addWidget(self.ok_button, 0, 3, 1, 1)
        self.cancel_button = QtWidgets.QPushButton(self.button_frame)
        self.cancel_button.setDefault(True)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.button_frame, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.cancel_button.clicked.connect(Dialog.close)
        self.ok_button.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.cancel_button, self.ok_button)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Exit?"))
        self.sidereal_label.setText(_translate("Dialog", "Are you sure you want to exit? Incomplete observations may not be usable."))
        self.ok_button.setText(_translate("Dialog", "Yes, Exit"))
        self.cancel_button.setText(_translate("Dialog", "No, go back"))

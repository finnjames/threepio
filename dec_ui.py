# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'misc/dec_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(323, 110)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.discard_cal_button = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Sans")
        self.discard_cal_button.setFont(font)
        self.discard_cal_button.setObjectName("discard_cal_button")
        self.gridLayout.addWidget(self.discard_cal_button, 3, 1, 1, 1)
        self.next_cal_button = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Sans")
        self.next_cal_button.setFont(font)
        self.next_cal_button.setCheckable(False)
        self.next_cal_button.setDefault(True)
        self.next_cal_button.setObjectName("next_cal_button")
        self.gridLayout.addWidget(self.next_cal_button, 3, 2, 1, 1)
        self.set_dec_value = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Mono")
        self.set_dec_value.setFont(font)
        self.set_dec_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.set_dec_value.setObjectName("set_dec_value")
        self.gridLayout.addWidget(self.set_dec_value, 1, 2, 1, 1)
        self.north_or_south_combo_box = QtWidgets.QComboBox(Dialog)
        self.north_or_south_combo_box.setObjectName("north_or_south_combo_box")
        self.gridLayout.addWidget(self.north_or_south_combo_box, 3, 0, 1, 1)
        self.set_dec_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Sans")
        self.set_dec_label.setFont(font)
        self.set_dec_label.setObjectName("set_dec_label")
        self.gridLayout.addWidget(self.set_dec_label, 1, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.next_cal_button, self.discard_cal_button)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.discard_cal_button.setText(_translate("Dialog", "Discard"))
        self.next_cal_button.setText(_translate("Dialog", "Next"))
        self.set_dec_value.setText(_translate("Dialog", "TextLabel"))
        self.set_dec_label.setText(_translate("Dialog", "Set declination to"))

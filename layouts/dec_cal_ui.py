# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dec_cal.ui'
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
        self.button_box = QtWidgets.QWidget(Dialog)
        self.button_box.setObjectName("button_box")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.button_box)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.north_or_south_combo_box = QtWidgets.QComboBox(self.button_box)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Sans")
        self.north_or_south_combo_box.setFont(font)
        self.north_or_south_combo_box.setObjectName("north_or_south_combo_box")
        self.gridLayout_2.addWidget(self.north_or_south_combo_box, 0, 0, 1, 1)
        self.discard_cal_button = QtWidgets.QPushButton(self.button_box)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Sans")
        self.discard_cal_button.setFont(font)
        self.discard_cal_button.setObjectName("discard_cal_button")
        self.gridLayout_2.addWidget(self.discard_cal_button, 0, 2, 1, 1)
        self.next_cal_button = QtWidgets.QPushButton(self.button_box)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Sans")
        self.next_cal_button.setFont(font)
        self.next_cal_button.setCheckable(False)
        self.next_cal_button.setDefault(True)
        self.next_cal_button.setObjectName("next_cal_button")
        self.gridLayout_2.addWidget(self.next_cal_button, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.button_box, 2, 0, 1, 3)
        self.set_dec_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Sans")
        self.set_dec_label.setFont(font)
        self.set_dec_label.setObjectName("set_dec_label")
        self.gridLayout.addWidget(self.set_dec_label, 1, 0, 1, 2)
        self.set_dec_value = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("IBM Plex Mono")
        self.set_dec_value.setFont(font)
        self.set_dec_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.set_dec_value.setObjectName("set_dec_value")
        self.gridLayout.addWidget(self.set_dec_value, 1, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Declination Calibration"))
        self.discard_cal_button.setText(_translate("Dialog", "Discard"))
        self.next_cal_button.setText(_translate("Dialog", "Next"))
        self.set_dec_label.setText(_translate("Dialog", "Set declination to"))
        self.set_dec_value.setText(_translate("Dialog", "TextLabel"))

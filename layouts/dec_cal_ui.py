# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dec_cal.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(554, 369)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cal_display_widget = QtWidgets.QWidget(Dialog)
        self.cal_display_widget.setObjectName("cal_display_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.cal_display_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.degree_values_label = QtWidgets.QLabel(self.cal_display_widget)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        font.setBold(True)
        font.setWeight(75)
        self.degree_values_label.setFont(font)
        self.degree_values_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.degree_values_label.setObjectName("degree_values_label")
        self.gridLayout.addWidget(self.degree_values_label, 0, 2, 1, 1)
        self.input_data_label = QtWidgets.QLabel(self.cal_display_widget)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        self.input_data_label.setFont(font)
        self.input_data_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.input_data_label.setObjectName("input_data_label")
        self.gridLayout.addWidget(self.input_data_label, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.cal_display_widget)
        self.set_dec_widget = QtWidgets.QWidget(Dialog)
        self.set_dec_widget.setObjectName("set_dec_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.set_dec_widget)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.set_dec_label = QtWidgets.QLabel(self.set_dec_widget)
        self.set_dec_label.setObjectName("set_dec_label")
        self.horizontalLayout.addWidget(self.set_dec_label)
        self.set_dec_value = QtWidgets.QLabel(self.set_dec_widget)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        font.setPointSize(20)
        self.set_dec_value.setFont(font)
        self.set_dec_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.set_dec_value.setObjectName("set_dec_value")
        self.horizontalLayout.addWidget(self.set_dec_value)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.set_dec_widget)
        self.warning_label = QtWidgets.QLabel(Dialog)
        self.warning_label.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.warning_label.setFont(font)
        self.warning_label.setStyleSheet("color: darkorange")
        self.warning_label.setAlignment(QtCore.Qt.AlignCenter)
        self.warning_label.setObjectName("warning_label")
        self.verticalLayout.addWidget(self.warning_label)
        self.button_frame = QtWidgets.QFrame(Dialog)
        self.button_frame.setObjectName("button_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.button_frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.north_south_combo_box = QtWidgets.QComboBox(self.button_frame)
        self.north_south_combo_box.setObjectName("north_south_combo_box")
        self.north_south_combo_box.addItem("")
        self.north_south_combo_box.addItem("")
        self.horizontalLayout_3.addWidget(self.north_south_combo_box)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.discard_cal_button = QtWidgets.QPushButton(self.button_frame)
        self.discard_cal_button.setObjectName("discard_cal_button")
        self.horizontalLayout_3.addWidget(self.discard_cal_button)
        self.previous_button = QtWidgets.QPushButton(self.button_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previous_button.sizePolicy().hasHeightForWidth())
        self.previous_button.setSizePolicy(sizePolicy)
        self.previous_button.setObjectName("previous_button")
        self.horizontalLayout_3.addWidget(self.previous_button)
        self.next_button = QtWidgets.QPushButton(self.button_frame)
        self.next_button.setObjectName("next_button")
        self.horizontalLayout_3.addWidget(self.next_button)
        self.record_button = QtWidgets.QPushButton(self.button_frame)
        self.record_button.setCheckable(False)
        self.record_button.setDefault(True)
        self.record_button.setObjectName("record_button")
        self.horizontalLayout_3.addWidget(self.record_button)
        self.save_button = QtWidgets.QPushButton(self.button_frame)
        self.save_button.setEnabled(False)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout_3.addWidget(self.save_button)
        self.verticalLayout.addWidget(self.button_frame)

        self.retranslateUi(Dialog)
        self.discard_cal_button.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.north_south_combo_box, self.record_button)
        Dialog.setTabOrder(self.record_button, self.next_button)
        Dialog.setTabOrder(self.next_button, self.previous_button)
        Dialog.setTabOrder(self.previous_button, self.discard_cal_button)
        Dialog.setTabOrder(self.discard_cal_button, self.save_button)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Declination Calibration"))
        self.degree_values_label.setText(_translate("Dialog", "<html><head/><body><p>-25<br/>-15<br/>-5<br/>5<br/>15<br/>25<br/>35<br/>45<br/>55<br/>65<br/>75<br/>85<br/>95</p></body></html>"))
        self.input_data_label.setText(_translate("Dialog", "<html><head/><body><p>-25<br/>-15<br/>-5<br/>5<br/>15<br/>25<br/>35<br/>45<br/>55<br/>65<br/>75<br/>85<br/>95</p></body></html>"))
        self.set_dec_label.setText(_translate("Dialog", "Currently calibrating"))
        self.set_dec_value.setText(_translate("Dialog", "N°"))
        self.warning_label.setText(_translate("Dialog", "Warning about data"))
        self.north_south_combo_box.setItemText(0, _translate("Dialog", "S → N"))
        self.north_south_combo_box.setItemText(1, _translate("Dialog", "N → S"))
        self.discard_cal_button.setText(_translate("Dialog", "Discard All"))
        self.previous_button.setText(_translate("Dialog", "<"))
        self.next_button.setText(_translate("Dialog", ">"))
        self.record_button.setText(_translate("Dialog", "Record"))
        self.save_button.setText(_translate("Dialog", "Save"))

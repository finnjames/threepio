# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'threepio.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 640)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 640))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setObjectName("main_frame")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.main_frame)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.data_display_group = QtWidgets.QGroupBox(self.main_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_display_group.sizePolicy().hasHeightForWidth())
        self.data_display_group.setSizePolicy(sizePolicy)
        self.data_display_group.setObjectName("data_display_group")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.data_display_group)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dec_label = QtWidgets.QLabel(self.data_display_group)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.dec_label.setFont(font)
        self.dec_label.setObjectName("dec_label")
        self.gridLayout_2.addWidget(self.dec_label, 2, 0, 1, 1)
        self.channelB_label = QtWidgets.QLabel(self.data_display_group)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.channelB_label.setFont(font)
        self.channelB_label.setObjectName("channelB_label")
        self.gridLayout_2.addWidget(self.channelB_label, 5, 0, 1, 1)
        self.dec_value = QtWidgets.QLabel(self.data_display_group)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.dec_value.setFont(font)
        self.dec_value.setScaledContents(False)
        self.dec_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dec_value.setObjectName("dec_value")
        self.gridLayout_2.addWidget(self.dec_value, 2, 1, 1, 1)
        self.channelA_value = QtWidgets.QLabel(self.data_display_group)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(33, 150, 243))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 150, 243))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 150, 243))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 150, 243))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.channelA_value.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.channelA_value.setFont(font)
        self.channelA_value.setScaledContents(False)
        self.channelA_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.channelA_value.setObjectName("channelA_value")
        self.gridLayout_2.addWidget(self.channelA_value, 3, 1, 1, 1)
        self.channelA_label = QtWidgets.QLabel(self.data_display_group)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.channelA_label.setFont(font)
        self.channelA_label.setObjectName("channelA_label")
        self.gridLayout_2.addWidget(self.channelA_label, 3, 0, 1, 1)
        self.ra_value = QtWidgets.QLabel(self.data_display_group)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.ra_value.setFont(font)
        self.ra_value.setScaledContents(False)
        self.ra_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ra_value.setObjectName("ra_value")
        self.gridLayout_2.addWidget(self.ra_value, 1, 1, 1, 1)
        self.channelB_value = QtWidgets.QLabel(self.data_display_group)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 82, 82))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 82, 82))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 82, 82))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 82, 82))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.channelB_value.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.channelB_value.setFont(font)
        self.channelB_value.setScaledContents(False)
        self.channelB_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.channelB_value.setObjectName("channelB_value")
        self.gridLayout_2.addWidget(self.channelB_value, 5, 1, 1, 1)
        self.ra_label = QtWidgets.QLabel(self.data_display_group)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.ra_label.setFont(font)
        self.ra_label.setObjectName("ra_label")
        self.gridLayout_2.addWidget(self.ra_label, 1, 0, 1, 1)
        self.gridLayout_7.addWidget(self.data_display_group, 1, 0, 1, 1)
        self.stripchart_control_group = QtWidgets.QGroupBox(self.main_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stripchart_control_group.sizePolicy().hasHeightForWidth())
        self.stripchart_control_group.setSizePolicy(sizePolicy)
        self.stripchart_control_group.setObjectName("stripchart_control_group")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.stripchart_control_group)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_2 = QtWidgets.QFrame(self.stripchart_control_group)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.stripchart_faster_label = QtWidgets.QLabel(self.frame_2)
        self.stripchart_faster_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.stripchart_faster_label.setObjectName("stripchart_faster_label")
        self.gridLayout_3.addWidget(self.stripchart_faster_label, 0, 2, 1, 1)
        self.stripchart_speed_slider = QtWidgets.QSlider(self.frame_2)
        self.stripchart_speed_slider.setMaximum(6)
        self.stripchart_speed_slider.setProperty("value", 3)
        self.stripchart_speed_slider.setOrientation(QtCore.Qt.Horizontal)
        self.stripchart_speed_slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.stripchart_speed_slider.setTickInterval(1)
        self.stripchart_speed_slider.setObjectName("stripchart_speed_slider")
        self.gridLayout_3.addWidget(self.stripchart_speed_slider, 0, 1, 1, 1)
        self.stripchart_slower_label = QtWidgets.QLabel(self.frame_2)
        self.stripchart_slower_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.stripchart_slower_label.setObjectName("stripchart_slower_label")
        self.gridLayout_3.addWidget(self.stripchart_slower_label, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame_2, 0, 0, 1, 4)
        self.frame = QtWidgets.QFrame(self.stripchart_control_group)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chart_clear_button = QtWidgets.QPushButton(self.frame)
        self.chart_clear_button.setObjectName("chart_clear_button")
        self.horizontalLayout.addWidget(self.chart_clear_button)
        self.chart_legacy_button = QtWidgets.QPushButton(self.frame)
        self.chart_legacy_button.setObjectName("chart_legacy_button")
        self.horizontalLayout.addWidget(self.chart_legacy_button)
        self.gridLayout_4.addWidget(self.frame, 3, 0, 1, 4)
        self.gridLayout_7.addWidget(self.stripchart_control_group, 2, 0, 1, 1)
        self.message_group_box = QtWidgets.QGroupBox(self.main_frame)
        self.message_group_box.setObjectName("message_group_box")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.message_group_box)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.refresh_label = QtWidgets.QLabel(self.message_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_label.sizePolicy().hasHeightForWidth())
        self.refresh_label.setSizePolicy(sizePolicy)
        self.refresh_label.setObjectName("refresh_label")
        self.gridLayout_5.addWidget(self.refresh_label, 2, 0, 1, 1)
        self.refresh_value = QtWidgets.QLabel(self.message_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_value.sizePolicy().hasHeightForWidth())
        self.refresh_value.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        font.setBold(True)
        font.setWeight(75)
        self.refresh_value.setFont(font)
        self.refresh_value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.refresh_value.setObjectName("refresh_value")
        self.gridLayout_5.addWidget(self.refresh_value, 2, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.message_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        self.progressBar.setFont(font)
        self.progressBar.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_5.addWidget(self.progressBar, 1, 0, 1, 2)
        self.message_label = QtWidgets.QLabel(self.message_group_box)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.message_label.setFont(font)
        self.message_label.setObjectName("message_label")
        self.gridLayout_5.addWidget(self.message_label, 0, 0, 1, 2)
        self.gridLayout_7.addWidget(self.message_group_box, 0, 0, 1, 1)
        self.console_background = QtWidgets.QFrame(self.main_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.console_background.sizePolicy().hasHeightForWidth())
        self.console_background.setSizePolicy(sizePolicy)
        self.console_background.setObjectName("console_background")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.console_background)
        self.gridLayout_11.setContentsMargins(0, -1, 0, -1)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.console_inner_frame_2 = QtWidgets.QFrame(self.console_background)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.console_inner_frame_2.sizePolicy().hasHeightForWidth())
        self.console_inner_frame_2.setSizePolicy(sizePolicy)
        self.console_inner_frame_2.setStyleSheet("background: black; border-radius: 5px")
        self.console_inner_frame_2.setObjectName("console_inner_frame_2")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.console_inner_frame_2)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.console_label = QtWidgets.QLabel(self.console_inner_frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.console_label.sizePolicy().hasHeightForWidth())
        self.console_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Iosevka Aile")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.console_label.setFont(font)
        self.console_label.setStyleSheet("color: #0f0")
        self.console_label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.console_label.setObjectName("console_label")
        self.gridLayout_12.addWidget(self.console_label, 0, 0, 1, 1)
        self.dec_view = QtWidgets.QGraphicsView(self.console_inner_frame_2)
        self.dec_view.setStyleSheet("background: transparent")
        self.dec_view.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.dec_view.setFrameShadow(QtWidgets.QFrame.Plain)
        self.dec_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.dec_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.dec_view.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.TextAntialiasing)
        self.dec_view.setObjectName("dec_view")
        self.gridLayout_12.addWidget(self.dec_view, 0, 1, 1, 1)
        self.gridLayout_11.addWidget(self.console_inner_frame_2, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.console_background, 3, 0, 1, 1)
        self.output_frame = QtWidgets.QFrame(self.main_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_frame.sizePolicy().hasHeightForWidth())
        self.output_frame.setSizePolicy(sizePolicy)
        self.output_frame.setObjectName("output_frame")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.output_frame)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.stripchart = QChartView(self.output_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stripchart.sizePolicy().hasHeightForWidth())
        self.stripchart.setSizePolicy(sizePolicy)
        self.stripchart.setMinimumSize(QtCore.QSize(100, 0))
        self.stripchart.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.stripchart.setFrameShadow(QtWidgets.QFrame.Plain)
        self.stripchart.setObjectName("stripchart")
        self.gridLayout_10.addWidget(self.stripchart, 0, 0, 2, 2)
        self.gridLayout_7.addWidget(self.output_frame, 0, 1, 4, 1)
        self.gridLayout.addWidget(self.main_frame, 0, 0, 1, 1)
        self.testing_frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.testing_frame.sizePolicy().hasHeightForWidth())
        self.testing_frame.setSizePolicy(sizePolicy)
        self.testing_frame.setMinimumSize(QtCore.QSize(0, 180))
        self.testing_frame.setObjectName("testing_frame")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.testing_frame)
        self.gridLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.dec_group_box = QtWidgets.QGroupBox(self.testing_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dec_group_box.sizePolicy().hasHeightForWidth())
        self.dec_group_box.setSizePolicy(sizePolicy)
        self.dec_group_box.setObjectName("dec_group_box")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.dec_group_box)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.declination_slider = QtWidgets.QSlider(self.dec_group_box)
        self.declination_slider.setMinimum(0)
        self.declination_slider.setMaximum(100)
        self.declination_slider.setSingleStep(1)
        self.declination_slider.setTickInterval(20)
        self.declination_slider.setObjectName("declination_slider")
        self.gridLayout_9.addWidget(self.declination_slider, 0, 0, 2, 1)
        self.north_label = QtWidgets.QLabel(self.dec_group_box)
        self.north_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.north_label.setObjectName("north_label")
        self.gridLayout_9.addWidget(self.north_label, 0, 1, 1, 1)
        self.south_label = QtWidgets.QLabel(self.dec_group_box)
        self.south_label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.south_label.setObjectName("south_label")
        self.gridLayout_9.addWidget(self.south_label, 1, 1, 1, 1)
        self.gridLayout_8.addWidget(self.dec_group_box, 0, 1, 1, 1)
        self.signal_group_box = QtWidgets.QGroupBox(self.testing_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.signal_group_box.sizePolicy().hasHeightForWidth())
        self.signal_group_box.setSizePolicy(sizePolicy)
        self.signal_group_box.setObjectName("signal_group_box")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.signal_group_box)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.variance_dial = QtWidgets.QDial(self.signal_group_box)
        self.variance_dial.setMinimum(0)
        self.variance_dial.setMaximum(16)
        self.variance_dial.setPageStep(4)
        self.variance_dial.setProperty("value", 4)
        self.variance_dial.setWrapping(False)
        self.variance_dial.setNotchTarget(1.0)
        self.variance_dial.setNotchesVisible(True)
        self.variance_dial.setObjectName("variance_dial")
        self.gridLayout_6.addWidget(self.variance_dial, 1, 0, 1, 1)
        self.variance_label = QtWidgets.QLabel(self.signal_group_box)
        self.variance_label.setAlignment(QtCore.Qt.AlignCenter)
        self.variance_label.setObjectName("variance_label")
        self.gridLayout_6.addWidget(self.variance_label, 3, 0, 1, 1)
        self.noise_label = QtWidgets.QLabel(self.signal_group_box)
        self.noise_label.setAlignment(QtCore.Qt.AlignCenter)
        self.noise_label.setObjectName("noise_label")
        self.gridLayout_6.addWidget(self.noise_label, 3, 3, 1, 1)
        self.polarization_label = QtWidgets.QLabel(self.signal_group_box)
        self.polarization_label.setAlignment(QtCore.Qt.AlignCenter)
        self.polarization_label.setObjectName("polarization_label")
        self.gridLayout_6.addWidget(self.polarization_label, 3, 2, 1, 1)
        self.polarization_dial = QtWidgets.QDial(self.signal_group_box)
        self.polarization_dial.setMinimum(0)
        self.polarization_dial.setMaximum(16)
        self.polarization_dial.setPageStep(4)
        self.polarization_dial.setProperty("value", 4)
        self.polarization_dial.setWrapping(False)
        self.polarization_dial.setNotchTarget(1.0)
        self.polarization_dial.setNotchesVisible(True)
        self.polarization_dial.setObjectName("polarization_dial")
        self.gridLayout_6.addWidget(self.polarization_dial, 1, 2, 1, 1)
        self.noise_dial = QtWidgets.QDial(self.signal_group_box)
        self.noise_dial.setMinimum(0)
        self.noise_dial.setMaximum(16)
        self.noise_dial.setPageStep(4)
        self.noise_dial.setProperty("value", 4)
        self.noise_dial.setWrapping(False)
        self.noise_dial.setNotchTarget(1.0)
        self.noise_dial.setNotchesVisible(True)
        self.noise_dial.setObjectName("noise_dial")
        self.gridLayout_6.addWidget(self.noise_dial, 1, 3, 1, 1)
        self.calibration_check_box = QtWidgets.QCheckBox(self.signal_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calibration_check_box.sizePolicy().hasHeightForWidth())
        self.calibration_check_box.setSizePolicy(sizePolicy)
        self.calibration_check_box.setObjectName("calibration_check_box")
        self.gridLayout_6.addWidget(self.calibration_check_box, 1, 4, 3, 1)
        self.gridLayout_8.addWidget(self.signal_group_box, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.testing_frame, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menuCalibration = QtWidgets.QMenu(self.menubar)
        self.menuCalibration.setObjectName("menuCalibration")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuMode = QtWidgets.QMenu(self.menubar)
        self.menuMode.setObjectName("menuMode")
        self.menuObservation = QtWidgets.QMenu(self.menubar)
        self.menuObservation.setObjectName("menuObservation")
        MainWindow.setMenuBar(self.menubar)
        self.actionRA = QtWidgets.QAction(MainWindow)
        self.actionRA.setObjectName("actionRA")
        self.actionDec = QtWidgets.QAction(MainWindow)
        self.actionDec.setObjectName("actionDec")
        self.actionSurvey = QtWidgets.QAction(MainWindow)
        self.actionSurvey.setObjectName("actionSurvey")
        self.actionInfo = QtWidgets.QAction(MainWindow)
        self.actionInfo.setObjectName("actionInfo")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setEnabled(False)
        self.actionHelp.setObjectName("actionHelp")
        self.actionScan = QtWidgets.QAction(MainWindow)
        self.actionScan.setObjectName("actionScan")
        self.actionSpectrum = QtWidgets.QAction(MainWindow)
        self.actionSpectrum.setObjectName("actionSpectrum")
        self.actionNormal = QtWidgets.QAction(MainWindow)
        self.actionNormal.setCheckable(True)
        self.actionNormal.setObjectName("actionNormal")
        self.actionTesting = QtWidgets.QAction(MainWindow)
        self.actionTesting.setCheckable(True)
        self.actionTesting.setObjectName("actionTesting")
        self.actionLegacy = QtWidgets.QAction(MainWindow)
        self.actionLegacy.setCheckable(True)
        self.actionLegacy.setObjectName("actionLegacy")
        self.actionGetInfo = QtWidgets.QAction(MainWindow)
        self.actionGetInfo.setEnabled(False)
        self.actionGetInfo.setObjectName("actionGetInfo")
        self.menuCalibration.addAction(self.actionRA)
        self.menuCalibration.addAction(self.actionDec)
        self.menuFile.addAction(self.actionHelp)
        self.menuFile.addAction(self.actionInfo)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuMode.addAction(self.actionNormal)
        self.menuMode.addAction(self.actionLegacy)
        self.menuMode.addAction(self.actionTesting)
        self.menuObservation.addAction(self.actionScan)
        self.menuObservation.addAction(self.actionSurvey)
        self.menuObservation.addAction(self.actionSpectrum)
        self.menuObservation.addSeparator()
        self.menuObservation.addAction(self.actionGetInfo)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuObservation.menuAction())
        self.menubar.addAction(self.menuCalibration.menuAction())
        self.menubar.addAction(self.menuMode.menuAction())

        self.retranslateUi(MainWindow)
        self.actionQuit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.data_display_group.setTitle(_translate("MainWindow", "Data"))
        self.dec_label.setText(_translate("MainWindow", "Declination:"))
        self.channelB_label.setText(_translate("MainWindow", "Channel B:"))
        self.dec_value.setText(_translate("MainWindow", "0.0000deg"))
        self.channelA_value.setText(_translate("MainWindow", "0.0000V"))
        self.channelA_label.setText(_translate("MainWindow", "Channel A:"))
        self.ra_value.setText(_translate("MainWindow", "00:00:00"))
        self.channelB_value.setText(_translate("MainWindow", "0.0000V"))
        self.ra_label.setText(_translate("MainWindow", "Right Ascension:"))
        self.stripchart_control_group.setTitle(_translate("MainWindow", "Strip chart"))
        self.stripchart_faster_label.setText(_translate("MainWindow", "Faster"))
        self.stripchart_slower_label.setText(_translate("MainWindow", "Slower"))
        self.chart_clear_button.setText(_translate("MainWindow", "Clear Chart"))
        self.chart_legacy_button.setText(_translate("MainWindow", "Legacy Mode"))
        self.message_group_box.setTitle(_translate("MainWindow", "Message"))
        self.refresh_label.setText(_translate("MainWindow", "Refresh rate:"))
        self.refresh_value.setText(_translate("MainWindow", "0.00Hz"))
        self.message_label.setText(_translate("MainWindow", "..."))
        self.console_label.setText(_translate("MainWindow", ">>>"))
        self.dec_group_box.setTitle(_translate("MainWindow", "Declination"))
        self.north_label.setText(_translate("MainWindow", "North"))
        self.south_label.setText(_translate("MainWindow", "South"))
        self.signal_group_box.setTitle(_translate("MainWindow", "Signal"))
        self.variance_label.setText(_translate("MainWindow", "Variance"))
        self.noise_label.setText(_translate("MainWindow", "Interference"))
        self.polarization_label.setText(_translate("MainWindow", "Polarization"))
        self.calibration_check_box.setText(_translate("MainWindow", "Calibration"))
        self.menuCalibration.setTitle(_translate("MainWindow", "Calibrate"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuMode.setTitle(_translate("MainWindow", "Mode"))
        self.menuObservation.setTitle(_translate("MainWindow", "Observation"))
        self.actionRA.setText(_translate("MainWindow", "RA..."))
        self.actionDec.setText(_translate("MainWindow", "Dec..."))
        self.actionSurvey.setText(_translate("MainWindow", "New Survey..."))
        self.actionSurvey.setShortcut(_translate("MainWindow", "Ctrl+2"))
        self.actionInfo.setText(_translate("MainWindow", "Credits..."))
        self.actionQuit.setText(_translate("MainWindow", "Exit"))
        self.actionHelp.setText(_translate("MainWindow", "Help..."))
        self.actionScan.setText(_translate("MainWindow", "New Scan..."))
        self.actionScan.setShortcut(_translate("MainWindow", "Ctrl+1"))
        self.actionSpectrum.setText(_translate("MainWindow", "New Spectrum..."))
        self.actionSpectrum.setShortcut(_translate("MainWindow", "Ctrl+3"))
        self.actionNormal.setText(_translate("MainWindow", "Normal"))
        self.actionNormal.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionTesting.setText(_translate("MainWindow", "Testing"))
        self.actionTesting.setShortcut(_translate("MainWindow", "Ctrl+T"))
        self.actionLegacy.setText(_translate("MainWindow", "Legacy"))
        self.actionLegacy.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionGetInfo.setText(_translate("MainWindow", "Get Info..."))
from PyQt5.QtChart import QChartView

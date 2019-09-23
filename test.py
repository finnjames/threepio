import PyQt5.QtWidgets as qt
import sys

class GroupBox(qt.QWidget):

    def __init__(self):
        qt.QWidget.__init__(self)

        self.setWindowTitle("GroupBox")
        layout = qt.QGridLayout()
        self.setLayout(layout)

        stripchart_speed_group = qt.QGroupBox("Stripchart speed")
        layout.addWidget(stripchart_speed_group)
        
        vbox = qt.QVBoxLayout()
        stripchart_speed_group.setLayout(vbox)

        radiobutton = qt.QRadioButton("Faster")
        vbox.addWidget(radiobutton)
        
        radiobutton = qt.QRadioButton("Default")
        vbox.addWidget(radiobutton)

        radiobutton = qt.QRadioButton("Slower")
        vbox.addWidget(radiobutton)
        
        
app = qt.QApplication(sys.argv)
app.setStyle("Fusion")
screen = GroupBox()
screen.show()
sys.exit(app.exec_())
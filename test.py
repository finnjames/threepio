from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("GroupBox")
        layout = QVBoxLayout()

        widget = QLabel("hello world")
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.setCentralWidget(widget)

        
        
app = QApplication(sys.argv)

app.setStyle("Fusion")

window = MainWindow()
window.show()

sys.exit(app.exec_())
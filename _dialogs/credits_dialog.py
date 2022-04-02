from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from layouts import credits_ui


class CreditsDialog(QDialog):
    """Credits dialog window"""

    def __init__(self):
        QWidget.__init__(self)

        self.ui = credits_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.label.setPixmap(QPixmap("assets/c3po.png"))

        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

from PyQt5 import QtWidgets, QtCore
from layouts import credits_ui


class CreditsDialog(QtWidgets.QDialog):
    """Credits dialogue window"""

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = credits_ui.Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint
        )

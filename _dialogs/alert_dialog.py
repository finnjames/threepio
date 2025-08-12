"""dialogue box for alerting the user about something"""

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from layouts import alert_ui


class AlertDialog(QDialog):
    """Alert dialogue window"""

    def __init__(self, alert: str, button_text: str):
        QWidget.__init__(self)
        self.ui = alert_ui.Ui_Dialog()
        # self.setModal(False)
        self.ui.setupUi(self)

        # Hide the close/minimize/fullscreen buttons and make window always on top
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowTitleHint
            | Qt.CustomizeWindowHint
            | Qt.WindowStaysOnTopHint
        )

        self.ui.alert.setText(alert)
        self.ui.close_button.setText(button_text)

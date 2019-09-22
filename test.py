import PyQt5.QtWidgets as qt

app = qt.QApplication([])

label = qt.QLabel('Hello World!')

label.show() # show the label

app.exec_() # run the app
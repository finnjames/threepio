import PyQt5.QtWidgets as qt

app = qt.QApplication([])
window = qt.QWidget()
layout = qt.QVBoxLayout()

layout.addWidget(qt.QPushButton('Top'))

layout.addWidget(qt.QPushButton('Right'))

window.setLayout(layout)

app.setStyle('Fusion')

window.show()

app.exec_()

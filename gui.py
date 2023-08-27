import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from send_email import *


def button_click():
    send_email(joke)
    label.setText(f"You've sent a joke to {EMAIL}")


app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Simple PyQt GUI")
window.setGeometry(100, 100, 300, 200)

label = QLabel("Hello, PyQt!", parent=window)
label.move(100, 50)

button = QPushButton("Click Me to send a joke!", parent=window)
button.move(100, 100)
button.resize(250, 100)
button.clicked.connect(button_click)

window.show()

sys.exit(app.exec_())

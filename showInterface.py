import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMainWindow
from Interface import Ui_MainWindow

app = QApplication(sys.argv)

class MainWindow(QMainWindow) :
    def __init__(self) :
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.btn_equipes.clicked.connect(self.widget_equipe)

    def widget_equipe(self):
        self.stackedWidget.setCurrentWidget(self.widget_home)

window = MainWindow()
window.setWindowTitle("Ma première interface PyQt6")
window.show()
app.exec()
sys.exit()

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMainWindow

app = QApplication(sys.argv)

class MainWindow(QMainWindow) :
    def __init__(self) :
        super().__init__()
        # Initialisation d'un objet avec la classe créée avec QT Designer
        self.ui = Ui_Form()
        self.ui.setupUi(self)

window = MainWindow()
window.setWindowTitle("Ma première interface PyQt6")
window.setGeometry(200, 200, 400, 200)
window.show()
app.exec()
sys.exit()

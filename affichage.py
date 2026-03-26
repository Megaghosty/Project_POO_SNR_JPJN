import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

app = QApplication(sys.argv)

class FenetrePrincipale(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Initialisation d'un label de resultat
        self.labelResultat = QLabel("...",self)
        self.labelResultat.move(100,115)
        # Initialisation d'un label du nombre 1
        self.labelNombre1 = QLabel("Nombre 1",self)
        self.labelNombre1.move(30,10)
        # Initialisation d'un label du nombre 2
        self.labelNombre2 = QLabel("Nombre 2",self)
        self.labelNombre2.move(30,40)
        # Initialisation d'un lineEdit du nombre 1
        self.lineEditNombre1 = QLineEdit("",self)
        self.lineEditNombre1.move(100,10)
        # Initialisation d'un lineEdit du nombre 2
        self.lineEditNombre2 = QLineEdit("",self)
        self.lineEditNombre2.move(100,40)
        # Initialisation d'un boutton pour le calcule de la somme
        self.bouttonValidation = QPushButton("Calculer la somme",self)
        # Relier l'appuie du boutton à la méthode calculer()
        self.bouttonValidation.clicked.connect(self.calculer)
        self.bouttonValidation.move(80,75)

    def calculer(self):
        # Récupération des valeurs
        n1 = int(self.lineEditNombre1.text())
        n2 = int(self.lineEditNombre2.text())
        # Modification du texte de resultat
        self.labelResultat.setText(f"La somme de {n1} + {n2} est {n1+n2}")
        # Ajustement de la taille du label au texte
        self.labelResultat.adjustSize()

window = FenetrePrincipale()
window.setWindowTitle("Ma première interface PyQt6")
window.setGeometry(200, 200, 400, 200)
window.show()
app.exec()
sys.exit()

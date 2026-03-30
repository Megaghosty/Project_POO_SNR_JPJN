import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

app = QApplication(sys.argv)

class MainWindow(QMainWindow) :
    def __init__(self,nomLabo) :
        super().__init__()
        uic.loadUi("Interface.ui", self)

        # Affichage nom du Labo
        self.label_labo.setText(nomLabo)
        self.label_home.setText(self.label_home.text()+nomLabo)
        self.setWindowTitle("Gestion "+nomLabo)

        # Initialisation des boutons
        self.btn_equipes.clicked.connect(self.afficher_equipe)
        self.btn_publications.clicked.connect(self.afficher_publications)
        self.widget_equipes_btn_creer_chercheur.clicked.connect(self.afficher_creer_chercheur)
        self.widget_equipes_btn_ajout_chercheur.clicked.connect(self.afficher_ajout_chercheur)
        self.widget_creer_chercheur_btn_creer.clicked.connect(self.creer_chercheur)

        # Page d'affichage
        self.stackedWidget.setCurrentWidget(self.widget_home)

    # Méthodes d'affichage
    def afficher_equipe(self):
        self.stackedWidget.setCurrentWidget(self.widget_equipes)
    def afficher_publications(self):
        self.stackedWidget.setCurrentWidget(self.widget_publications)
    def afficher_creer_chercheur(self):
        self.stackedWidget.setCurrentWidget(self.widget_creer_chercheur)
    def afficher_ajout_chercheur(self):
        self.stackedWidget.setCurrentWidget(self.widget_ajouter_chercheur)

    # Méthodes gestion BDD
    def creer_chercheur(self):
        nom = self.widget_creer_chercheur_lineEdit_nom.text()
        prenom = self.widget_creer_chercheur_lineEdit_prenom.text()
        sexe = self.widget_creer_chercheur_comboBox_sexe.currentText()
        email = self.widget_creer_chercheur_lineEdit_email.text()
        telephone = self.widget_creer_chercheur_lineEdit_telephone.text()
        userName = self.widget_creer_chercheur_lineEdit_nom_utilisateur.text()
        mdp = self.widget_creer_chercheur_lineEdit_mdp.text()
        specialite = self.widget_creer_chercheur_lineEdit_specialite.text()
        recherche = self.widget_creer_chercheur_lineEdit_recherche.text()
        grade = self.widget_creer_chercheur_comboBox_grade.currentText()
        naissance = self.widget_creer_chercheur_dateEdit_naissance.dateTime()
        print(nom,prenom,sexe,email,telephone,userName,mdp,specialite,recherche,grade,naissance)

window = MainWindow("IETR")
window.show()
app.exec()
sys.exit()

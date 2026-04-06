import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from controllers.auth_controller import AuthController
from controllers.equipes_controller import EquipesController
from controllers.chercheurs_controller import ChercheursController
from controllers.publications_controller import PublicationsController

# Configuration de l'application
app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    """
    Fenêtre principale de l'application.
    Gère le chargement de l'interface et l'initialisation des contrôleurs.
    """
    def __init__(self, nomLabo):
        super().__init__()
        uic.loadUi("Interface.ui", self)

        # Cookie de session (stocke les infos de l'utilisateur connecté)
        self.utilisateur_connecte = None
        
        # Initialisation des contrôleurs annexes
        self.auth_ctrl = AuthController(self)
        self.equipes_ctrl = EquipesController(self)
        self.chercheurs_ctrl = ChercheursController(self)
        self.pub_ctrl = PublicationsController(self)

        # Affichage nom du Labo
        self.label_labo.setText(nomLabo)
        self.label_home.setText(self.label_home.text() + nomLabo)
        self.setWindowTitle("Gestion " + nomLabo)

        # Initialisation des boutons -> Redirection vers les contrôleurs
        self.btn_equipes.clicked.connect(self.equipes_ctrl.afficher_equipe)
        self.btn_publications.clicked.connect(self.pub_ctrl.afficher_publications)
        self.btn_personnel.clicked.connect(self.chercheurs_ctrl.afficher_personnel)
        
        self.widget_equipes_btn_creer_equipe.clicked.connect(self.equipes_ctrl.afficher_creer_equipe)
        self.widget_membre_equipe_btn_ajouter_membre.clicked.connect(self.chercheurs_ctrl.afficher_ajouter_chercheur)
        self.widget_equipes_btn_supprimer_chercheur.clicked.connect(self.equipes_ctrl.afficher_supprimer_chercheur_equipe)
        
        self.widget_personnel_btn_creer_chercheur.clicked.connect(self.chercheurs_ctrl.afficher_creer_chercheur)
        self.widget_personnel_btn_supprimer_chercheur.clicked.connect(self.chercheurs_ctrl.afficher_supprimer_chercheur)
        
        self.widget_creer_chercheur_btn_creer.clicked.connect(self.chercheurs_ctrl.creer_chercheur)
        self.widget_creer_equipes_btn_creer_equipe.clicked.connect(self.equipes_ctrl.creer_equipe)
        self.widget_memebres_equipe_btn_retour.clicked.connect(self.equipes_ctrl.afficher_equipe)

        self.widget_publication_btn_creer.clicked.connect(self.pub_ctrl.afficher_creer_publication)
        self.widget_creer_publication_btn_creer.clicked.connect(self.pub_ctrl.creer_publication)
        self.widget_afficher_publication_btn_retour.clicked.connect(self.pub_ctrl.afficher_publications)
        self.widget_publication_btn_afficher.clicked.connect(self.pub_ctrl.afficher_publication)
        self.widget_equipes_btn_membres.clicked.connect(self.equipes_ctrl.afficher_membres)
        
        self.btn_connection.clicked.connect(self.auth_ctrl.afficher_connection)
        self.widget_connection_btn_connection.clicked.connect(self.auth_ctrl.verification_connection)
        self.widget_ajouter_chercheur_btn_ajouter.clicked.connect(self.chercheurs_ctrl.ajouter_chercheur)
        self.btn_deconnection.clicked.connect(self.auth_ctrl.deconnexion)

        # ---------------------------------------------------------
        # CONFIGURATION DU MESSAGE D'ERREUR CACHÉ
        # ---------------------------------------------------------
        if hasattr(self, 'label_compteutilse'):
            self.label_compteutilse.setVisible(False)
            self.label_compteutilse.setStyleSheet("color: red; font-weight: bold;")

        # 🔒 ON APPLIQUE LES DROITS DÈS LE DÉMARRAGE (Tout sera caché par défaut)
        self.auth_ctrl.appliquer_droits()

        # Page d'affichage par défaut
        self.stackedWidget.setCurrentWidget(self.widget_home)

    def nettoyer_formulaire(self):
        """Réinitialise les champs de saisie pour la création d'équipe et personnel."""
        self.widget_creer_chercheur_lineEdit_nom.clear()
        self.widget_creer_chercheur_lineEdit_prenom.clear()
        self.widget_creer_chercheur_lineEdit_email.clear()
        self.widget_creer_chercheur_lineEdit_telephone.clear()
        self.widget_creer_chercheur_lineEdit_nom_utilisateur.clear()
        self.widget_creer_chercheur_lineEdit_mdp.clear()
        self.widget_creer_chercheur_lineEdit_confirmation_mdp.clear()
        self.widget_creer_chercheur_lineEdit_specialite.clear()
        self.widget_creer_chercheur_lineEdit_recherche.clear()
        self.widget_creer_chercheur_comboBox_sexe.setCurrentIndex(0)
        self.widget_creer_chercheur_comboBox_grade.setCurrentIndex(0)

        if hasattr(self, 'label_compteutilse'):
            self.label_compteutilse.setVisible(False)

        self.widget_creer_equipes_lineEdit_nom.clear()
        self.widget_creer_equipes_lineEdit_abreviation.clear()
        self.widget_creer_equipes_lineEdit_axe.clear()
        self.widget_creer_equipes_textEdit_description.clear()

if __name__ == "__main__":
    window = MainWindow("IETR")
    window.show()
    sys.exit(app.exec())
import sys
import sqlite3
import bcrypt
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from PyQt6.QtCore import QStandardItemModel

# Configuration de l'application
app = QApplication(sys.argv)

def connecter_bdd():
    """Établit une connexion avec le fichier SQLite."""
    try:
        # Assure-toi que le fichier bdd_converted.db est dans le même dossier
        connexion = sqlite3.connect('bdd_converted.db')
        # Permet d'accéder aux colonnes par leur nom : row['nom']
        connexion.row_factory = sqlite3.Row 
        return connexion
    except sqlite3.Error as e:
        print(f"❌ Erreur de connexion à SQLite : {e}")
        return None

class MainWindow(QMainWindow):
    def __init__(self, nomLabo):
        super().__init__()
        uic.loadUi("Interface.ui", self)
    
        # Affichage nom du Labo
        self.label_labo.setText(nomLabo)
        self.label_home.setText(self.label_home.text() + nomLabo)
        self.setWindowTitle("Gestion " + nomLabo)

        # Initialisation des boutons
        self.btn_equipes.clicked.connect(self.afficher_equipe)
        self.btn_publications.clicked.connect(self.afficher_publications)
        self.btn_personnel.clicked.connect(self.afficher_personnel)
        self.widget_equipes_btn_ajouter_chercheur.clicked.connect(self.afficher_ajouter_chercheur)
        self.widget_equipes_btn_supprimer_chercheur.clicked.connect(self.afficher_supprimer_chercheur_equipe)
        self.widget_personnel_btn_creer_chercheur.clicked.connect(self.afficher_creer_chercheur)
        self.widget_personnel_btn_supprimer_chercheur.clicked.connect(self.afficher_supprimer_chercheur)
        self.widget_creer_chercheur_btn_creer.clicked.connect(self.creer_chercheur)
        self.btn_connection.clicked.connect(self.afficher_connection)

        # Page d'affichage par défaut
        self.stackedWidget.setCurrentWidget(self.widget_home)

    # Méthodes d'affichage
    def afficher_connection(self):
        self.stackedWidget.setCurrentWidget(self.widget_connection)

    def afficher_personnel(self):
        self.stackedWidget.setCurrentWidget(self.widget_personnel)
        
    def afficher_equipe(self):
        self.stackedWidget.setCurrentWidget(self.widget_equipes)

    def afficher_publications(self):
        self.stackedWidget.setCurrentWidget(self.widget_publications)
        
    def afficher_creer_chercheur(self):
        self.stackedWidget.setCurrentWidget(self.widget_creer_chercheur)
        
    def afficher_supprimer_chercheur(self):
        pass
        
    def afficher_ajouter_chercheur(self):
        connection = connecter_bdd()
        if connection is None:
            return 

        cursor = None
        try:
            cursor = connection.cursor()

            sql = """SELECT * FROM equipe"""

            cursor.execute(sql)
            data = cursor.fetchall()
            for i in range(len(data)):
                model =  QStandardItemModel()
                d = dict(data[i])
                model.setStringList([d["nom_eq"],d["abreviation_eq"]])
                self.widget_ajouter_chercheur_listWidget_equipe.setModel(model)

        except sqlite3.Error as e:
            if connection:
                connection.rollback()
            print(f"❌ Erreur SQLite : {e}")

        finally:
            if connection:
                connection.close()
            self.stackedWidget.setCurrentWidget(self.widget_ajouter_chercheur)
        
    def afficher_supprimer_chercheur_equipe(self):
        pass

    # Méthodes gestion BDD
    def creer_chercheur(self):
        # Récupération des données
        nom = self.widget_creer_chercheur_lineEdit_nom.text()
        prenom = self.widget_creer_chercheur_lineEdit_prenom.text()
        sexe = self.widget_creer_chercheur_comboBox_sexe.currentText()
        email = self.widget_creer_chercheur_lineEdit_email.text()
        telephone = self.widget_creer_chercheur_lineEdit_telephone.text()
        userName = self.widget_creer_chercheur_lineEdit_nom_utilisateur.text()
        mdp = self.widget_creer_chercheur_lineEdit_mdp.text()
        confirmationMdp = self.widget_creer_chercheur_lineEdit_confirmation_mdp.text()
        specialite = self.widget_creer_chercheur_lineEdit_specialite.text()
        recherche = self.widget_creer_chercheur_lineEdit_recherche.text()
        grade = self.widget_creer_chercheur_comboBox_grade.currentText()
        
        # Gestion de la date
        naissance_qt = self.widget_creer_chercheur_dateEdit_naissance.dateTime()
        naissance_sql = naissance_qt.toString("yyyy-MM-dd")

        # Vérification des champs obligatoires
        if not nom or not prenom or not userName or not mdp:
            print("⚠️ Erreur : Veuillez remplir les champs obligatoires.")
            return

        # Vérification mot de passe
        if mdp != confirmationMdp:
            print("⚠️ Erreur : Les mots de passe ne correspondent pas.")
            return

        # Détermination du statut
        est_permanent = 1
        type_role = "Permanent"
        if any(x in grade for x in ["Stagiaire", "Doctorant", "Assistant"]):
            est_permanent = 0
            type_role = "Non-Permanent"

        connection = connecter_bdd()
        if connection is None:
            return 

        cursor = None
        try:
            cursor = connection.cursor()

            # Hachage sécurisé
            salt = bcrypt.gensalt()
            mdp_hashe = bcrypt.hashpw(mdp.encode('utf-8'), salt).decode('utf-8')

            # Requête SQLite (Note l'utilisation des '?' au lieu de '%s')
            sql = """
                INSERT INTO chercheur 
                (nom, prenom, sexe, email, telephone, user, pw, specialite, axe_recherche, grade, date_naissance, type_role, est_permanent, Equipe_idEquipe) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            valeurs = (nom, prenom, sexe, email, telephone, userName, mdp_hashe, specialite, recherche, grade, naissance_sql, type_role, est_permanent, None)

            cursor.execute(sql, valeurs)
            connection.commit()

            print(f"✅ Succès : {prenom} {nom} a été ajouté à la base SQLite !")

            # Nettoyage de l'interface
            self.nettoyer_formulaire()

        except sqlite3.Error as e:
            if connection:
                connection.rollback()
            print(f"❌ Erreur SQLite : {e}")

        finally:
            if connection:
                connection.close()

    def nettoyer_formulaire(self):
        """Réinitialise les champs du formulaire."""
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

# Lancement de l'application
if __name__ == "__main__":
    window = MainWindow("IETR")
    window.show()
    sys.exit(app.exec())
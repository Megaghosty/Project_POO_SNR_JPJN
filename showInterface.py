import sys
import mysql.connector
import bcrypt
from mysql.connector import Error
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

app = QApplication(sys.argv)

def connecter_bdd():
   
    try:
        connexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',       
            database='projet_poo' 
        )
        
        if connexion.is_connected():
           
            return connexion

    except Error as e:
        print(f"❌ Erreur de connexion à la base de données : {e}")
        return None



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
        self.btn_personnel.clicked.connect(self.afficher_personnel)
        self.widget_equipes_btn_ajouter_chercheur.clicked.connect(self.afficher_ajouter_chercheur)
        self.widget_equipes_btn_supprimer_chercheur.clicked.connect(self.afficher_supprimer_chercheur_equipe)
        self.widget_personnel_btn_creer_chercheur.clicked.connect(self.afficher_creer_chercheur)
        self.widget_personnel_btn_supprimer_chercheur.clicked.connect(self.afficher_supprimer_chercheur)
        self.widget_creer_chercheur_btn_creer.clicked.connect(self.creer_chercheur)

        # Page d'affichage
        self.stackedWidget.setCurrentWidget(self.widget_home)

    # Méthodes d'affichage
    def afficher_personnel(self):
        self.stackedWidget.setCurrentWidget(self.widget_personnel)
    def afficher_equipe(self):
        self.stackedWidget.setCurrentWidget(self.widget_equipes)
    def afficher_publications(self):
        self.stackedWidget.setCurrentWidget(self.widget_publications)
    def afficher_creer_chercheur(self):
        self.stackedWidget.setCurrentWidget(self.widget_creer_chercheur)
<<<<<<< HEAD

    def afficher_ajout_chercheur(self):
        self.stackedWidget.setCurrentWidget(self.widget_ajouter_chercheur)
=======
    def afficher_supprimer_chercheur(self):
        #self.stackedWidget.setCurrentWidget(self.widget_supprimer_chercheur)
        pass
    def afficher_ajouter_chercheur(self):
        pass
    def afficher_supprimer_chercheur_equipe(self):
        pass
>>>>>>> 3ee1f94955b30ff6b479f856231c1d89b7b94642

    # Méthodes gestion BDD
    def creer_chercheur(self):
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
<<<<<<< HEAD
        
        naissance_qt = self.widget_creer_chercheur_dateEdit_naissance.dateTime()
        naissance_sql = naissance_qt.toString("yyyy-MM-dd")

        if not nom or not prenom or not userName or not mdp:
            print("⚠️ Erreur : Veuillez remplir les champs obligatoires (Nom, Prénom, Utilisateur, Mot de passe).")
            return

        est_permanent = 1
        type_role = "Permanent"
        if "Stagiaire" in grade or "Doctorant" in grade or "Assistant" in grade:
            est_permanent = 0
            type_role = "Non-Permanent"

        connection = connecter_bdd()

        if connection is None:
            print("❌ Erreur : Impossible de se connecter à la base de données.")
            return 

        cursor = None
        try:
            cursor = connection.cursor()

            salt = bcrypt.gensalt()
            mdp_hashe = bcrypt.hashpw(mdp.encode('utf-8'), salt).decode('utf-8')

            sql = """
                INSERT INTO chercheur 
                (nom, prenom, sexe, email, telephone, user, pw, specialite, axe_recherche, grade, date_naissance, type_role, est_permanent, Equipe_idEquipe) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valeurs = (nom, prenom, sexe, email, telephone, userName, mdp_hashe, specialite, recherche, grade, naissance_sql, type_role, est_permanent, None)

            cursor.execute(sql, valeurs)
            connection.commit()

            print(f"✅ Succès : Le chercheur {prenom} {nom} a été ajouté avec succès !")

            self.widget_creer_chercheur_lineEdit_nom.clear()
            self.widget_creer_chercheur_lineEdit_prenom.clear()
            self.widget_creer_chercheur_lineEdit_email.clear()
            self.widget_creer_chercheur_lineEdit_telephone.clear()
            self.widget_creer_chercheur_lineEdit_nom_utilisateur.clear()
            self.widget_creer_chercheur_lineEdit_mdp.clear()
            self.widget_creer_chercheur_lineEdit_specialite.clear()
            self.widget_creer_chercheur_lineEdit_recherche.clear()
            self.widget_creer_chercheur_comboBox_sexe.setCurrentIndex(0)
            self.widget_creer_chercheur_comboBox_grade.setCurrentIndex(0)

        except Error as e:
            connection.rollback()
            print(f"❌ Erreur SQL : Une erreur est survenue lors de l'insertion :\n{e}")

        finally:
            if cursor: cursor.close()
            if connection and connection.is_connected(): connection.close()

=======
        naissance = self.widget_creer_chercheur_dateEdit_naissance.dateTime()
        print(nom,prenom,sexe,email,telephone,userName,mdp,confirmationMdp,specialite,recherche,grade,naissance)
>>>>>>> 3ee1f94955b30ff6b479f856231c1d89b7b94642

window = MainWindow("IETR")
window.show()
app.exec()
sys.exit()

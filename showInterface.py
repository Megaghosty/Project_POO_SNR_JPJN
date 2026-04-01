import sys
import sqlite3
import bcrypt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
from PyQt6 import uic

# IMPORTATION DE VOTRE NOUVEAU FICHIER
from database import connecter_bdd

app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self, nomLabo):
        super().__init__()
        uic.loadUi("Interface.ui", self)
    
        self.label_labo.setText(nomLabo)
        self.label_home.setText(self.label_home.text() + nomLabo)
        self.setWindowTitle("Gestion " + nomLabo)

        # Connexion des boutons
        self.btn_equipes.clicked.connect(self.afficher_equipe)
        self.btn_publications.clicked.connect(self.afficher_publications)
        self.btn_personnel.clicked.connect(self.afficher_personnel)
        self.widget_personnel_btn_creer_chercheur.clicked.connect(self.afficher_creer_chercheur)
        self.widget_creer_chercheur_btn_creer.clicked.connect(self.creer_chercheur)
        self.btn_connection.clicked.connect(self.afficher_connection)

        self.stackedWidget.setCurrentWidget(self.widget_home)


    # --- NOUVELLE MÉTHODE POUR AFFICHER LE PERSONNEL ---

    # Méthodes d'affichage
    def afficher_connection(self):
        self.stackedWidget.setCurrentWidget(self.widget_connection)


    def afficher_personnel(self):
        self.stackedWidget.setCurrentWidget(self.widget_personnel)
        
        connection = connecter_bdd()
        if connection is None: return

        try:
            cursor = connection.cursor()
            query = """
                SELECT nom, prenom, sexe, email, telephone, user, specialite, grade, date_naissance 
                FROM chercheur
            """
            cursor.execute(query)
            chercheurs = cursor.fetchall()

            # Vérification du widget tableau
            if hasattr(self, 'tableWidget_personnel'):
                self.tableWidget_personnel.setRowCount(0)
                
                # Configuration automatique des colonnes si besoin
                self.tableWidget_personnel.setColumnCount(9)
                self.tableWidget_personnel.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

                for row_idx, row_data in enumerate(chercheurs):
                    self.tableWidget_personnel.insertRow(row_idx)
                    for col_idx, value in enumerate(row_data):
                        item = QTableWidgetItem(str(value) if value is not None else "")
                        self.tableWidget_personnel.setItem(row_idx, col_idx, item)
            
            print(f"✅ {len(chercheurs)} chercheurs chargés dans l'interface.")

        except sqlite3.Error as e:
            print(f"❌ Erreur lors du chargement : {e}")
        finally:
            if connection: connection.close()

    # --- MÉTHODES D'AFFICHAGE ---
    def afficher_equipe(self):
        self.stackedWidget.setCurrentWidget(self.widget_equipes)

    def afficher_publications(self):
        self.stackedWidget.setCurrentWidget(self.widget_publications)
        
    def afficher_creer_chercheur(self):
        self.stackedWidget.setCurrentWidget(self.widget_creer_chercheur)

    # --- GESTION BDD ---
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
        
        naissance_qt = self.widget_creer_chercheur_dateEdit_naissance.dateTime()
        naissance_sql = naissance_qt.toString("yyyy-MM-dd")

        if not nom or not prenom or not userName or not mdp:
            print("⚠️ Erreur : Veuillez remplir les champs obligatoires.")
            return

        if mdp != confirmationMdp:
            print("⚠️ Erreur : Les mots de passe ne correspondent pas.")
            return

        est_permanent = 1
        type_role = "Permanent"
        if any(x in grade for x in ["Stagiaire", "Doctorant", "Assistant"]):
            est_permanent = 0
            type_role = "Non-Permanent"

        connection = connecter_bdd()
        if connection is None: return 

        try:
            cursor = connection.cursor()
            salt = bcrypt.gensalt()
            mdp_hashe = bcrypt.hashpw(mdp.encode('utf-8'), salt).decode('utf-8')

            sql = """
                INSERT INTO chercheur 
                (nom, prenom, sexe, email, telephone, user, pw, specialite, axe_recherche, grade, date_naissance, type_role, est_permanent, Equipe_idEquipe) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            valeurs = (nom, prenom, sexe, email, telephone, userName, mdp_hashe, specialite, recherche, grade, naissance_sql, type_role, est_permanent, None)

            cursor.execute(sql, valeurs)
            connection.commit()
            print(f"✅ Succès : {prenom} {nom} ajouté !")
            self.nettoyer_formulaire()

        except sqlite3.Error as e:
            if connection: connection.rollback()
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection: connection.close()

    def nettoyer_formulaire(self):
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

if __name__ == "__main__":
    window = MainWindow("IETR")
    window.show()
    sys.exit(app.exec())
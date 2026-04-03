import sys
import sqlite3
import bcrypt
import datetime as dt
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from connexion_bdd import connecter_bdd

# Configuration de l'application
app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self, nomLabo):
        super().__init__()
        uic.loadUi("Interface.ui", self)

        # Cookie de session (stocke les infos de l'utilisateur connecté)
        self.utilisateur_connecte = None
        
        # Affichage nom du Labo
        self.label_labo.setText(nomLabo)
        self.label_home.setText(self.label_home.text() + nomLabo)
        self.setWindowTitle("Gestion " + nomLabo)

        # Initialisation des boutons
        self.btn_equipes.clicked.connect(self.afficher_equipe)
        self.btn_publications.clicked.connect(self.afficher_publications)
        self.btn_personnel.clicked.connect(self.afficher_personnel)
        
        self.widget_equipes_btn_creer_equipe.clicked.connect(self.afficher_creer_equipe)
        self.widget_equipes_btn_ajouter_chercheur.clicked.connect(self.afficher_ajouter_chercheur)
        self.widget_equipes_btn_supprimer_chercheur.clicked.connect(self.afficher_supprimer_chercheur_equipe)
        
        self.widget_personnel_btn_creer_chercheur.clicked.connect(self.afficher_creer_chercheur)
        self.widget_personnel_btn_supprimer_chercheur.clicked.connect(self.afficher_supprimer_chercheur)
        
        self.widget_creer_chercheur_btn_creer.clicked.connect(self.creer_chercheur)
        self.widget_creer_equipes_btn_creer_equipe.clicked.connect(self.creer_equipe)
        
        self.btn_connection.clicked.connect(self.afficher_connection)
        self.widget_connection_btn_connection.clicked.connect(self.verification_connection)

        # 🔒 ON APPLIQUE LES DROITS DÈS LE DÉMARRAGE (Tout sera caché par défaut)
        self.appliquer_droits()

        # Page d'affichage par défaut
        self.stackedWidget.setCurrentWidget(self.widget_home)

    # ==========================================
    # MÉTHODES DE CONNEXION ET SÉCURITÉ
    # ==========================================
    
    def afficher_connection(self):
        self.stackedWidget.setCurrentWidget(self.widget_connection)

    def verification_connection(self):
        username = self.widget_connection_lineEdit_nom.text()
        password = self.widget_connection_lineEdit_mdp.text()

        if not username or not password:
            print("⚠️ Veuillez remplir tous les champs.")
            return

        connection = connecter_bdd()
        if connection is None:
            return 

        try: 
            cursor = connection.cursor()
            query = "SELECT idChercheur, nom, prenom, type_role, grade, pw FROM chercheur WHERE user = ?"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result:
                hash_stocke = result['pw']
                
                if bcrypt.checkpw(password.encode('utf-8'), hash_stocke.encode('utf-8')):
                    
                    # 🍪 CRÉATION DU "COOKIE" DE SESSION
                    self.utilisateur_connecte = {
                        "id": result['idChercheur'],
                        "nom": result['nom'],
                        "prenom": result['prenom'],
                        "role": result['type_role'],
                        "grade": result['grade']
                    }
                    
                    print(f"✅ Connexion réussie ! Bienvenue {self.utilisateur_connecte['prenom']}.")
                    print(f"   - Rôle : {self.utilisateur_connecte['role']}")
                    
                    # 🔒 On met à jour les droits d'affichage après connexion !
                    self.appliquer_droits()

                    self.stackedWidget.setCurrentWidget(self.widget_home)
                    self.widget_connection_lineEdit_nom.clear()
                    self.widget_connection_lineEdit_mdp.clear()
                else:
                    print("❌ Mot de passe incorrect.")
            else:
                print("❌ Nom d'utilisateur introuvable.")

        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()

    def appliquer_droits(self):
        """Affiche ou masque les boutons selon le profil de l'utilisateur."""
        
        # 1. Si personne n'est connecté, on bloque tout d'office
        if self.utilisateur_connecte is None:
            est_admin = False
            peut_gerer_personnel_equipes = False
            peut_gerer_publications = False
            
        # 2. Sinon, on vérifie les rôles normalement
        else:
            role = self.utilisateur_connecte['role']
            grade = self.utilisateur_connecte['grade']

            est_admin = (role == "Administrateur" or grade == "Super-Admin")
            est_stagiaire = any(mot in grade for mot in ["Stagiaire", "Doctorant", "Assistant"])
            
            peut_gerer_personnel_equipes = est_admin
            
            if est_admin:
                peut_gerer_publications = True
            elif est_stagiaire:
                peut_gerer_publications = False
            else:
                # Chercheur Permanent
                peut_gerer_publications = True

        # --- APPLICATION À L'INTERFACE ---
        
        # Droits sur le personnel
        self.widget_personnel_btn_creer_chercheur.setVisible(peut_gerer_personnel_equipes)
        self.widget_personnel_btn_supprimer_chercheur.setVisible(peut_gerer_personnel_equipes)
        
        # Droits sur les équipes
        self.widget_equipes_btn_creer_equipe.setVisible(peut_gerer_personnel_equipes)
        self.widget_equipes_btn_ajouter_chercheur.setVisible(peut_gerer_personnel_equipes)
        self.widget_equipes_btn_supprimer_chercheur.setVisible(peut_gerer_personnel_equipes)

        # /!\ DÉCOMMETTRE ET CHANGER LE NOM DU BOUTON ICI POUR LES PUBLICATIONS :
        # if hasattr(self, 'nom_du_bouton_creer_publication'):
        #     self.nom_du_bouton_creer_publication.setVisible(peut_gerer_publications)
        
        print(f"🔐 Droits mis à jour : Admin={est_admin}, Créer Publi={peut_gerer_publications}")


    # ==========================================
    # MÉTHODES D'AFFICHAGE
    # ==========================================
    
    def afficher_personnel(self):
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()
            self.widget_personnel_listWidget_personnel.clear()
            sql = """SELECT * FROM chercheur"""
            cursor.execute(sql)
            data = cursor.fetchall()
            for i in range(len(data)):
                d = dict(data[i])
                self.widget_personnel_listWidget_personnel.addItem(str(d['nom'])+" | "+ str(d['prenom'])+" | "+ str(d['grade']))
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.stackedWidget.setCurrentWidget(self.widget_personnel)
        
    def afficher_creer_equipe(self):
        # Bloquer l'accès direct si l'utilisateur n'est pas Admin
        if not self.utilisateur_connecte or self.utilisateur_connecte['role'] != "Administrateur":
            return
        self.stackedWidget.setCurrentWidget(self.widget_creer_equipe)
                
    def afficher_equipe(self):
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()
            self.widget_equipes_listWidget_equipes.clear()
            sql = """SELECT * FROM equipe"""
            cursor.execute(sql)
            data = cursor.fetchall()
            for i in range(len(data)):
                d = dict(data[i])
                self.widget_equipes_listWidget_equipes.addItem(str(d['nom_eq'])+" | "+ str(d['abreviation_eq']))
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.stackedWidget.setCurrentWidget(self.widget_equipes)

    def afficher_publications(self):
        self.stackedWidget.setCurrentWidget(self.widget_publications)
        
    def afficher_creer_chercheur(self):
        # Sécurité
        if not self.utilisateur_connecte or self.utilisateur_connecte['role'] != "Administrateur":
            return
        self.stackedWidget.setCurrentWidget(self.widget_creer_chercheur)
        
    def afficher_supprimer_chercheur(self):
        pass
        
    def afficher_ajouter_chercheur(self):
        if not self.utilisateur_connecte or self.utilisateur_connecte['role'] != "Administrateur":
            return

        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()

            self.widget_ajouter_chercheur_listWidget_equipe.clear()
            self.widget_ajouter_chercheur_listWidget_chercheur.clear()

            sql = """SELECT * FROM equipe"""
            cursor.execute(sql)
            data = cursor.fetchall()
            for i in range(len(data)):
                d = dict(data[i])
                self.widget_ajouter_chercheur_listWidget_equipe.addItem(str(d['nom_eq'])+" | "+ str(d['abreviation_eq']))
            
            sql = """SELECT * FROM chercheur"""
            cursor.execute(sql)
            data = cursor.fetchall()
            for i in range(len(data)):
                d = dict(data[i])
                self.widget_ajouter_chercheur_listWidget_chercheur.addItem(str(d['nom'])+" | "+ str(d['prenom'])+" | "+ str(d['grade']))

        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.stackedWidget.setCurrentWidget(self.widget_ajouter_chercheur)
        
    def afficher_supprimer_chercheur_equipe(self):
        pass

    # ==========================================
    # MÉTHODES GESTION BDD
    # ==========================================
    
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
        if connection is None:
            return 

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
            if connection:
                connection.rollback()
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()

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

        self.widget_creer_equipes_lineEdit_nom.clear()
        self.widget_creer_equipes_lineEdit_abreviation.clear()
        self.widget_creer_equipes_lineEdit_axe.clear()
        self.widget_creer_equipes_textEdit_description.clear()

    def creer_equipe(self):
        nom = self.widget_creer_equipes_lineEdit_nom.text()
        abreviation = self.widget_creer_equipes_lineEdit_abreviation.text()
        axe = self.widget_creer_equipes_lineEdit_axe.text()
        description = self.widget_creer_equipes_textEdit_description.toPlainText()
        date = dt.datetime.now()
        
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()

            sql = """
                INSERT INTO equipe 
                (nom_eq, abreviation_eq, axe_recherche_eq, description_eq, date_creation_eq) 
                VALUES (?, ?, ?, ?, ?)
            """
            valeurs = (nom, abreviation, axe, description, date)

            cursor.execute(sql, valeurs)
            connection.commit()
            print("✅ Équipe créée avec succès.")
            self.nettoyer_formulaire()

        except sqlite3.Error as e:
            if connection:
                connection.rollback()
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()

if __name__ == "__main__":
    window = MainWindow("IETR")
    window.show()
    sys.exit(app.exec())
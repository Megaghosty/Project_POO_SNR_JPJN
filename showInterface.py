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
        self.widget_ajouter_chercheur_btn_ajouter.clicked.connect(self.ajouter_chercheur)
        self.btn_deconnection.clicked.connect(self.deconnexion)

        # ---------------------------------------------------------
        # CONFIGURATION DU MESSAGE D'ERREUR CACHÉ
        # ---------------------------------------------------------
        if hasattr(self, 'label_compteutilse'):
            self.label_compteutilse.setVisible(False)
            self.label_compteutilse.setStyleSheet("color: red; font-weight: bold;")

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
            # On récupère aussi l'équipe de l'utilisateur pour le Chef d'équipe
            query = "SELECT idChercheur, nom, prenom, type_role, grade, pw, Equipe_idEquipe FROM chercheur WHERE user = ?"
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
                        "grade": result['grade'],
                        "id_equipe": result['Equipe_idEquipe'] # NOUVEAU
                    }
                    
                    print(f"✅ Connexion réussie ! Bienvenue {self.utilisateur_connecte['prenom']}.")
                    print(f"   - Grade : {self.utilisateur_connecte['grade']}")
                    
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

    def deconnexion(self):
        self.utilisateur_connecte = None
        print("👋 Vous êtes déconnecté.")
        self.appliquer_droits()
        self.stackedWidget.setCurrentWidget(self.widget_home)

    def appliquer_droits(self):
        """Affiche ou masque les boutons selon le profil de l'utilisateur."""
        
        if self.utilisateur_connecte is None:
            est_admin = False
            est_chef = False
            peut_gerer_publications = False
            
            self.btn_connection.setVisible(True)
            self.btn_deconnection.setVisible(False)
            self.label_23.setText("Non connecté")
            self.label_23.setStyleSheet("color: gray;")
            
        else:
            role = self.utilisateur_connecte['role']
            grade = self.utilisateur_connecte['grade']
            prenom = self.utilisateur_connecte['prenom']
            nom = self.utilisateur_connecte['nom']

            # Définition des rôles
            est_admin = (role == "Administrateur" or grade == "Super-Admin")
            est_chef = (grade == "Chef d'équipe")
            est_stagiaire = any(mot in grade for mot in ["Stagiaire", "Doctorant", "Assistant"])
            
            # Gestion des publications
            if est_admin or est_chef:
                peut_gerer_publications = True
            elif est_stagiaire:
                peut_gerer_publications = False
            else:
                peut_gerer_publications = True # Chercheur normal

            self.btn_connection.setVisible(False) 
            self.btn_deconnection.setVisible(True) 
            self.label_23.setText(f"👤 {prenom} {nom} ({grade})")
            self.label_23.setStyleSheet("color: green; font-weight: bold;")

        # --- APPLICATION À L'INTERFACE ---
        
        # Seul l'Admin peut créer/supprimer des profils ou des équipes entières
        peut_creer_suppr_global = est_admin
        
        self.widget_personnel_btn_creer_chercheur.setVisible(peut_creer_suppr_global)
        self.widget_personnel_btn_supprimer_chercheur.setVisible(peut_creer_suppr_global)
        
        self.widget_equipes_btn_creer_equipe.setVisible(peut_creer_suppr_global)
        self.widget_equipes_btn_supprimer_chercheur.setVisible(peut_creer_suppr_global) # Attention ce bouton supprime l'équipe !

        # Le Chef d'équipe ET l'Admin peuvent gérer les membres des équipes
        peut_gerer_membres = est_admin or est_chef
        self.widget_equipes_btn_ajouter_chercheur.setVisible(peut_gerer_membres)

        # /!\ DÉCOMMETTRE ET CHANGER LE NOM DU BOUTON ICI POUR LES PUBLICATIONS :
        # if hasattr(self, 'nom_du_bouton_creer_publication'):
        #     self.nom_du_bouton_creer_publication.setVisible(peut_gerer_publications)


    # ==========================================
    # MÉTHODES D'AFFICHAGE ET SUPPRESSION
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
                if d['nom'] != "Système":
                    if d['Equipe_idEquipe'] != None:
                        self.widget_personnel_listWidget_personnel.addItem(str(d['nom'])+" | "+ str(d['prenom'])+" | "+ str(d['grade'])+" | "+ str(d['Equipe_idEquipe']))
                    else:
                        self.widget_personnel_listWidget_personnel.addItem(str(d['nom'])+" | "+ str(d['prenom'])+" | "+ str(d['grade'])+" |      ")
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.stackedWidget.setCurrentWidget(self.widget_personnel)
        
    def afficher_supprimer_chercheur(self):
        if not self.utilisateur_connecte or self.utilisateur_connecte['role'] != "Administrateur":
            print("⛔ Accès refusé.")
            return

        item_selectionne = self.widget_personnel_listWidget_personnel.currentItem()
        if item_selectionne is None:
            print("⚠️ Veuillez sélectionner un chercheur.")
            return

        texte = item_selectionne.text().split(" | ")
        nom_select = texte[0].strip()
        prenom_select = texte[1].strip()

        if nom_select == "Système" and prenom_select == "Admin":
            print("⛔ Impossible de supprimer le compte Super-Administrateur !")
            return

        connection = connecter_bdd()
        if connection is None: return 

        try:
            cursor = connection.cursor()
            sql = "DELETE FROM chercheur WHERE nom = ? AND prenom = ?"
            cursor.execute(sql, (nom_select, prenom_select))
            connection.commit()
            print(f"✅ Chercheur {prenom_select} {nom_select} supprimé.")
        except sqlite3.Error as e:
            if connection: connection.rollback()
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection: connection.close()
            self.afficher_personnel()

    def afficher_creer_equipe(self):
        if not self.utilisateur_connecte or self.utilisateur_connecte['role'] != "Administrateur":
            return
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()
            self.widget_creer_equipes_comboBox_chef.clear()
            sql = """SELECT * FROM chercheur WHERE est_permanent = 1 AND Equipe_idEquipe IS NULL"""
            cursor.execute(sql)
            data = cursor.fetchall()
            for i in range(len(data)):
                d = dict(data[i])
                if d['nom'] != "Système":
                    self.widget_creer_equipes_comboBox_chef.addItem(str(d['nom'])+" | "+str(d['prenom']))

        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
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
                self.widget_equipes_listWidget_equipes.addItem(str(d['idEquipe'])+" | "+str(d['nom_eq'])+" | "+ str(d['abreviation_eq']))
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.stackedWidget.setCurrentWidget(self.widget_equipes)

    def afficher_supprimer_chercheur_equipe(self):
        if not self.utilisateur_connecte or self.utilisateur_connecte['role'] != "Administrateur":
            print("⛔ Accès refusé.")
            return

        item_selectionne = self.widget_equipes_listWidget_equipes.currentItem()
        if item_selectionne is None:
            print("⚠️ Veuillez sélectionner une équipe.")
            return

        texte = item_selectionne.text().split(" | ")
        id_equipe = texte[0].strip()

        connection = connecter_bdd()
        if connection is None: return 

        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE chercheur SET Equipe_idEquipe = NULL WHERE Equipe_idEquipe = ?", (id_equipe,))
            cursor.execute("DELETE FROM equipe WHERE idEquipe = ?", (id_equipe,))
            connection.commit()
            print(f"✅ Équipe supprimée.")
        except sqlite3.Error as e:
            if connection: connection.rollback()
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection: connection.close()
            self.afficher_equipe()

    def afficher_publications(self):
        self.stackedWidget.setCurrentWidget(self.widget_publications)
        
    def afficher_creer_chercheur(self):
        if not self.utilisateur_connecte or self.utilisateur_connecte['role'] != "Administrateur":
            return
        self.stackedWidget.setCurrentWidget(self.widget_creer_chercheur)
        
    def afficher_ajouter_chercheur(self):
        if not self.utilisateur_connecte: return
        is_admin = (self.utilisateur_connecte['role'] == "Administrateur")
        is_chef = (self.utilisateur_connecte['grade'] == "Chef d'équipe")
        
        if not is_admin and not is_chef:
            return

        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()

            self.widget_ajouter_chercheur_listWidget_equipe.clear()
            self.widget_ajouter_chercheur_listWidget_chercheur.clear()

            # 🛡️ Si c'est un Chef d'équipe, on ne montre que SON équipe
            if is_chef and not is_admin:
                id_equipe_chef = self.utilisateur_connecte.get('id_equipe')
                if id_equipe_chef is not None:
                    sql = """SELECT * FROM equipe WHERE idEquipe = ?"""
                    cursor.execute(sql, (id_equipe_chef,))
                else:
                    print("⚠️ Vous n'êtes rattaché à aucune équipe.")
                    # Requête qui ne renvoie rien pour éviter de tout afficher
                    cursor.execute("SELECT * FROM equipe WHERE idEquipe = -1")
            else:
                # Si c'est l'Admin, on montre tout
                sql = """SELECT * FROM equipe"""
                cursor.execute(sql)
                
            data = cursor.fetchall()
            for i in range(len(data)):
                d = dict(data[i])
                self.widget_ajouter_chercheur_listWidget_equipe.addItem(str(d['idEquipe'])+" | "+str(d['nom_eq'])+" | "+ str(d['abreviation_eq']))
            
            # Liste de tous les chercheurs
            sql = """SELECT * FROM chercheur"""
            cursor.execute(sql)
            data = cursor.fetchall()
            for i in range(len(data)):
                d = dict(data[i])
                if d['nom'] != "Système":
                    if d['Equipe_idEquipe'] != None:
                        self.widget_ajouter_chercheur_listWidget_chercheur.addItem(str(d['nom'])+" | "+ str(d['prenom'])+" | "+ str(d['grade'])+" | "+ str(d['Equipe_idEquipe']))
                    else:
                        self.widget_ajouter_chercheur_listWidget_chercheur.addItem(str(d['nom'])+" | "+ str(d['prenom'])+" | "+ str(d['grade'])+" |      ")

        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.stackedWidget.setCurrentWidget(self.widget_ajouter_chercheur)
        
    # ==========================================
    # MÉTHODES GESTION BDD
    # ==========================================

    def ajouter_chercheur(self):
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()
            n = self.widget_ajouter_chercheur_listWidget_chercheur.currentItem()
            p = self.widget_ajouter_chercheur_listWidget_chercheur.currentItem()
            e = self.widget_ajouter_chercheur_listWidget_equipe.currentItem()

            if n != None and p != None and e != None:
                nom_select = n.text().split(" | ")[0]
                prenom_select = p.text().split(" | ")[1]
                equipe = e.text().split(" | ")[1]

                sql = """SELECT * FROM equipe WHERE nom_eq = ?"""
                
                cursor.execute(sql,(equipe,))
                equ = dict(cursor.fetchone())['idEquipe']

                # Sécurité : vérifier que le chef n'ajoute pas à une autre équipe
                is_admin = (self.utilisateur_connecte['role'] == "Administrateur")
                if not is_admin:
                    id_equipe_chef = self.utilisateur_connecte.get('id_equipe')
                    if equ != id_equipe_chef:
                        print("⛔ Accès refusé : Vous ne pouvez ajouter des membres qu'à votre propre équipe.")
                        return

                sql = """UPDATE chercheur SET Equipe_idEquipe = ?  WHERE prenom = ? AND nom = ?"""
                cursor.execute(sql,(equ,nom_select,prenom_select))
                connection.commit()
                print("✅ Chercheur affecté à l'équipe avec succès.")

        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")

        finally:
            if connection:
                connection.close()
            self.afficher_ajouter_chercheur()

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

            cursor.execute("SELECT nom FROM chercheur WHERE user = ? OR email = ?", (userName, email))
            if cursor.fetchone():
                print("⛔ Erreur : Ce nom d'utilisateur ou cet email est déjà utilisé !")
                if hasattr(self, 'label_compteutilse'):
                    self.label_compteutilse.setText("⚠️ Ce nom d'utilisateur ou cet email est déjà pris !")
                    self.label_compteutilse.setVisible(True)
                return 
            
            if hasattr(self, 'label_compteutilse'):
                self.label_compteutilse.setVisible(False)

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

        if hasattr(self, 'label_compteutilse'):
            self.label_compteutilse.setVisible(False)

        self.widget_creer_equipes_lineEdit_nom.clear()
        self.widget_creer_equipes_lineEdit_abreviation.clear()
        self.widget_creer_equipes_lineEdit_axe.clear()
        self.widget_creer_equipes_textEdit_description.clear()

    def creer_equipe(self):
        nom = self.widget_creer_equipes_lineEdit_nom.text().strip()
        abreviation = self.widget_creer_equipes_lineEdit_abreviation.text().strip()
        axe = self.widget_creer_equipes_lineEdit_axe.text()
        description = self.widget_creer_equipes_textEdit_description.toPlainText()
        date = dt.datetime.now()
        
        if not nom or not abreviation:
            print("⚠️ Erreur : Le nom de l'équipe et son abréviation sont obligatoires.")
            return

        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()

            cursor.execute("SELECT nom_eq FROM equipe WHERE nom_eq = ? OR abreviation_eq = ?", (nom, abreviation))
            if cursor.fetchone():
                print("⛔ Erreur : Une équipe avec ce nom ou cette abréviation existe déjà !")
                return 

            sql = """
                INSERT INTO equipe 
                (nom_eq, abreviation_eq, axe_recherche_eq, description_eq, date_creation_eq) 
                VALUES (?, ?, ?, ?, ?)
            """
            valeurs = (nom, abreviation, axe, description, date)
            cursor.execute(sql, valeurs)
            connection.commit()

            chef = self.widget_creer_equipes_comboBox_chef.currentText()
            if chef:
                nom_chef = chef.split(" | ")[0]
                prenom_chef = chef.split(" | ")[1]
                cursor.execute("""SELECT * FROM equipe WHERE nom_eq = ?""",(nom,))
                id_eq = dict(cursor.fetchone())['idEquipe']
                cursor.execute("UPDATE chercheur SET grade = ? WHERE nom = ? AND prenom = ?", ("Chef d'équipe",nom_chef, prenom_chef))
                cursor.execute("UPDATE chercheur SET Equipe_idEquipe = ? WHERE nom = ? AND prenom = ?", (id_eq,nom_chef, prenom_chef))
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
            self.stackedWidget.setCurrentWidget(self.widget_equipes)

if __name__ == "__main__":
    window = MainWindow("IETR")
    window.show()
    sys.exit(app.exec())
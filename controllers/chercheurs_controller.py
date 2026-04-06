import sqlite3
import bcrypt
from connexion_bdd import connecter_bdd

class ChercheursController:
    """
    Contrôleur pour la gestion du personnel, ajout et création de chercheurs.
    """
    def __init__(self, main_window):
        self.window = main_window

    def afficher_personnel(self):
        """Affiche la liste de tout le personnel dans l'interface."""
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()
            self.window.widget_personnel_listWidget_personnel.clear()
            
            # --- NOUVEAU : En-tête de la liste ---
            self.window.widget_personnel_listWidget_personnel.addItem("📌 NOM | PRÉNOM | GRADE | ID ÉQUIPE")
            self.window.widget_personnel_listWidget_personnel.addItem("-" * 60)
            
            sql = """SELECT * FROM chercheur"""
            cursor.execute(sql)
            data = cursor.fetchall()
            for i in range(len(data)):
                d = dict(data[i])
                if d['nom'] != "Système":
                    if d['Equipe_idEquipe'] != None:
                        self.window.widget_personnel_listWidget_personnel.addItem(str(d['nom'])+" | "+ str(d['prenom'])+" | "+ str(d['grade'])+" | "+ str(d['Equipe_idEquipe']))
                    else:
                        self.window.widget_personnel_listWidget_personnel.addItem(str(d['nom'])+" | "+ str(d['prenom'])+" | "+ str(d['grade'])+" |      ")
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.window.stackedWidget.setCurrentWidget(self.window.widget_personnel)

    def afficher_supprimer_chercheur(self):
        """Supprime un chercheur sélectionné de la base de données."""
        if not self.window.utilisateur_connecte or self.window.utilisateur_connecte['role'] != "Administrateur":
            print("⛔ Accès refusé.")
            return

        item_selectionne = self.window.widget_personnel_listWidget_personnel.currentItem()
        if item_selectionne is None:
            print("⚠️ Veuillez sélectionner un chercheur.")
            return
            
        # --- NOUVELLE SÉCURITÉ ---
        if "📌" in item_selectionne.text() or "---" in item_selectionne.text():
            print("⚠️ Vous avez sélectionné l'en-tête. Veuillez choisir un chercheur valide.")
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

    def afficher_creer_chercheur(self):
        """Affiche le formulaire pour créer un chercheur."""
        if not self.window.utilisateur_connecte or self.window.utilisateur_connecte['role'] != "Administrateur":
            return
        self.window.stackedWidget.setCurrentWidget(self.window.widget_creer_chercheur)

    def afficher_ajouter_chercheur(self):
        """Affiche l'interface d'ajout d'un chercheur dans une équipe."""
        if not self.window.utilisateur_connecte: return
        is_admin = (self.window.utilisateur_connecte['role'] == "Administrateur")
        is_chef = (self.window.utilisateur_connecte['grade'] == "Chef d'équipe")
        
        if not is_admin and not is_chef:
            return

        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()

            self.window.widget_ajouter_chercheur_listWidget_chercheur.clear()
            
            self.window.widget_ajouter_chercheur_listWidget_chercheur.addItem("📌 NOM | PRÉNOM | GRADE | ID ÉQUIPE")
            self.window.widget_ajouter_chercheur_listWidget_chercheur.addItem("-" * 60)
            
            # Liste de tous les chercheurs
            id_eq = self.window.widget_equipes_listWidget_equipes.currentItem().text().split(" | ")[0]
            sql = """SELECT * FROM chercheur WHERE Equipe_idEquipe != ? OR Equipe_idEquipe IS NULL"""
            cursor.execute(sql,(id_eq,))
            data = cursor.fetchall()
            for i in range(len(data)):
                d = dict(data[i])
                if d['nom'] != "Système" and d['grade'] != "Chef d'équipe":
                    if d['Equipe_idEquipe'] != None:
                        self.window.widget_ajouter_chercheur_listWidget_chercheur.addItem(str(d['nom'])+" | "+ str(d['prenom'])+" | "+ str(d['grade'])+" | "+ str(d['Equipe_idEquipe']))
                    else:
                        self.window.widget_ajouter_chercheur_listWidget_chercheur.addItem(str(d['nom'])+" | "+ str(d['prenom'])+" | "+ str(d['grade'])+" |      ")

        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.window.stackedWidget.setCurrentWidget(self.window.widget_ajouter_chercheur)

    def ajouter_chercheur(self):
        """Attribue le chercheur sélectionné à une équipe spécifique."""
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()
            n = self.window.widget_ajouter_chercheur_listWidget_chercheur.currentItem()
            p = self.window.widget_ajouter_chercheur_listWidget_chercheur.currentItem()
            e = self.window.widget_equipes_listWidget_equipes.currentItem()

            if n != None and p != None:
                # --- NOUVELLE SÉCURITÉ ---
                if "📌" in n.text() or "---" in n.text() or "📌" in e.text() or "---" in e.text():
                    print("⚠️ Vous avez sélectionné un en-tête au lieu d'un élément valide.")
                    return
                    
                nom_select = n.text().split(" | ")[0]
                prenom_select = p.text().split(" | ")[1]
                equipe = e.text().split(" | ")[1]

                sql = """SELECT * FROM equipe WHERE nom_eq = ?"""
                
                cursor.execute(sql,(equipe,))
                equ = dict(cursor.fetchone())['idEquipe']

                # Sécurité : vérifier que le chef n'ajoute pas à une autre équipe
                is_admin = (self.window.utilisateur_connecte['role'] == "Administrateur")
                if not is_admin:
                    id_equipe_chef = self.window.utilisateur_connecte.get('id_equipe')
                    if equ != id_equipe_chef:
                        print("⛔ Accès refusé : Vous ne pouvez ajouter des membres qu'à votre propre équipe.")
                        return

                sql = """UPDATE chercheur SET Equipe_idEquipe = ? WHERE prenom = ? AND nom = ?"""
                cursor.execute(sql,(equ,prenom_select,nom_select))
                connection.commit()
                print("✅ Chercheur affecté à l'équipe avec succès.")

        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")

        finally:
            if connection:
                connection.close()
            self.afficher_ajouter_chercheur()

    def creer_chercheur(self):
        """Inscrit un nouveau chercheur dans la base de données avec l'ensemble des informations de profil."""
        nom = self.window.widget_creer_chercheur_lineEdit_nom.text()
        prenom = self.window.widget_creer_chercheur_lineEdit_prenom.text()
        sexe = self.window.widget_creer_chercheur_comboBox_sexe.currentText()
        email = self.window.widget_creer_chercheur_lineEdit_email.text()
        telephone = self.window.widget_creer_chercheur_lineEdit_telephone.text()
        userName = self.window.widget_creer_chercheur_lineEdit_nom_utilisateur.text()
        mdp = self.window.widget_creer_chercheur_lineEdit_mdp.text()
        confirmationMdp = self.window.widget_creer_chercheur_lineEdit_confirmation_mdp.text()
        specialite = self.window.widget_creer_chercheur_lineEdit_specialite.text()
        recherche = self.window.widget_creer_chercheur_lineEdit_recherche.text()
        grade = self.window.widget_creer_chercheur_comboBox_grade.currentText()
        
        naissance_qt = self.window.widget_creer_chercheur_dateEdit_naissance.dateTime()
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
                if hasattr(self.window, 'label_compteutilse'):
                    self.window.label_compteutilse.setText("⚠️ Ce nom d'utilisateur ou cet email est déjà pris !")
                    self.window.label_compteutilse.setVisible(True)
                return 
            
            if hasattr(self.window, 'label_compteutilse'):
                self.window.label_compteutilse.setVisible(False)

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
            self.window.nettoyer_formulaire()

        except sqlite3.Error as e:
            if connection:
                connection.rollback()
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
import sqlite3
import datetime as dt
from connexion_bdd import connecter_bdd

class EquipesController:
    """
    Contrôleur pour la gestion des équipes et de  leurs membres.
    """
    def __init__(self, main_window):
        self.window = main_window

    def afficher_equipe(self):
        """Affiche la liste des équipes dans l'interface."""
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()
            self.window.widget_equipes_listWidget_equipes.clear()
            
            # --- NOUVEAU : En-tête de la liste ---
            self.window.widget_equipes_listWidget_equipes.addItem("📌 ID ÉQUIPE | NOM | ABRÉVIATION")
            self.window.widget_equipes_listWidget_equipes.addItem("-" * 60)
            
            sql = """SELECT * FROM equipe"""
            cursor.execute(sql)
            data = cursor.fetchall()
            for i in range(len(data)):
                d = dict(data[i])
                self.window.widget_equipes_listWidget_equipes.addItem(str(d['idEquipe'])+" | "+str(d['nom_eq'])+" | "+ str(d['abreviation_eq']))
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.window.stackedWidget.setCurrentWidget(self.window.widget_equipes)

    def afficher_creer_equipe(self):
        """Affiche le formulaire de création d'une nouvelle équipe."""
        if not self.window.utilisateur_connecte or self.window.utilisateur_connecte['role'] != "Administrateur":
            return
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()
            self.window.widget_creer_equipes_comboBox_chef.clear()
            sql = """SELECT * FROM chercheur WHERE est_permanent = 1 AND Equipe_idEquipe IS NULL"""
            cursor.execute(sql)
            data = cursor.fetchall()
            for i in range(len(data)):
                d = dict(data[i])
                if d['nom'] != "Système":
                    self.window.widget_creer_equipes_comboBox_chef.addItem(str(d['nom'])+" | "+str(d['prenom']))

        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.window.stackedWidget.setCurrentWidget(self.window.widget_creer_equipe)

    def creer_equipe(self):
        """Prend les données du formulaire et crée l'équipe en base de données."""
        nom = self.window.widget_creer_equipes_lineEdit_nom.text().strip()
        abreviation = self.window.widget_creer_equipes_lineEdit_abreviation.text().strip()
        axe = self.window.widget_creer_equipes_lineEdit_axe.text()
        description = self.window.widget_creer_equipes_textEdit_description.toPlainText()
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

            chef = self.window.widget_creer_equipes_comboBox_chef.currentText()
            if chef:
                nom_chef = chef.split(" | ")[0]
                prenom_chef = chef.split(" | ")[1]
                cursor.execute("""SELECT * FROM equipe WHERE nom_eq = ?""",(nom,))
                id_eq = dict(cursor.fetchone())['idEquipe']
                cursor.execute("UPDATE chercheur SET grade = ? WHERE nom = ? AND prenom = ?", ("Chef d'équipe",nom_chef, prenom_chef))
                cursor.execute("UPDATE chercheur SET Equipe_idEquipe = ? WHERE nom = ? AND prenom = ?", (id_eq,nom_chef, prenom_chef))
                connection.commit()
            
            print("✅ Équipe créée avec succès.")
            self.window.nettoyer_formulaire()

        except sqlite3.Error as e:
            if connection:
                connection.rollback()
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.window.stackedWidget.setCurrentWidget(self.window.widget_equipes)

    def afficher_supprimer_chercheur_equipe(self):
        """Supprime une équipe sélectionnée de la base de données."""
        if not self.window.utilisateur_connecte or self.window.utilisateur_connecte['role'] != "Administrateur":
            print("⛔ Accès refusé.")
            return

        item_selectionne = self.window.widget_equipes_listWidget_equipes.currentItem()
        if item_selectionne is None:
            print("⚠️ Veuillez sélectionner une équipe.")
            return
            
        # --- NOUVELLE SÉCURITÉ ---
        if "📌" in item_selectionne.text() or "---" in item_selectionne.text():
            print("⚠️ Vous avez sélectionné l'en-tête. Veuillez choisir une équipe valide.")
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

    def afficher_membres(self):
        """Affiche les membres rattachés à une équipe particulière."""
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()
            self.window.widget_membres_equipe_listWidget_membres.clear()
            eq = self.window.widget_equipes_listWidget_equipes.currentItem().text().split(" | ")[1]
            sql = """SELECT * FROM equipe WHERE nom_eq = ?"""
            cursor.execute(sql,(eq,))
            data = dict(cursor.fetchone())

            sql = """SELECT * FROM chercheur WHERE equipe_idEquipe = ?"""
            cursor.execute(sql,(data["idEquipe"],))
            data = cursor.fetchall()
            for i in data:
                d = dict(i)
                self.window.widget_membres_equipe_listWidget_membres.addItem(d['nom']+" | "+d['prenom'])

        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")

        finally:
            if connection:
                connection.close()
            self.window.stackedWidget.setCurrentWidget(self.window.widget_membres_equipe)

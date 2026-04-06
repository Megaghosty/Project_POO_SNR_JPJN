import sqlite3
from connexion_bdd import connecter_bdd

class PublicationsController:
    """
    Contrôleur gérant l'affichage, la création et la consultation des publications.
    """
    
    def __init__(self, main_window):
        self.window = main_window

    def afficher_publications(self):
        """Affiche la liste de toutes les publications dans l'interface."""
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()
            self.window.widget_publication_listWidget_publications.clear()
            sql = """SELECT * FROM publication"""
            cursor.execute(sql)
            data = cursor.fetchall()
            for i in range(len(data)):
                d = dict(data[i])
                self.window.widget_publication_listWidget_publications.addItem(str(d['titre']))
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.window.stackedWidget.setCurrentWidget(self.window.widget_publications)

    def afficher_publication(self):
        """Charge le contenu détaillé d'une publication sélectionnée."""
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()
            self.window.widget_personnel_listWidget_personnel.clear()
            sql = """SELECT * FROM publication WHERE titre = ?"""
            cursor.execute(sql,(self.window.widget_publication_listWidget_publications.currentItem().text(),))
            data = dict(cursor.fetchone())
            self.window.widget_afficher_publication_textBrowser_publication.setText(data['fichier'])
            self.window.widget_publication_listWidget_publications.clear()

        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")

        finally:
            if connection:
                connection.close()
            self.window.stackedWidget.setCurrentWidget(self.window.widget_afficher_publication)

    def creer_publication(self):
        """Prend les données du formulaire et insère la nouvelle publication en base."""
        connection = connecter_bdd()
        if connection is None:
            return 

        try:
            cursor = connection.cursor()
            self.window.widget_personnel_listWidget_personnel.clear()
            sql = """
                INSERT INTO publication 
                (titre, fichier) 
                VALUES (?, ?)
            """
            valeurs = (self.window.widget_creer_publication_lineEdit_nom.text(), self.window.widget_creer_publication_textEdit_publication.toPlainText())

            cursor.execute(sql, valeurs)
            connection.commit()
            print("✅ Publication créée avec succès.")
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite : {e}")
        finally:
            if connection:
                connection.close()
            self.window.stackedWidget.setCurrentWidget(self.window.widget_publications)

    def afficher_creer_publication(self):
        """Affiche le formulaire pour rédiger une nouvelle publication."""
        if not self.window.utilisateur_connecte or self.window.utilisateur_connecte['role'] != "Administrateur":
            return
        self.window.stackedWidget.setCurrentWidget(self.window.widget_creer_publication)

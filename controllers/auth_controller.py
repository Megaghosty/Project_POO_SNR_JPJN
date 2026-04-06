import sqlite3
import bcrypt
from connexion_bdd import connecter_bdd

class AuthController:
    """
    Contrôleur gérant l'authentification et les droits des utilisateurs.
    """
    
    def __init__(self, main_window):
        """
        Initialise le contrôleur avec l'interface principale.
        :param main_window: L'instance de MainWindow (interface graphique)
        """
        self.window = main_window

    def afficher_connection(self):
        """Affiche la page de connexion sur l'interface."""
        self.window.stackedWidget.setCurrentWidget(self.window.widget_connection)

    def verification_connection(self):
        """Vérifie les informations de connexion de l'utilisateur."""
        username = self.window.widget_connection_lineEdit_nom.text()
        password = self.window.widget_connection_lineEdit_mdp.text()

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
                    self.window.utilisateur_connecte = {
                        "id": result['idChercheur'],
                        "nom": result['nom'],
                        "prenom": result['prenom'],
                        "role": result['type_role'],
                        "grade": result['grade'],
                        "id_equipe": result['Equipe_idEquipe']
                    }
                    
                    print(f"✅ Connexion réussie ! Bienvenue {self.window.utilisateur_connecte['prenom']}.")
                    print(f"   - Grade : {self.window.utilisateur_connecte['grade']}")
                    
                    # 🔒 On met à jour les droits d'affichage après connexion !
                    self.appliquer_droits()

                    self.window.stackedWidget.setCurrentWidget(self.window.widget_home)
                    self.window.widget_connection_lineEdit_nom.clear()
                    self.window.widget_connection_lineEdit_mdp.clear()
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
        """Gère la déconnexion de l'utilisateur actuel."""
        self.window.utilisateur_connecte = None
        print("👋 Vous êtes déconnecté.")
        self.appliquer_droits()
        self.window.stackedWidget.setCurrentWidget(self.window.widget_home)

    def appliquer_droits(self):
        """Affiche ou masque les boutons et fonctionnalités selon le profil de l'utilisateur."""
        if self.window.utilisateur_connecte is None:
            est_admin = False
            est_chef = False
            peut_gerer_publications = False
            
            self.window.btn_connection.setVisible(True)
            self.window.btn_deconnection.setVisible(False)
            self.window.label_23.setText("Non connecté")
            self.window.label_23.setStyleSheet("color: gray;")
            
        else:
            role = self.window.utilisateur_connecte['role']
            grade = self.window.utilisateur_connecte['grade']
            prenom = self.window.utilisateur_connecte['prenom']
            nom = self.window.utilisateur_connecte['nom']

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

            self.window.btn_connection.setVisible(False) 
            self.window.btn_deconnection.setVisible(True) 
            self.window.label_23.setText(f"👤 {prenom} {nom} ({grade})")
            self.window.label_23.setStyleSheet("color: green; font-weight: bold;")

        # --- APPLICATION À L'INTERFACE ---
        
        # Seul l'Admin peut créer/supprimer des profils ou des équipes entières
        peut_creer_suppr_global = est_admin
        
        self.window.widget_personnel_btn_creer_chercheur.setVisible(peut_creer_suppr_global)
        self.window.widget_personnel_btn_supprimer_chercheur.setVisible(peut_creer_suppr_global)
        
        self.window.widget_equipes_btn_creer_equipe.setVisible(peut_creer_suppr_global)
        self.window.widget_equipes_btn_supprimer_chercheur.setVisible(peut_creer_suppr_global) # Attention ce bouton supprime l'équipe !

        # Le Chef d'équipe ET l'Admin peuvent gérer les membres des équipes
        peut_gerer_membres = est_admin or est_chef
        self.window.widget_equipes_btn_membres.setVisible(peut_gerer_membres)

        # Boutons de publications
        self.window.widget_publication_btn_creer.setVisible(peut_gerer_publications)

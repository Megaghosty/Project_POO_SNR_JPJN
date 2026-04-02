import sqlite3
import bcrypt
from connexion_bdd import connecter_bdd 

def injecter_admin():
    connection = connecter_bdd()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        
        mot_de_passe_clair = "admin123" 
        
        salt = bcrypt.gensalt()
        mdp_hashe = bcrypt.hashpw(mot_de_passe_clair.encode('utf-8'), salt).decode('utf-8')

        # Ajout de idChercheur au début de la requête
        sql = """
            INSERT INTO chercheur 
            (idChercheur, nom, prenom, user, pw, type_role, est_permanent, email, sexe, telephone, specialite, grade, date_naissance) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Ajout du 0 en première position
        valeurs = (
            0,                     # 👉 idChercheur forcé à 0
            "Système",             # nom
            "Admin",               # prenom
            "admin",               # user 
            mdp_hashe,             # pw
            "Administrateur",      # type_role
            1,                     # est_permanent
            "admin@admin.com",     # email
            "Autre",               # sexe
            "0000000000",          # telephone
            "Administration",      # specialite
            "Super-Admin",         # grade
            "2000-01-01"           # date_naissance
        )

        cursor.execute(sql, valeurs)
        connection.commit()
        
        print("✅ Compte administrateur créé avec l'ID 0 !")
        print(f"👉 Identifiant : admin")
        print(f"👉 Mot de passe : {mot_de_passe_clair}")

    except sqlite3.IntegrityError:
        print("⚠️ Un compte avec l'ID 0 (ou le pseudo 'admin') existe peut-être déjà.")
    except sqlite3.Error as e:
        print(f"❌ Erreur SQL : {e}")
    finally:
        if connection:
            connection.close()

injecter_admin()
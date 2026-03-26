import mysql.connector
import bcrypt
from mysql.connector import Error

connection = None
cursor = None

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mydb'
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # --- TEST AVEC MOT DE PASSE BIDON ---
        mdp_clair = "password123" 
        salt = bcrypt.gensalt()
        mdp_hashe = bcrypt.hashpw(mdp_clair.encode('utf-8'), salt)
        
        # Affichage pour ton information
        print(f"Le mot de passe '{mdp_clair}' sera stocké comme : {mdp_hashe.decode('utf-8')}")

        # 1. Laboratoire
        sql_lab = "INSERT INTO Laboratoire (nom_complet, abreviation) VALUES (%s, %s)"
        cursor.execute(sql_lab, ("Laboratoire de Test", "LAB-TEST"))
        id_labo = cursor.lastrowid

        # 2. Equipe
        sql_eq = "INSERT INTO Equipe (nom, abreviation, id_labo) VALUES (%s, %s, %s)"
        cursor.execute(sql_eq, ("Equipe Alpha", "ALPHA", id_labo))
        id_equipe = cursor.lastrowid

        # 3. Chercheur (avec le hash)
        sql_ch = """INSERT INTO Chercheur (nom, prenom, login, mdp_hash, id_equipe) 
                    VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql_ch, ("Doe", "John", "test_user", mdp_hashe.decode('utf-8'), id_equipe))
        id_chercheur = cursor.lastrowid

        # 4. Chercheur Permanent
        sql_perm = "INSERT INTO Chercheur_Permanent (id_chercheur, grade) VALUES (%s, %s)"
        cursor.execute(sql_perm, (id_chercheur, "Stagiaire"))

        # 5. Publication
        sql_pub = "INSERT INTO Publication (titre, date_publication) VALUES (%s, %s)"
        cursor.execute(sql_pub, ("Ma premiere publication", "2024-05-20"))
        id_publi = cursor.lastrowid

        # 6. Association Auteur/Publication
        sql_assoc = "INSERT INTO Auteur_Publication (id_chercheur, id_publi) VALUES (%s, %s)"
        cursor.execute(sql_assoc, (id_chercheur, id_publi))

        connection.commit()
        print("\nInsertion réussie !")
        print(f"Login : test_user")
        print(f"MDP   : password123")

except Error as e:
    if connection:
        connection.rollback()
    print(f"Erreur SQL : {e}")

finally:
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
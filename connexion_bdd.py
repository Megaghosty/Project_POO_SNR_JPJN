import sqlite3

def connecter_bdd():
    try:
        
        connexion = sqlite3.connect('bdd_converted.db')
        
        
        connexion.row_factory = sqlite3.Row 
        
        return connexion
    except sqlite3.Error as e:
        print(f"❌ Erreur de connexion à SQLite : {e}")
        return None
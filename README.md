# Project_POO_SNR_JPJN

Application desktop en Python (PyQt6 + SQLite) pour la gestion d'un laboratoire de recherche:
- gestion du personnel (chercheurs),
- gestion des equipes,
- authentification des utilisateurs,
- controle des droits selon le role.

## Apercu

Le projet fournit une interface graphique permettant de:
- afficher la liste du personnel,
- creer un chercheur,
- afficher la liste des equipes,
- creer une equipe,
- preparer l'ajout/suppression de chercheurs dans une equipe,
- se connecter avec un compte existant.

La base de donnees est locale (SQLite), et les mots de passe sont verifies avec `bcrypt`.

## Fonctionnalites principales

### 1) Connexion utilisateur
- Formulaire de connexion (nom d'utilisateur + mot de passe).
- Verification du mot de passe hashé (`bcrypt.checkpw`).
- Creation d'une session utilisateur en memoire (cookie de session applicatif).
- Application des droits selon le role/grade apres connexion.

### 2) Gestion des droits
Les actions d'administration sont visibles uniquement pour les profils admin:
- creer/supprimer des chercheurs,
- creer une equipe,
- ajouter/supprimer des chercheurs des equipes.

Si aucun utilisateur n'est connecte, ces actions sont masquees.

### 3) Gestion du personnel
- Affichage de tous les chercheurs en base.
- Creation d'un chercheur avec:
	- informations personnelles,
	- informations academiques,
	- compte utilisateur,
	- mot de passe hashé avec `bcrypt`.

### 4) Gestion des equipes
- Affichage de toutes les equipes.
- Creation d'une equipe (nom, abreviation, axe de recherche, description, date).

## Stack technique

- Python 3.x
- PyQt6 (interface graphique)
- SQLite3 (base de donnees locale)
- bcrypt (hachage/verif des mots de passe)

## Structure du projet

- `showInterface.py`: logique principale de l'interface, navigation, connexion, droits, CRUD de base.
- `Interface.ui`: maquette Qt Designer (pages, widgets, boutons).
- `connexion_bdd.py`: connexion centralisee a la base SQLite.
- `insertion_sql.py`: script de peuplement/initialisation SQL (si utilise).
- `bdd_converted.sqbpro`: projet DB Browser/SQLite.

## Installation

1. Cloner le depot:

```bash
git clone https://github.com/Megaghosty/Project_POO_SNR_JPJN.git
cd Project_POO_SNR_JPJN
```

2. Installer les dependances Python:

```bash
pip install pyqt6 bcrypt
```

3. Verifier la presence de la base SQLite (`bdd_converted.db`) a la racine du projet.

## Lancement

```bash
python showInterface.py
```

L'application s'ouvre sur la page d'accueil du laboratoire (ex: IETR).

## Notes importantes

- Certaines vues existent dans l'interface mais ne sont pas encore finalisees dans le code (ex: suppression effective d'un chercheur/equipe, publications detaillees).
- Les messages d'erreur/succes sont actuellement affiches en console.

## Ameliorations possibles

- Ajouter des boites de dialogue Qt (`QMessageBox`) pour les retours utilisateur.
- Completer les actions manquantes (suppression/ajout effectif en table de liaison).
- Ajouter des validations plus strictes (email, telephone, unicite username).
- Ajouter des tests unitaires et une couche de services/metier.

## Auteurs

Projet realise dans le cadre d'un travail POO (SNR).


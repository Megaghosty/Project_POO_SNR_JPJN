# Project_POO_SNR_JPJN

Application desktop de gestion de laboratoire de recherche, developpee en Python avec PyQt6 et SQLite.

Le projet permet de gerer des chercheurs et des equipes, avec un systeme de connexion et de droits selon le profil utilisateur.

## Objectifs du projet

- Centraliser les informations du personnel de recherche.
- Organiser les equipes de recherche.
- Controler l'acces aux actions sensibles (creation/modification) via authentification.

## Fonctionnalites

### Authentification
- Connexion via nom d'utilisateur et mot de passe.
- Verification du mot de passe avec bcrypt.
- Session utilisateur en memoire pendant l'execution.

### Gestion des droits
- Utilisateur non connecte: actions d'administration masquees.
- Administrateur / Super-Admin: acces a la gestion du personnel et des equipes.
- Profils stagiaire/assistant/doctorant: acces restreint selon la logique metier.

### Personnel
- Affichage de la liste des chercheurs.
- Creation d'un chercheur avec informations personnelles et professionnelles.
- Hachage du mot de passe lors de l'insertion en base.

### Equipes
- Affichage de la liste des equipes.
- Creation d'une equipe (nom, abreviation, axe, description, date de creation).
- Verification anti-doublons (nom/abreviation) sur la creation.

## Etat actuel

Fonctionnel:
- Connexion utilisateur.
- Affichage personnel/equipes.
- Creation chercheur.
- Creation equipe.
- Gestion visuelle des droits.

Partiellement implemente / a completer:
- Suppression de chercheur.
- Suppression de chercheur d'une equipe.
- Module publications.

## Stack technique

- Python 3
- PyQt6
- SQLite3
- bcrypt

## Arborescence principale

- showInterface.py: logique principale de l'application (UI, navigation, connexion, droits, actions BDD).
- Interface.ui: interface Qt Designer.
- connexion_bdd.py: utilitaire de connexion SQLite.
- bdd_converted.db: base de donnees SQLite utilisee par l'application.
- Interface_ui.py: fichier genere depuis l'UI (selon workflow utilise).

## Installation

1. Cloner le depot

```bash
git clone https://github.com/Megaghosty/Project_POO_SNR_JPJN.git
cd Project_POO_SNR_JPJN
```

2. Installer les dependances

```bash
pip install pyqt6 bcrypt
```

3. Verifier que le fichier bdd_converted.db est present a la racine du projet

## Lancement

```bash
python showInterface.py
```

## Notes techniques

- Les retours utilisateur (succes/erreur) sont majoritairement affiches dans la console.
- Les mots de passe sont stockes sous forme hashée.
- La base est locale (SQLite), sans serveur externe requis.

## Pistes d'amelioration

- Ajouter des QMessageBox pour les messages UI.
- Finaliser toutes les operations CRUD manquantes.
- Ajouter des validations de formulaires (email, telephone, champs obligatoires).
- Ajouter des tests unitaires et une separation plus nette UI/metier/persistance.

## Contexte

Projet realise dans le cadre d'un travail de POO (SNR).


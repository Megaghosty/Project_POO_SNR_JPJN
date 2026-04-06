# 🔬 Gestion de Laboratoire de Recherche (Projet_POO_SNR_JPJN)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt-6.0+-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![Bcrypt](https://img.shields.io/badge/Security-Bcrypt-red.svg)

Application desktop de gestion de laboratoire de recherche, développée en **Python** avec **PyQt6** et une base de données **SQLite**. 

Ce projet permet de gérer efficacement le personnel (chercheurs, doctorants, stagiaires), les équipes de recherche et les publications scientifiques au sein d'un laboratoire, avec un système de droits et d'authentification sécurisé.

---

## 📋 Table des matières
- [Objectifs du projet](#-objectifs-du-projet)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture du Projet](#-architecture-du-projet)
- [Prérequis et Installation](#-prérequis-et-installation)
- [Utilisation](#-utilisation)
- [État d'avancement](#-état-davancement)

---

## 🎯 Objectifs du projet

- Centraliser et gérer les informations du personnel de recherche.
- Organiser les équipes de recherche selon leurs axes de développement.
- Contrôler l'accès aux actions sensibles (création, modification, suppression) via une authentification par profil (Administrateur, Chef d'équipe, Chercheur, etc.).
- Historiser et consulter les publications scientifiques du laboratoire.

---

## ✨ Fonctionnalités

### 🔐 Authentification & Sécurité
- Connexion sécurisée via nom d'utilisateur et mot de passe.
- Hachage cryptographique des mots de passe avec **bcrypt**.
- Gestion de session utilisateur (système de "cookie" local en mémoire).
- Interface dynamique : les actions d'administration sont masquées pour les utilisateurs non connectés ou ne disposant pas des droits suffisants.

### 👥 Gestion du Personnel
- Affichage de la liste détaillée des chercheurs.
- Création d'un chercheur avec ses informations personnelles, son grade et son rôle.
- (En cours) Suppression ou modification du profil d'un chercheur.

### 🏢 Gestion des Équipes
- Consultation de la liste des équipes de recherche.
- Ajout d'une nouvelle équipe (Nom, Abréviation, Axe de recherche).
- Système anti-doublon vérifiant le nom et l'abréviation avant l'insertion en base.
- Visualisation des membres affectés à chaque équipe.

### 📚 Publications
- (En cours) Création et consultation des publications liées aux chercheurs et aux équipes.

---

## 🏗 Architecture du Projet

Le projet suit une structure simple et modulaire :

```text
📁 Project_POO_SNR_JPJN
│
├── showInterface.py    # Point d'entrée principal de l'application
├── Interface.ui        # Fichier design de l'interface (Qt Designer)
├── Interface_ui.py     # Code généré de l'interface graphique
├── connexion_bdd.py    # Logique de connexion à la base SQLite
├── insertion_sql.py    # Script d'initialisation/insertion des données SQL
├── UML.mwb             # Modèle de données conceptuel (MySQL Workbench)
└── README.md           # Documentation du projet
```

---

## 🚀 Prérequis et Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/VOTRE_NOM/Project_POO_SNR_JPJN.git
cd Project_POO_SNR_JPJN
```

### 2. Installer les dépendances
Assurez-vous d'avoir Python 3.8 ou supérieur installé sur votre machine. Installez ensuite les paquets requis :

```bash
pip install PyQt6 bcrypt
```

*(Note: `sqlite3` et `sys` sont inclus par défaut dans la bibliothèque standard de Python).*

### 3. Base de données
La base de données SQLite est générée/récupérée par `connexion_bdd.py`. Vous pouvez utiliser le script `insertion_sql.py` pour pré-remplir la base avec des données de test si nécessaire.

---

## 💻 Utilisation

Pour lancer l'application, exécutez le script principal :

```bash
python showInterface.py
```

1. **Visiteur :** Par défaut, vous avez uniquement un accès en lecture à certaines listes.
2. **Connexion :** Cliquez sur le bouton de connexion en haut à droite pour accéder aux fonctionnalités d'édition (Créez un compte via la BDD ou utilisez les accès de test si vous avez lancé le script d'insertion).

---

## 📊 État d'avancement

**✅ Fonctionnel :**
- Interface graphique (navigation par onglets via `QStackedWidget`).
- Connexion utilisateur avec vérification Bcrypt.
- Affichage du personnel et des équipes.
- Création de chercheurs et d'équipes en BDD.
- Gestion visuelle et dynamique des droits (Admin vs Guest).

**🚧 Partiellement implémenté / À compléter :**
- Suppression / Modification des chercheurs.
- Gestion fine des membres d'une équipe (Ajout/Retrait d'un chercheur à une équipe existante).
- Module complet de création et d'affichage des `Publications`.


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


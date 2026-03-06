# LITRevu – Application Django

Application web développée avec **Django** permettant aux utilisateurs de :

- Créer des **tickets** (demande de critique)
- Publier des **critiques** (reviews)
- **Suivre** d'autres utilisateurs
- **Bloquer** des utilisateurs
- Consulter un **flux personnalisé** combinant tickets et critiques

Projet réalisé dans le cadre du parcours **Développeur d'application Python – OpenClassrooms**.

---

# ⚙️ Technologies utilisées

- Python 3.12
- Django 6.0.1
- SQLite3
- Bootstrap 5
- Pillow (gestion des images)

---

# 🚀 Installation

## 1️⃣ Cloner le projet

```bash
git clone <url-du-repo>
cd django-web-app
2️⃣ Créer et activer un environnement virtuel
python -m venv env
Windows
env\Scripts\activate
Mac / Linux
source env/bin/activate
3️⃣ Installer les dépendances
pip install -r requirements.txt
4️⃣ Lancer le serveur
cd LITrevu
python manage.py runserver

Accéder à l'application :

http://127.0.0.1:8000/
👤 Comptes de test

(À adapter selon tes comptes)

Utilisateur standard
Username : testuser
Mot de passe : password123
Administrateur
Username : admin1
Mot de passe : admin

Accès interface admin :

http://127.0.0.1:8000/admin/
📌 Fonctionnalités principales
🔹 Gestion des tickets

Création d’un ticket avec titre, description et image optionnelle

Modification et suppression uniquement par l’auteur

Suppression autorisée uniquement via requête POST

🔹 Gestion des critiques

Création d’une critique en réponse à un ticket

Impossible de poster plus d’une critique sur le même ticket

Modification et suppression réservées à l’auteur

🔹 Système d’abonnement

Suivre un utilisateur par nom d’utilisateur

Désabonnement possible

Gestion des erreurs :

utilisateur inexistant

utilisateur déjà suivi

auto-follow interdit

🔹 Système de blocage

Possibilité de bloquer un utilisateur.

Un utilisateur bloqué :

ne peut pas être suivi

n’apparaît plus dans le flux

son contenu est masqué dans les deux sens

🔹 Flux personnalisé

Le flux combine :

les tickets des utilisateurs suivis

les critiques des utilisateurs suivis

les critiques publiées sur les tickets de l’utilisateur connecté

les propres publications de l’utilisateur

Les contenus sont :

fusionnés

annotés pour distinguer Ticket / Review

triés par date antéchronologique

🏗️ Architecture du projet

Le projet est organisé en deux applications Django :

📂 users

Authentification

Templates liés à la connexion

Page feed

📂 reviews

Contient :

modèles Ticket

modèles Review

modèles UserFollows

modèles UserBlock

Gestion de la logique métier.

Les vues sont organisées par domaine :

feed

tickets

reviews

follows

Les vues ont été refactorisées en package pour améliorer la lisibilité et la maintenabilité.

🔐 Sécurité et bonnes pratiques

Accès aux vues protégé via @login_required

Vérification de l’auteur avant modification ou suppression

Suppression possible uniquement via requête POST

Validation des formulaires côté serveur

Utilisation de get_object_or_404

Gestion du blocage via service dédié

📁 Base de données

Le fichier db.sqlite3 est fourni avec des données de test afin de faciliter l’évaluation du projet.

🧠 Points techniques intéressants

Utilisation de Q() pour des requêtes complexes

Fusion de QuerySets avec itertools.chain

Annotation dynamique pour distinguer les types de contenu

Séparation des responsabilités via refactorisation des vues

Gestion du blocage bidirectionnel

📌 Auteur

Aurélien Amorin

Projet réalisé dans le cadre du parcours
Développeur d'application Python – OpenClassrooms
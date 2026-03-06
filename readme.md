# LITRevu – Application Django

Application web développée avec **Django** permettant aux utilisateurs de :

- créer des **tickets** (demande de critique)
- publier des **critiques** (reviews)
- **suivre** d'autres utilisateurs
- **bloquer** des utilisateurs
- consulter un **flux personnalisé** combinant tickets et critiques

Projet réalisé dans le cadre du parcours  
**Développeur d'application Python – OpenClassrooms**

---

# Fonctionnalités principales

## Gestion des utilisateurs

- inscription
- connexion / déconnexion
- suivi d'autres utilisateurs
- blocage d'utilisateurs

## Tickets

Un ticket correspond à une **demande de critique** d’un livre ou d’un article.

Un utilisateur peut :

- créer un ticket
- modifier son ticket
- supprimer son ticket

## Critiques

Un utilisateur peut :

- publier une critique
- répondre à un ticket avec une critique
- modifier sa critique
- supprimer sa critique

## Flux personnalisé

Le flux affiche :

- les tickets de l’utilisateur connecté
- les tickets des utilisateurs suivis
- les critiques des utilisateurs suivis
- les critiques faites sur les tickets de l’utilisateur

Les publications sont triées par **date antéchronologique**.

---

# Technologies utilisées

- Python 3.12
- Django 6.0.1
- SQLite3
- Bootstrap 5
- Pillow

---

# Structure du projet

```
django-web-app/
│
├── env/
├── .env
├── .flake8
├── .gitignore
├── requirements.txt
│
└── LITrevu/
│
├── manage.py
├── db.sqlite3
│
├── LITrevu/
│ ├── settings.py
│ ├── urls.py
│ └── asgi.py / wsgi.py
│
├── users/
│ ├── models.py
│ ├── forms.py
│ ├── views.py
│ ├── urls.py
│ └── templates/
│
├── reviews/
│ ├── models.py
│ ├── forms.py
│ ├── services.py
│ ├── urls.py
│ ├── views/
│ │ ├── feed.py
│ │ ├── tickets.py
│ │ ├── reviews.py
│ │ └── follows.py
│ └── templates/
│
├── templates/
└── media/
```

---

# Installation

## 1. Cloner le projet

```bash
git clone <url-du-repository>
cd django-web-app
```

---

## 2. Créer un environnement virtuel

```bash
python -m venv env
```

### Windows

```
env\Scripts\activate
```

### Mac / Linux

```
source env/bin/activate
```

---

## 3. Installer les dépendances

```
pip install -r requirements.txt
```

---

## 4. Configurer les variables d'environnement

Créer un fichier `.env` à la racine du projet :

```
SECRET_KEY=your_secret_key
DEBUG=True
```

---

## 5. Appliquer les migrations

```
cd LITrevu
python manage.py migrate
```

---

## 6. Lancer le serveur

```
python manage.py runserver
```

Accéder ensuite à :

```
http://127.0.0.1:8000/
```

---

# Comptes de test

Superuser :

```
username : admin1
password : admin
```

Utilisateur standard :

```
username : user2
password : passpassyes
```

---

# Qualité du code

Le projet utilise :

- **Flake8** pour l'analyse statique du code
- **Black** pour le formatage automatique

Configuration présente dans :

```
.flake8
```

---

# Sécurité

- les utilisateurs ne peuvent modifier **que leurs propres tickets**
- les utilisateurs ne peuvent modifier **que leurs propres critiques**
- les suppressions sont autorisées **uniquement via POST**
- système de **blocage d'utilisateurs**
- suppression automatique des relations de suivi lors d'un blocage

---

# Améliorations possibles

- pagination du flux
- système de notifications
- amélioration de l'interface utilisateur
- déploiement (Heroku / Render)

---

# Auteur

Projet réalisé par **Aurélien Amorin**  
dans le cadre du parcours **OpenClassrooms – Développeur d'application Python**
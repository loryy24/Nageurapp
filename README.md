```markdown
# 🏊‍♂️ Nageur – Gestion des historiques de nage

Ce projet Flask permet de gérer les historiques de nage des sportifs, avec visualisation graphique des données et gestion via base de données MySQL.

---

## 📂 Structure du projet

```

Nageur/
│
├── **init**.py              # Initialisation de l'application Flask
├── models.py                # Connexion à la base de données MySQL
├── schema.sql               # Script SQL de création des tables
├── templates/
│   ├── index.html           # Page d’accueil avec formulaire
│   └── historique.html      # Affichage graphique de l’historique
├── static/
│   └── chart.js             # (ou via CDN dans les templates)
├── requirements.txt         # Liste des dépendances Python
└── README.md                # Guide de démarrage

````

---

## ⚙️ Pré-requis

- Python 3.10+
- MySQL (avec phpMyAdmin)
- Un environnement virtuel Python (`venv`)

---

## 🧰 Installation

### 1. Cloner le dépôt

```bash
git clone <lien-du-repo>
cd Nageur
````

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🛠️ Configuration de la base de données

### 1. Créer une base MySQL nommée `nageur_db` (depuis phpMyAdmin)

### 2. Importer le fichier SQL

* Ouvrir phpMyAdmin
* Sélectionner `nageur_db`
* Aller dans l’onglet **Importer**
* Choisir `schema.sql` et exécuter

### 3. Vérifier le contenu de `models.py`

```python
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='votre_mot_de_passe',
    database='nageur_db'
)
```

> 🔒 N'oubliez pas de personnaliser les identifiants de connexion MySQL.

---

## 🚀 Lancer le serveur Flask

```bash
python NageurApp/__init__.py
```

Puis ouvrez votre navigateur à l'adresse :

```
http://localhost:5000
```

---

## 📊 Bibliothèque utilisée pour les graphiques

* [Chart.js (CDN)](https://cdn.jsdelivr.net/npm/chart.js)

> Inclus via `<script src="..."></script>` dans le fichier `historique.html`

---

## ✅ Fait avec

* Flask
* MySQL / phpMyAdmin
* Chart.js
* HTML5 + Jinja2

---

## 🔐 Sécurité

* Aucun mot de passe en clair dans le code.
* Pensez à créer un `.env` pour les déploiements sérieux.

---

## 🧾 Auteurs

> Projet développé par Larissa Chatigre – Août 2025

```


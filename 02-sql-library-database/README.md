# LibraryDB -- Systeme de Gestion de Bibliotheque Relationnelle

> **Outils :** SQLite, SQL, Python, Streamlit, pandas  
> **Duree :** ~6 heures

---

## Problematique metier

Une bibliotheque universitaire a besoin d'un systeme pour gerer son catalogue de livres, suivre les emprunts des lecteurs inscrits et identifier les retards. Le systeme doit permettre des analyses sur les habitudes de lecture, les auteurs les plus presents et l'activite mensuelle.

---

## Objectifs du projet

- Concevoir un schema relationnel normalise (5 tables, cles etrangeres, contraintes)
- Ecrire des requetes SQL analytiques avancees (jointures, agregations, sous-requetes, fonctions de date)
- Creer des vues SQL pour simplifier les analyses recurrentes
- Optimiser les performances avec des index cibles
- Construire une interface interactive Streamlit pour explorer la base en temps reel

---

## Outils et competences mobilisees

| Categorie | Technologies |
|-----------|-------------|
| Base de donnees | SQLite |
| Langage | SQL, Python 3.x |
| Interface | Streamlit |
| Analyse | pandas |
| Modelisation | Schema relationnel normalise (3NF) |
| Optimisation | Index sur colonnes de jointure et de filtre |
| Vues | 4 vues SQL (catalogue, emprunts, statistiques, dashboard) |

---

## Le schema relationnel

| Table | Description | Cle primaire |
|-------|-------------|-------------|
| authors | 15 auteurs (africains et internationaux) | author_id |
| categories | 7 categories (Fiction, Informatique, Histoire, etc.) | category_id |
| books | 20 livres avec ISBN, annee, exemplaires | book_id |
| borrowers | 10 lecteurs inscrits | borrower_id |
| loans | 28 emprunts (19 retournes, 7 en cours, 2 en retard) | loan_id |

### Relations

- `books.author_id` -> `authors.author_id`
- `books.category_id` -> `categories.category_id`
- `loans.book_id` -> `books.book_id`
- `loans.borrower_id` -> `borrowers.borrower_id`

---

## L'application

### Dashboard

![Dashboard](images/dashboard.jpg)
*KPIs globaux (20 livres, 53 exemplaires, 15 auteurs, 10 lecteurs, 28 emprunts, 9 en cours, 2 en retard) et graphiques de repartition.*

### Catalogue

![Catalogue](images/catalogue.jpg)
*Catalogue complet avec recherche par titre ou auteur. Affiche la disponibilite en temps reel.*

### Emprunts actifs

![Emprunts](images/emprunts.jpg)
*Suivi des emprunts en retard (mis en evidence) et des emprunts en cours avec dates d'echeance.*

### Analytique

![Analytique](images/analytique.jpg)
*Auteurs les plus presents, lecteurs les plus actifs, duree moyenne d'emprunt par categorie et activite mensuelle.*

### Console SQL

![Console SQL](images/console-sql.jpg)
*Console interactive pour executer des requetes SQL personnalisees sur la base en lecture seule.*

---

## Requetes SQL implementees

| Requete | Description |
|---------|-------------|
| Q1 | Livres actuellement empruntes avec statut (en cours / en retard) |
| Q2 | Auteurs ayant le plus de livres dans la bibliotheque |
| Q3 | Emprunteurs les plus actifs (total, retournes, en cours) |
| Q4 | Livres les plus empruntes avec categorie |
| Q5 | Emprunts en retard avec nombre de jours de depassement |
| Q6 | Repartition des livres par categorie (nombre et pourcentage) |
| Q7 | Duree moyenne d'emprunt par categorie (min, max, moyenne) |
| Q8 | Activite mensuelle (emprunts, retours, en attente) |

### Vues SQL

| Vue | Description |
|-----|-------------|
| v_catalog | Catalogue complet avec disponibilite sur etagere |
| v_active_loans | Emprunts actifs avec details complets et statut |
| v_author_stats | Statistiques par auteur (livres, exemplaires, emprunts) |
| v_dashboard | Tableau de bord global (KPIs agreges) |

---

## Optimisation

5 index crees pour optimiser les jointures et les filtres frequents :

```sql
CREATE INDEX idx_loans_book ON loans(book_id);
CREATE INDEX idx_loans_borrower ON loans(borrower_id);
CREATE INDEX idx_loans_dates ON loans(loan_date, return_date);
CREATE INDEX idx_books_author ON books(author_id);
CREATE INDEX idx_books_category ON books(category_id);
```

---

## Competences demontrees

- Modelisation relationnelle normalisee
- Requetes SQL avancees (JOIN, GROUP BY, HAVING, sous-requetes, CASE, fonctions de date)
- Creation de vues pour encapsuler la logique metier
- Indexation pour optimisation des performances
- Integration SQL/Python avec sqlite3
- Visualisation interactive avec Streamlit
- Interface bilingue (FR/EN)

---

## Structure du projet

```
02-sql-library-database/
├── app.py                    # Interface Streamlit (bilingue)
├── requirements.txt          # Dependances Python
├── sql/
│   ├── schema.sql            # Schema (5 tables + 5 index)
│   ├── data.sql              # Donnees d'exemple
│   └── queries.sql           # 8 requetes analytiques + 4 vues
├── data/
│   └── library.db            # Base SQLite generee
└── images/
    ├── dashboard.jpg
    ├── catalogue.jpg
    ├── emprunts.jpg
    ├── analytique.jpg
    └── console-sql.jpg
```

---

## Pour reproduire

```bash
git clone https://github.com/barde44/portfolio-data-engineer.git
cd portfolio-data-engineer/02-sql-library-database

pip install -r requirements.txt
python -m streamlit run app.py
```

La base de donnees est automatiquement creee au premier lancement a partir des fichiers SQL.

---

## A propos

Projet realise par **Steven Barde** dans le cadre du portfolio Data Engineer.  
[github.com/barde44/portfolio-data-engineer](https://github.com/barde44/portfolio-data-engineer)

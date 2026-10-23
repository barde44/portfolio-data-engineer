# ReviewScope -- Scraping et analyse d'avis consommateurs

Application de web scraping et d'analyse d'avis consommateurs. Collecte des donnees depuis des sites e-commerce avec BeautifulSoup, stockage structure en SQLite, et visualisation interactive via Streamlit.

## Fonctionnalites

- **Scraping web** : collecte automatisee d'avis avec BeautifulSoup (parsing HTML, nettoyage, extraction structuree)
- **Stockage SQLite** : schema relationnel avec 3 tables, 6 index, 3 vues analytiques
- **Dashboard interactif** : 5 onglets (Dashboard, Produits, Avis, Insights, Console SQL)
- **Interface bilingue** : francais / anglais avec bascule instantanee
- **Mode demo** : generation de donnees realistes (12 produits, 5 categories, ~460 avis)
- **Console SQL** : execution de requetes personnalisees en lecture seule

## Stack technique

| Composant | Technologie |
|-----------|------------|
| Scraping | BeautifulSoup, requests |
| Base de donnees | SQLite |
| Dashboard | Streamlit |
| Analyse | pandas |
| Langage | Python 3.10+ |

## Structure du projet

```
04-web-scraping-reviews/
  scraper.py          # Scraper web + generateur de donnees demo
  app.py              # Dashboard Streamlit
  requirements.txt    # Dependances Python
  sql/
    schema.sql        # Schema de la base (tables, index, vues)
    queries.sql       # 8 requetes analytiques
  data/
    reviews.db        # Base SQLite (generee)
    scraper.log       # Journal de scraping
```

## Installation et lancement

```bash
pip install -r requirements.txt
python scraper.py --demo
streamlit run app.py
```

## Schema de la base

- **sources** : sites e-commerce (Amazon, Best Buy, Walmart)
- **products** : produits avec categorie, marque, source
- **reviews** : avis avec note, auteur, contenu, date, verification

### Vues analytiques

- `v_product_summary` : resume par produit (notes, avis positifs/negatifs)
- `v_rating_distribution` : distribution des notes par produit
- `v_monthly_activity` : activite mensuelle par produit

## Requetes SQL incluses

1. Vue d'ensemble des produits avec resume des notes
2. Distribution des notes par produit
3. Avis les plus utiles
4. Tendances mensuelles
5. Analyse de sentiment par categorie
6. Longueur des avis vs note
7. Achats verifies vs non verifies
8. Classement des marques

## Auteur

Steven Barde -- github.com/barde44

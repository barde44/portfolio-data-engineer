"""ShelfFlow | Bilingual recruiter-ready library showcase.
Independent session data; never writes to CLI JSON storage.
Run: python -m streamlit run app.py
"""
from __future__ import annotations
from datetime import datetime, timezone
from uuid import uuid4
import html
import pandas as pd
import streamlit as st

st.set_page_config(page_title="ShelfFlow | Library Manager", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

COPY = {
 "English": {
  "tag":"YOUR READING SPACE, SIMPLIFIED", "hero":"A smarter home for every book.","desc":"Discover, organize and manage your personal collection in one beautifully simple workspace.",
  "subtitle":"A thoughtfully designed library experience", "nav":"Workspace", "browse":"Explore library", "add":"Add a book", "manage":"Manage books", "insights":"Insights",
  "books":"Books in library","cats":"Categories","authors":"Unique authors", "sidebar_title":"A library that works for you.",
  "sidebar_desc":"Browse your shelves, organize titles and discover insights — all in one place.","privacy":"Private demo — changes only affect your current session.",
  "reset":"Reset demo data","reset_done":"Demo collection restored.","language":"Language / Langue","search":"Search books","search_hint":"Search title or author…","category":"Category",
  "all":"All categories","sort":"Sort by","az":"Title: A to Z","za":"Title: Z to A","new":"Newest first","old":"Oldest first","bycat":"Category: A to Z",
  "showing":"Showing {shown} of {total} books","empty":"No books match your filters.","no_books":"Your collection is empty. Add your first book.",
  "title":"Title","author":"Author","added":"Added","collection":"Your collection","add_head":"Add something worth reading","add_help":"Every great library starts with a great book.",
  "book_title":"Book title","book_placeholder":"e.g. The Data Warehouse Toolkit","author_placeholder":"e.g. Ralph Kimball","cat_placeholder":"e.g. Data Warehousing","submit":"Add to library",
  "required":"Please complete all fields.","duplicate":"This title already exists in your collection.","added_ok":"Book added to your library.",
  "manage_head":"Keep your shelves up to date","manage_help":"Update details or remove a book from your demo collection.","choose":"Select a book","save":"Save changes","saved":"Changes saved. The original added date was preserved.",
  "delete_heading":"Remove book","delete_help":"This will remove the selected title from your current demo session.","confirm":"I understand and want to remove this book","delete":"Delete book","deleted":"Book removed.",
  "insights_head":"A closer look at your library","insights_help":"A quick overview of how your books are organized.","cat_chart":"Books by category","chart_note":"Updated live from this browser session.",
  "footer":"Crafted for curious readers · ShelfFlow demo · No account required", "status":"LIVE DEMO", "hint":"Explore a fully interactive sample library", "error":"Something went wrong.",
 },
 "Français": {
  "tag":"VOTRE BIBLIOTHÈQUE, EN TOUTE SIMPLICITÉ", "hero":"Tous vos livres, au même endroit.","desc":"Découvrez, organisez et gérez votre collection personnelle dans un espace élégant et intuitif.",
  "subtitle":"Une expérience de lecture pensée pour vous", "nav":"Espace de travail", "browse":"Explorer les livres", "add":"Ajouter un livre", "manage":"Gérer les livres", "insights":"Statistiques",
  "books":"Livres dans la collection","cats":"Catégories","authors":"Auteurs uniques", "sidebar_title":"Une bibliothèque à votre image.",
  "sidebar_desc":"Parcourez, classez et explorez votre collection depuis un seul espace.","privacy":"Démo privée : les modifications restent limitées à votre session.",
  "reset":"Réinitialiser la démo","reset_done":"Collection de démonstration restaurée.","language":"Langue / Language","search":"Rechercher un livre","search_hint":"Titre ou auteur…","category":"Catégorie",
  "all":"Toutes les catégories","sort":"Trier par","az":"Titre : A à Z","za":"Titre : Z à A","new":"Plus récents","old":"Plus anciens","bycat":"Catégorie : A à Z",
  "showing":"{shown} livre(s) sur {total}","empty":"Aucun livre ne correspond aux filtres.","no_books":"Votre collection est vide. Ajoutez votre premier livre.",
  "title":"Titre","author":"Auteur","added":"Ajouté le","collection":"Votre collection","add_head":"Ajoutez votre prochaine lecture","add_help":"Chaque grande bibliothèque commence par un livre.",
  "book_title":"Titre du livre","book_placeholder":"Ex. The Data Warehouse Toolkit","author_placeholder":"Ex. Ralph Kimball","cat_placeholder":"Ex. Ingénierie des données","submit":"Ajouter à la bibliothèque",
  "required":"Veuillez remplir tous les champs.","duplicate":"Ce titre existe déjà dans la collection.","added_ok":"Livre ajouté à votre bibliothèque.",
  "manage_head":"Gardez votre bibliothèque à jour","manage_help":"Modifiez les informations ou supprimez un livre de la démo.","choose":"Sélectionner un livre","save":"Enregistrer les modifications","saved":"Modifications enregistrées. La date d'ajout initiale a été conservée.",
  "delete_heading":"Supprimer le livre","delete_help":"Ce titre sera supprimé uniquement de votre session de démonstration.","confirm":"Je confirme vouloir supprimer ce livre","delete":"Supprimer le livre","deleted":"Livre supprimé.",
  "insights_head":"Votre bibliothèque en chiffres","insights_help":"Visualisez la répartition de votre collection.","cat_chart":"Livres par catégorie","chart_note":"Données actualisées en direct pour cette session.",
  "footer":"Conçu pour les lecteurs curieux · Démo ShelfFlow · Sans inscription", "status":"DÉMO EN DIRECT", "hint":"Testez une bibliothèque entièrement interactive", "error":"Une erreur est survenue.",
 }
}
SAMPLES = [
 ("Fundamentals of Data Engineering", "Joe Reis & Matt Housley", "Data Engineering"),
 ("Designing Data-Intensive Applications", "Martin Kleppmann", "Distributed Systems"),
 ("Python Crash Course", "Eric Matthes", "Programming"),
 ("Clean Code", "Robert C. Martin", "Software Engineering"),
 ("Data Engineering with Python", "Paul Crickard", "Data Engineering"),
]
def create_book(title,author,category):
 return {"id":str(uuid4()),"title":title.strip(),"author":author.strip(),"category":category.strip(),"date_added":datetime.now(timezone.utc).isoformat(timespec="seconds")}
def starter_books(): return [create_book(*x) for x in SAMPLES]
if "books" not in st.session_state: st.session_state.books=starter_books()
if "lang" not in st.session_state: st.session_state.lang="English"
if "notice" not in st.session_state: st.session_state.notice=None

def duplicate(title, exclude=None):
 return any(b["title"].casefold()==title.strip().casefold() and b["id"]!=exclude for b in st.session_state.books)
def inform(message,kind="success"):
 st.session_state.notice=(message,kind)
 st.rerun()
def safe(value): return html.escape(str(value),quote=True)

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--ink:#172B40;--muted:#64788B;--navy:#101F33;--teal:#087F79;--line:#E3EAF0;--bg:#F5F8FB}
html,body,[data-testid="stApp"]{font-family:'DM Sans',sans-serif!important;color:var(--ink)!important}
[data-testid="stAppViewContainer"],.stApp{background:var(--bg)!important}
[data-testid="stHeader"]{background:transparent!important}
[data-testid="stSidebar"]{background:var(--navy)!important;border-right:1px solid #284057}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,[data-testid="stSidebar"] label,[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3{color:#F2F6FA!important}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{color:#A9BDCE!important}
[data-testid="stSidebar"] [data-testid="stAlert"]{background:#1D354B!important;color:white!important}
[data-testid="stSidebar"] [data-testid="stAlert"] p{color:#E3EEF5!important}
.block-container{max-width:1360px!important;padding:1.9rem 3rem 3rem!important}
h1,h2,h3{font-family:'Manrope',sans-serif!important;letter-spacing:-.04em!important;color:var(--ink)!important}
.shelf-logo{display:flex;align-items:center;gap:12px;padding:10px 0 3px}.logo-symbol{width:43px;height:43px;border-radius:13px;background:#17A89B;color:white;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:800}.logo-text{font-family:Manrope;font-size:26px;font-weight:800;color:#fff;letter-spacing:-1px}
.sidebar-hint{font-size:12px;color:#B4C7D8;line-height:1.8;padding:3px 0 20px}
.sidebar-card{border:1px solid #35516A;background:#19314A;border-radius:16px;padding:20px;margin:20px 0}.sidebar-card h4{color:white;margin:0 0 8px;font-family:Manrope;font-size:16px}.sidebar-card p{color:#C6D6E3;margin:0;line-height:1.65;font-size:13px}
.mini-status{display:inline-flex;align-items:center;gap:8px;color:#BCEDE7;font-size:11px;font-weight:700;letter-spacing:.08em;border:1px solid #346F70;border-radius:30px;padding:8px 12px;margin:16px 0}.status-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#45E0C4}
.hero-new{background:#112B40;border-radius:22px;padding:34px 42px;margin:3px 0 25px;position:relative;overflow:hidden;border:1px solid #29485D}.hero-new:after{content:"";position:absolute;width:260px;height:260px;border:1px solid #315369;border-radius:50%;right:-92px;top:-130px;box-shadow:0 0 0 35px #ffffff06,0 0 0 80px #ffffff04;pointer-events:none}
.hero-eyebrow{font-size:11px;color:#73DBCE;font-weight:800;letter-spacing:.16em;margin-bottom:13px}.hero-new h1{color:#fff!important;font-size:clamp(26px,3vw,43px)!important;line-height:1.18!important;margin:0 0 12px!important;max-width:900px}.hero-new p{color:#D0DEE8;font-size:15px;line-height:1.8;max-width:690px;margin:0}
.section-bar{display:flex;justify-content:space-between;align-items:center;gap:10px;margin:27px 0 14px}.section-bar h3{font-size:18px;margin:0!important}.section-bar span{color:#6D8091;font-size:12px}
[data-testid="stMetric"]{background:#fff!important;border:1px solid var(--line);border-radius:16px;padding:20px 22px;box-shadow:0 5px 16px #192e4010}
[data-testid="stMetricLabel"] p{font-size:13px!important;color:#6A7F91!important;font-weight:600!important}
[data-testid="stMetricValue"]{color:#142A40!important;font-family:Manrope;font-weight:800!important}
.stTabs [data-baseweb="tab-list"]{gap:10px!important;background:#fff!important;border:1px solid #E3EAF0!important;padding:8px!important;border-radius:14px!important;flex-wrap:wrap!important}
.stTabs [data-baseweb="tab"]{background:transparent!important;border-radius:9px!important;color:#435B70!important;font-weight:700!important;padding:10px 15px!important;height:auto!important}
.stTabs [aria-selected="true"]{background:#E4F5F2!important;color:#076F68!important}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important}
.stTabs [data-testid="stTabContent"]{padding-top:20px!important}
[data-testid="stWidgetLabel"] p{color:#294156!important;font-weight:600!important}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:12px;overflow:hidden}
[data-testid="stForm"]{border:1px solid var(--line);border-radius:16px;background:#fff;padding:24px}
.stButton>button[kind="primary"], [data-testid="stFormSubmitButton"] button[kind="primary"]{background:var(--teal)!important;color:white!important;border:1px solid var(--teal)!important}
.stButton>button,[data-testid="stFormSubmitButton"] button{border-radius:10px!important;font-weight:700!important;min-height:43px}
.stButton>button:hover{border-color:var(--teal)!important;color:var(--teal)}
[data-testid="stSidebar"] .stButton>button{background:#25435C!important;color:white!important;border-color:#42627D!important}
[data-testid="stSidebar"] .stButton>button:hover{background:#325770!important}
.footer-new{margin-top:40px;padding-top:22px;border-top:1px solid #DDE6EC;font-size:12px;color:#788B9B;text-align:center}
@media(max-width:800px){.block-container{padding:1.3rem 1rem 2rem!important}.hero-new{padding:26px 22px}.stTabs [data-baseweb="tab"]{padding:9px!important}}
</style>""",unsafe_allow_html=True)

with st.sidebar:
 st.markdown('<div class="shelf-logo"><div class="logo-symbol">S</div><div class="logo-text">ShelfFlow</div></div>',unsafe_allow_html=True)
 st.session_state.lang=st.selectbox("Language / Langue",["English","Français"],index=["English","Français"].index(st.session_state.lang))
 t=COPY[st.session_state.lang]
 st.markdown(f'<div class="mini-status"><span class="status-dot"></span>{safe(t["status"])}</div>',unsafe_allow_html=True)
 st.markdown(f'<div class="sidebar-hint">{safe(t["hint"])}</div>',unsafe_allow_html=True)
 st.markdown(f'<div class="sidebar-card"><h4>{safe(t["sidebar_title"])}</h4><p>{safe(t["sidebar_desc"])}</p></div>',unsafe_allow_html=True)
 st.info("🔒  "+t["privacy"])
 if st.button("↻  "+t["reset"],use_container_width=True):
  st.session_state.books=starter_books()
  inform(t["reset_done"])
 st.caption("Python · Streamlit · CRUD · Session data")

t=COPY[st.session_state.lang]
st.markdown(f'<div class="hero-new"><div class="hero-eyebrow">{safe(t["tag"])}</div><h1>{safe(t["hero"])}</h1><p>{safe(t["desc"])}</p></div>',unsafe_allow_html=True)
if st.session_state.notice:
 message,kind=st.session_state.notice
 if kind=="error": st.error(message)
 else: st.success(message)
 st.session_state.notice=None
books=st.session_state.books
cats=sorted({b["category"] for b in books},key=str.casefold)
authors={b["author"].casefold() for b in books}
a,b,c=st.columns(3)
a.metric(t["books"],len(books)); b.metric(t["cats"],len(cats)); c.metric(t["authors"],len(authors))
st.markdown(f'<div class="section-bar"><h3>{safe(t["nav"])}</h3><span>{safe(t["subtitle"])}</span></div>',unsafe_allow_html=True)
explore,add,manage,insights=st.tabs(["▦  "+t["browse"],"＋  "+t["add"],"✎  "+t["manage"],"◫  "+t["insights"]])
with explore:
 s1,s2,s3=st.columns([2.0,1.2,1.45])
 with s1: query=st.text_input(t["search"],placeholder=t["search_hint"])
 with s2: cat=st.selectbox(t["category"],[t["all"]]+cats)
 with s3:
  sort_keys=["az","za","new","old","bycat"]
  sort=st.selectbox(t["sort"],sort_keys,format_func=lambda k:t[k])
 found=[b for b in books if (not query.strip() or query.strip().casefold() in b["title"].casefold() or query.strip().casefold() in b["author"].casefold()) and (cat==t["all"] or b["category"]==cat)]
 if sort=="az": found.sort(key=lambda x:x["title"].casefold())
 elif sort=="za": found.sort(key=lambda x:x["title"].casefold(),reverse=True)
 elif sort=="new": found.sort(key=lambda x:x["date_added"],reverse=True)
 elif sort=="old": found.sort(key=lambda x:x["date_added"])
 else: found.sort(key=lambda x:(x["category"].casefold(),x["title"].casefold()))
 st.caption(t["showing"].format(shown=len(found),total=len(books)))
 if found:
  st.dataframe(pd.DataFrame([{t["title"]:x["title"],t["author"]:x["author"],t["category"]:x["category"],t["added"]:x["date_added"][:10]} for x in found]),use_container_width=True,hide_index=True)
 else: st.info(t["empty"] if books else t["no_books"])
with add:
 st.subheader(t["add_head"]);st.caption(t["add_help"])
 with st.form("add_form",clear_on_submit=True):
  title=st.text_input(t["book_title"],placeholder=t["book_placeholder"])
  author=st.text_input(t["author"],placeholder=t["author_placeholder"])
  category=st.text_input(t["category"],placeholder=t["cat_placeholder"])
  submitted=st.form_submit_button(t["submit"],type="primary",use_container_width=True)
 if submitted:
  if not all((title.strip(),author.strip(),category.strip())):st.error(t["required"])
  elif duplicate(title):st.error(t["duplicate"])
  else:
   books.append(create_book(title,author,category));inform(t["added_ok"])
with manage:
 st.subheader(t["manage_head"]);st.caption(t["manage_help"])
 if not books:st.info(t["no_books"])
 else:
  id=st.selectbox(t["choose"],[b["id"] for b in books],format_func=lambda id:next(b["title"]+"  ·  "+b["author"] for b in books if b["id"]==id))
  selected=next(x for x in books if x["id"]==id)
  with st.form(f"edit_form_{id}"):
   edit_title=st.text_input(t["book_title"],value=selected["title"])
   edit_author=st.text_input(t["author"],value=selected["author"])
   edit_cat=st.text_input(t["category"],value=selected["category"])
   save=st.form_submit_button(t["save"],type="primary",use_container_width=True)
  if save:
   if not all((edit_title.strip(),edit_author.strip(),edit_cat.strip())):st.error(t["required"])
   elif duplicate(edit_title,exclude=id):st.error(t["duplicate"])
   else:
    selected.update(title=edit_title.strip(),author=edit_author.strip(),category=edit_cat.strip());inform(t["saved"])
  st.divider();st.markdown("#### "+t["delete_heading"]);st.caption(t["delete_help"])
  confirm=st.checkbox(t["confirm"],key="delete_confirm_"+id)
  if st.button(t["delete"],disabled=not confirm,use_container_width=True):
   st.session_state.books=[b for b in books if b["id"]!=id];inform(t["deleted"])
with insights:
 st.subheader(t["insights_head"]);st.caption(t["insights_help"])
 if not books:st.info(t["no_books"])
 else:
  st.markdown("**"+t["cat_chart"]+"**")
  frame=pd.DataFrame([{t["category"]:x,"Count":sum(y["category"]==x for y in books)} for x in cats])
  st.bar_chart(frame.set_index(t["category"]),horizontal=True,color="#087F79",x_label="",y_label="")
  st.caption(t["chart_note"])
st.markdown(f'<div class="footer-new">{safe(t["footer"])}</div>',unsafe_allow_html=True)

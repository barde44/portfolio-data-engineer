"""LibraryDB -- Interactive SQL Library Explorer (Streamlit)."""

import sqlite3
import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "library.db")
SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")

COPY = {
    "fr": {
        "title": "LibraryDB",
        "subtitle": "Systeme de gestion de bibliotheque relationnelle",
        "tab_dashboard": "Dashboard",
        "tab_catalog": "Catalogue",
        "tab_loans": "Emprunts actifs",
        "tab_analytics": "Analytique",
        "tab_sql": "Console SQL",
        "kpi_books": "Livres",
        "kpi_copies": "Exemplaires",
        "kpi_authors": "Auteurs",
        "kpi_borrowers": "Lecteurs",
        "kpi_loans": "Emprunts",
        "kpi_active": "En cours",
        "kpi_overdue": "En retard",
        "kpi_categories": "Categories",
        "top_borrowed": "Livres les plus empruntes",
        "by_category": "Livres par categorie",
        "monthly": "Activite mensuelle",
        "top_authors": "Auteurs les plus presents",
        "top_borrowers": "Lecteurs les plus actifs",
        "avg_duration": "Duree moyenne d'emprunt par categorie (jours)",
        "search": "Rechercher dans le catalogue...",
        "overdue": "Emprunts en retard",
        "current": "Emprunts en cours",
        "sql_label": "Ecrivez votre requete SQL",
        "sql_run": "Executer",
        "sql_info": "Base SQLite en lecture seule. Essayez : SELECT * FROM v_catalog;",
        "lang": "EN",
    },
    "en": {
        "title": "LibraryDB",
        "subtitle": "Relational Library Management System",
        "tab_dashboard": "Dashboard",
        "tab_catalog": "Catalog",
        "tab_loans": "Active Loans",
        "tab_analytics": "Analytics",
        "tab_sql": "SQL Console",
        "kpi_books": "Books",
        "kpi_copies": "Copies",
        "kpi_authors": "Authors",
        "kpi_borrowers": "Readers",
        "kpi_loans": "Loans",
        "kpi_active": "Active",
        "kpi_overdue": "Overdue",
        "kpi_categories": "Categories",
        "top_borrowed": "Most borrowed books",
        "by_category": "Books by category",
        "monthly": "Monthly activity",
        "top_authors": "Top authors",
        "top_borrowers": "Most active readers",
        "avg_duration": "Average loan duration by category (days)",
        "search": "Search the catalog...",
        "overdue": "Overdue loans",
        "current": "Current loans",
        "sql_label": "Write your SQL query",
        "sql_run": "Execute",
        "sql_info": "Read-only SQLite database. Try: SELECT * FROM v_catalog;",
        "lang": "FR",
    },
}


def init_db():
    """Create and populate the database if it doesn't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        return
    conn = sqlite3.connect(DB_PATH)
    with open(os.path.join(SQL_DIR, "schema.sql"), encoding="utf-8") as f:
        conn.executescript(f.read())
    with open(os.path.join(SQL_DIR, "data.sql"), encoding="utf-8") as f:
        conn.executescript(f.read())
    with open(os.path.join(SQL_DIR, "queries.sql"), encoding="utf-8") as f:
        script = f.read()
        views = script.split("-- VUES")[1] if "-- VUES" in script else ""
        if views:
            conn.executescript(views)
    conn.close()


def get_conn():
    """Return a read-only connection."""
    return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)


def query(sql, conn=None):
    """Execute a SELECT and return a DataFrame."""
    c = conn or get_conn()
    try:
        return pd.read_sql_query(sql, c)
    finally:
        if conn is None:
            c.close()


CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1100px;
    padding-top: 1rem !important;
    padding-bottom: 2rem;
}

/* Header */
.app-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.app-header h1 {
    margin: 0;
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
}
.app-header p {
    margin: 4px 0 0;
    font-size: 14px;
    color: #94a3b8;
    font-weight: 400;
}

/* Lang button */
.lang-btn {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 6px;
    padding: 6px 16px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    letter-spacing: 0.5px;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #1e293b 0%, #1a1a2e 100%);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    border-color: #3b82f6;
}
.kpi-label {
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #94a3b8;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
}
.kpi-value.accent { color: #3b82f6; }
.kpi-value.success { color: #22c55e; }
.kpi-value.warning { color: #f59e0b; }
.kpi-value.danger { color: #ef4444; }

/* Section headers */
.section-title {
    font-size: 16px;
    font-weight: 600;
    color: #1e293b;
    margin: 24px 0 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Overdue badge */
.badge-overdue {
    display: inline-block;
    background: #dc2626;
    color: #fff;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-active {
    display: inline-block;
    background: #2563eb;
    color: #fff;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
}

/* SQL console */
.sql-hint {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 13px;
    color: #475569;
    margin-bottom: 16px;
}
.sql-hint code {
    background: #e2e8f0;
    padding: 2px 6px;
    border-radius: 4px;
    color: #2563eb;
    font-size: 12px;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #f1f5f9;
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    padding: 10px 20px;
    font-weight: 600;
    font-size: 14px;
    border-radius: 8px;
    color: #64748b;
}
.stTabs [aria-selected="true"] {
    background: #1e293b !important;
    color: #ffffff !important;
}

/* DataFrames */
[data-testid="stDataFrame"] {
    border-radius: 8px;
    overflow: hidden;
}

/* Metrics override */
[data-testid="stMetric"] {
    display: none;
}

/* Chart area */
[data-testid="stArrowVegaLiteChart"] {
    border-radius: 8px;
    overflow: hidden;
}

/* Dividers */
hr {
    border-color: #e2e8f0 !important;
    margin: 20px 0 !important;
}

/* Fixed tabs clone */
#sticky-tabs-clone {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 9999999;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 8px 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
#sticky-tabs-clone .sticky-inner {
    max-width: 1100px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 16px;
}
#sticky-tabs-clone .sticky-title {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    white-space: nowrap;
}
#sticky-tabs-clone .sticky-tab-list {
    display: flex;
    gap: 4px;
    background: rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 3px;
}
#sticky-tabs-clone .sticky-tab {
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 600;
    color: #94a3b8;
    border-radius: 6px;
    cursor: pointer;
    border: none;
    background: transparent;
    transition: background 0.15s, color 0.15s;
}
#sticky-tabs-clone .sticky-tab:hover {
    color: #e2e8f0;
}
#sticky-tabs-clone .sticky-tab.active {
    background: rgba(255,255,255,0.2);
    color: #ffffff;
}
</style>
"""


def render_kpi(label, value, style=""):
    css_class = f"kpi-value {style}" if style else "kpi-value"
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="{css_class}">{value}</div>
    </div>
    """


def render_header(title, subtitle, lang_label):
    return f"""
    <div class="app-header">
        <div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        <span class="lang-btn">{lang_label}</span>
    </div>
    """


def main():
    st.set_page_config(page_title="LibraryDB", page_icon="", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    init_db()

    if "lang" not in st.session_state:
        st.session_state.lang = "fr"
    t = COPY[st.session_state.lang]

    col_h, col_b = st.columns([9, 1])
    with col_h:
        st.markdown(render_header(t["title"], t["subtitle"], t["lang"]), unsafe_allow_html=True)
    with col_b:
        st.write("")
        st.write("")
        if st.button(t["lang"], key="lang_btn"):
            st.session_state.lang = "en" if st.session_state.lang == "fr" else "fr"
            st.rerun()

    tabs = st.tabs([
        t["tab_dashboard"], t["tab_catalog"], t["tab_loans"],
        t["tab_analytics"], t["tab_sql"]
    ])

    # -- Dashboard --
    with tabs[0]:
        dash = query("SELECT * FROM v_dashboard").iloc[0]

        row1 = st.columns(4)
        row1[0].markdown(render_kpi(t["kpi_books"], int(dash["total_books"]), "accent"), unsafe_allow_html=True)
        row1[1].markdown(render_kpi(t["kpi_copies"], int(dash["total_copies"])), unsafe_allow_html=True)
        row1[2].markdown(render_kpi(t["kpi_authors"], int(dash["total_authors"])), unsafe_allow_html=True)
        row1[3].markdown(render_kpi(t["kpi_borrowers"], int(dash["total_borrowers"])), unsafe_allow_html=True)

        row2 = st.columns(4)
        row2[0].markdown(render_kpi(t["kpi_loans"], int(dash["total_loans"])), unsafe_allow_html=True)
        row2[1].markdown(render_kpi(t["kpi_active"], int(dash["active_loans"]), "success"), unsafe_allow_html=True)
        row2[2].markdown(render_kpi(t["kpi_overdue"], int(dash["overdue_loans"]), "danger"), unsafe_allow_html=True)
        row2[3].markdown(render_kpi(t["kpi_categories"], int(dash["total_categories"])), unsafe_allow_html=True)

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="section-title">{t["by_category"]}</div>', unsafe_allow_html=True)
            cat_df = query("""
                SELECT c.name AS category, COUNT(b.book_id) AS count
                FROM categories c LEFT JOIN books b ON c.category_id = b.category_id
                GROUP BY c.category_id ORDER BY count DESC
            """)
            st.bar_chart(cat_df.set_index("category"), color="#3b82f6")
        with c2:
            st.markdown(f'<div class="section-title">{t["top_borrowed"]}</div>', unsafe_allow_html=True)
            top = query("""
                SELECT b.title, COUNT(l.loan_id) AS loans
                FROM books b JOIN loans l ON b.book_id = l.book_id
                GROUP BY b.book_id ORDER BY loans DESC LIMIT 8
            """)
            st.bar_chart(top.set_index("title"), color="#8b5cf6")

    # -- Catalogue --
    with tabs[1]:
        search = st.text_input(t["search"], key="cat_search", label_visibility="collapsed", placeholder=t["search"])
        where = ""
        if search:
            safe = search.replace("'", "''")
            where = f"WHERE title LIKE '%{safe}%' OR author LIKE '%{safe}%'"
        catalog = query(f"SELECT * FROM v_catalog {where} ORDER BY title")
        st.dataframe(
            catalog,
            use_container_width=True,
            hide_index=True,
            column_config={
                "book_id": st.column_config.NumberColumn("ID", width="small"),
                "title": st.column_config.TextColumn("Titre" if st.session_state.lang == "fr" else "Title", width="large"),
                "author": st.column_config.TextColumn("Auteur" if st.session_state.lang == "fr" else "Author", width="medium"),
                "category": st.column_config.TextColumn("Categorie" if st.session_state.lang == "fr" else "Category"),
                "isbn": st.column_config.TextColumn("ISBN"),
                "publication_year": st.column_config.NumberColumn("Annee" if st.session_state.lang == "fr" else "Year", format="%d"),
                "copies_available": st.column_config.NumberColumn("Stock", width="small"),
                "copies_on_shelf": st.column_config.NumberColumn("Dispo" if st.session_state.lang == "fr" else "Avail.", width="small"),
            }
        )
        st.caption(f"{len(catalog)} {'livres' if st.session_state.lang == 'fr' else 'books'}")

    # -- Emprunts actifs --
    with tabs[2]:
        overdue = query("SELECT * FROM v_active_loans WHERE status = 'EN RETARD' ORDER BY days_overdue DESC")
        if not overdue.empty:
            st.markdown(f'<div class="section-title">{t["overdue"]} <span class="badge-overdue">{len(overdue)}</span></div>', unsafe_allow_html=True)
            st.dataframe(
                overdue,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "loan_id": st.column_config.NumberColumn("ID", width="small"),
                    "title": st.column_config.TextColumn("Titre" if st.session_state.lang == "fr" else "Title", width="large"),
                    "author": st.column_config.TextColumn("Auteur" if st.session_state.lang == "fr" else "Author"),
                    "borrower": st.column_config.TextColumn("Emprunteur" if st.session_state.lang == "fr" else "Borrower"),
                    "loan_date": st.column_config.DateColumn("Emprunt" if st.session_state.lang == "fr" else "Borrowed"),
                    "due_date": st.column_config.DateColumn("Echeance" if st.session_state.lang == "fr" else "Due"),
                    "days_overdue": st.column_config.NumberColumn("Retard (j)" if st.session_state.lang == "fr" else "Overdue (d)", width="small"),
                    "status": None,
                    "isbn": None,
                    "email": None,
                }
            )
            st.markdown("---")

        current = query("SELECT * FROM v_active_loans WHERE status != 'EN RETARD' ORDER BY due_date")
        st.markdown(f'<div class="section-title">{t["current"]} <span class="badge-active">{len(current)}</span></div>', unsafe_allow_html=True)
        st.dataframe(
            current,
            use_container_width=True,
            hide_index=True,
            column_config={
                "loan_id": st.column_config.NumberColumn("ID", width="small"),
                "title": st.column_config.TextColumn("Titre" if st.session_state.lang == "fr" else "Title", width="large"),
                "author": st.column_config.TextColumn("Auteur" if st.session_state.lang == "fr" else "Author"),
                "borrower": st.column_config.TextColumn("Emprunteur" if st.session_state.lang == "fr" else "Borrower"),
                "loan_date": st.column_config.DateColumn("Emprunt" if st.session_state.lang == "fr" else "Borrowed"),
                "due_date": st.column_config.DateColumn("Echeance" if st.session_state.lang == "fr" else "Due"),
                "status": st.column_config.TextColumn("Statut" if st.session_state.lang == "fr" else "Status"),
                "days_overdue": None,
                "isbn": None,
                "email": None,
            }
        )

    # -- Analytique --
    with tabs[3]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="section-title">{t["top_authors"]}</div>', unsafe_allow_html=True)
            authors = query("SELECT author, total_books, total_loans FROM v_author_stats ORDER BY total_loans DESC LIMIT 8")
            st.dataframe(
                authors,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "author": st.column_config.TextColumn("Auteur" if st.session_state.lang == "fr" else "Author", width="large"),
                    "total_books": st.column_config.NumberColumn("Livres" if st.session_state.lang == "fr" else "Books"),
                    "total_loans": st.column_config.ProgressColumn(
                        "Emprunts" if st.session_state.lang == "fr" else "Loans",
                        min_value=0,
                        max_value=int(authors["total_loans"].max()) if not authors.empty else 1,
                        format="%d",
                    ),
                }
            )

        with c2:
            st.markdown(f'<div class="section-title">{t["top_borrowers"]}</div>', unsafe_allow_html=True)
            borrowers = query("""
                SELECT br.first_name || ' ' || br.last_name AS reader,
                       COUNT(l.loan_id) AS total_loans
                FROM borrowers br JOIN loans l ON br.borrower_id = l.borrower_id
                GROUP BY br.borrower_id ORDER BY total_loans DESC LIMIT 8
            """)
            st.dataframe(
                borrowers,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "reader": st.column_config.TextColumn("Lecteur" if st.session_state.lang == "fr" else "Reader", width="large"),
                    "total_loans": st.column_config.ProgressColumn(
                        "Emprunts" if st.session_state.lang == "fr" else "Loans",
                        min_value=0,
                        max_value=int(borrowers["total_loans"].max()) if not borrowers.empty else 1,
                        format="%d",
                    ),
                }
            )

        st.markdown("---")
        st.markdown(f'<div class="section-title">{t["avg_duration"]}</div>', unsafe_allow_html=True)
        dur = query("""
            SELECT c.name AS category,
                   ROUND(AVG(julianday(l.return_date) - julianday(l.loan_date)), 1) AS avg_days
            FROM loans l JOIN books b ON l.book_id = b.book_id
            JOIN categories c ON b.category_id = c.category_id
            WHERE l.return_date IS NOT NULL
            GROUP BY c.category_id ORDER BY avg_days DESC
        """)
        st.bar_chart(dur.set_index("category"), color="#f59e0b")

        st.markdown("---")
        st.markdown(f'<div class="section-title">{t["monthly"]}</div>', unsafe_allow_html=True)
        monthly = query("""
            SELECT strftime('%Y-%m', loan_date) AS month, COUNT(*) AS loans
            FROM loans GROUP BY month ORDER BY month
        """)
        st.area_chart(monthly.set_index("month"), color="#22c55e")

    # -- Console SQL --
    with tabs[4]:
        st.markdown(f'<div class="sql-hint">{t["sql_info"]}</div>', unsafe_allow_html=True)
        user_sql = st.text_area(t["sql_label"], height=120, key="sql_input",
                                value="SELECT * FROM v_catalog LIMIT 10;")
        if st.button(t["sql_run"], key="sql_btn", type="primary"):
            try:
                result = query(user_sql)
                st.dataframe(result, use_container_width=True, hide_index=True)
                st.caption(f"{len(result)} {'ligne(s)' if st.session_state.lang == 'fr' else 'row(s)'}")
            except Exception as e:
                st.error(str(e))

    STICKY_JS = """
    <script>
    (function() {
        const root = window.parent.document;
        const run = () => {
            const tabList = root.querySelector('[data-baseweb="tab-list"]');
            const scrollContainer = root.querySelector('section[data-testid="stMain"]');
            if (!tabList || !scrollContainer) { setTimeout(run, 500); return; }
            if (root.getElementById('sticky-tabs-clone')) return;

            const tabs = tabList.querySelectorAll('[data-baseweb="tab"]');
            const clone = root.createElement('div');
            clone.id = 'sticky-tabs-clone';
            const inner = root.createElement('div');
            inner.className = 'sticky-inner';
            inner.innerHTML = '<span class="sticky-title">LibraryDB</span>';
            const list = root.createElement('div');
            list.className = 'sticky-tab-list';
            tabs.forEach((tab, i) => {
                const btn = root.createElement('button');
                btn.className = 'sticky-tab' + (tab.getAttribute('aria-selected') === 'true' ? ' active' : '');
                btn.textContent = tab.textContent;
                btn.addEventListener('click', () => { tabs[i].click(); });
                list.appendChild(btn);
            });
            inner.appendChild(list);
            clone.appendChild(inner);
            root.body.appendChild(clone);

            scrollContainer.addEventListener('scroll', () => {
                const rect = tabList.getBoundingClientRect();
                const mainRect = scrollContainer.getBoundingClientRect();
                if (rect.top < mainRect.top) {
                    clone.style.display = 'block';
                    clone.style.top = mainRect.top + 'px';
                    const btns = list.querySelectorAll('.sticky-tab');
                    tabs.forEach((tab, i) => {
                        if (btns[i]) {
                            btns[i].className = 'sticky-tab' + (tab.getAttribute('aria-selected') === 'true' ? ' active' : '');
                        }
                    });
                } else {
                    clone.style.display = 'none';
                }
            });
        };
        setTimeout(run, 800);
    })();
    </script>
    """
    components.html(STICKY_JS, height=0)


if __name__ == "__main__":
    main()

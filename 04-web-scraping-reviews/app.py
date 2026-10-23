"""ReviewScope -- Consumer Review Analytics Dashboard (Streamlit)."""

import sqlite3
import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "reviews.db")
SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")

COPY = {
    "fr": {
        "title": "ReviewScope",
        "subtitle": "Scraping et analyse d'avis consommateurs",
        "tab_dashboard": "Dashboard",
        "tab_products": "Produits",
        "tab_reviews": "Avis",
        "tab_insights": "Insights",
        "tab_sql": "Console SQL",
        "kpi_products": "Produits",
        "kpi_reviews": "Avis",
        "kpi_avg_rating": "Note moyenne",
        "kpi_sources": "Sources",
        "kpi_categories": "Categories",
        "kpi_brands": "Marques",
        "product_overview": "Vue d'ensemble des produits",
        "rating_dist": "Distribution des notes",
        "by_category": "Performance par categorie",
        "by_brand": "Performance par marque",
        "monthly_trends": "Tendances mensuelles",
        "top_reviews": "Avis les plus utiles",
        "verified_comparison": "Achats verifies vs non verifies",
        "review_length": "Longueur des avis par note",
        "select_product": "Selectionnez un produit",
        "select_category": "Selectionnez une categorie",
        "all_categories": "Toutes",
        "sql_label": "Ecrivez votre requete SQL",
        "sql_run": "Executer",
        "sql_info": "Base SQLite en lecture seule. Essayez : SELECT * FROM v_product_summary;",
        "lang": "EN",
        "no_data": "Aucune donnee. Executez d'abord : python scraper.py --demo",
    },
    "en": {
        "title": "ReviewScope",
        "subtitle": "Consumer review scraping and analysis",
        "tab_dashboard": "Dashboard",
        "tab_products": "Products",
        "tab_reviews": "Reviews",
        "tab_insights": "Insights",
        "tab_sql": "SQL Console",
        "kpi_products": "Products",
        "kpi_reviews": "Reviews",
        "kpi_avg_rating": "Avg Rating",
        "kpi_sources": "Sources",
        "kpi_categories": "Categories",
        "kpi_brands": "Brands",
        "product_overview": "Product overview",
        "rating_dist": "Rating distribution",
        "by_category": "Performance by category",
        "by_brand": "Performance by brand",
        "monthly_trends": "Monthly trends",
        "top_reviews": "Most helpful reviews",
        "verified_comparison": "Verified vs unverified purchases",
        "review_length": "Review length by rating",
        "select_product": "Select a product",
        "select_category": "Select a category",
        "all_categories": "All",
        "sql_label": "Write your SQL query",
        "sql_run": "Execute",
        "sql_info": "Read-only SQLite database. Try: SELECT * FROM v_product_summary;",
        "lang": "FR",
        "no_data": "No data. Run first: python scraper.py --demo",
    },
}


def ensure_db():
    return os.path.exists(DB_PATH)


def get_conn():
    return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)


def query(sql, params=None):
    conn = get_conn()
    try:
        return pd.read_sql_query(sql, conn, params=params or {})
    finally:
        conn.close()


CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.block-container { max-width: 1100px; padding-top: 1rem !important; padding-bottom: 2rem; }

.app-header {
    background: linear-gradient(135deg, #1a0533 0%, #2d1b69 50%, #6c3483 100%);
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.app-header h1 { margin: 0; font-size: 28px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px; }
.app-header p { margin: 4px 0 0; font-size: 14px; color: #c39bd3; font-weight: 400; }

.kpi-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 16px; }
.kpi-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px; text-align: center; }
.kpi-card .value { font-size: 26px; font-weight: 700; color: #2d1b69; margin: 0; line-height: 1.2; }
.kpi-card .label { font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }

.section-title { font-size: 16px; font-weight: 600; color: #1e293b; margin: 20px 0 10px; padding-bottom: 6px; border-bottom: 2px solid #6c3483; display: inline-block; }

.styled-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 8px; }
.styled-table thead th { background: #1a0533; color: #ffffff; padding: 10px 12px; text-align: left; font-weight: 600; font-size: 12px; text-transform: uppercase; letter-spacing: 0.3px; }
.styled-table tbody td { padding: 9px 12px; border-bottom: 1px solid #e2e8f0; color: #334155; }
.styled-table tbody tr:hover { background: #f5f0ff; }
.styled-table tbody tr:nth-child(even) { background: #f8fafc; }

.star { color: #f59e0b; }
.star-empty { color: #d1d5db; }

#sticky-tabs-clone {
    display: none; position: fixed; left: 0; right: 0; z-index: 9999999;
    background: #1a0533; padding: 8px 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
#sticky-tabs-clone .clone-title { color: #c39bd3; font-weight: 600; font-size: 14px; margin-right: 16px; }
#sticky-tabs-clone button { background: transparent; border: none; color: #94a3b8; font-size: 13px; font-weight: 500; padding: 6px 14px; cursor: pointer; border-radius: 4px; margin-right: 2px; }
#sticky-tabs-clone button:hover { background: rgba(255,255,255,0.1); }
#sticky-tabs-clone button.active { color: #ffffff; background: rgba(108,52,131,0.3); border-bottom: 2px solid #6c3483; }
</style>
"""


def render_stars(rating):
    full = int(rating)
    html = '<span class="star">' + "&#9733;" * full + '</span>'
    if full < 5:
        html += '<span class="star-empty">' + "&#9733;" * (5 - full) + '</span>'
    return html


def render_kpi(label, value):
    return f'<div class="kpi-card"><p class="value">{value}</p><p class="label">{label}</p></div>'


def tab_dashboard(t):
    stats = query("""SELECT
        COUNT(DISTINCT p.product_id) as products,
        COUNT(r.review_id) as reviews,
        ROUND(AVG(r.rating), 2) as avg_rating,
        COUNT(DISTINCT s.source_id) as sources,
        COUNT(DISTINCT p.category) as categories,
        COUNT(DISTINCT p.brand) as brands
        FROM products p
        JOIN sources s ON s.source_id = p.source_id
        LEFT JOIN reviews r ON r.product_id = p.product_id""")
    row = stats.iloc[0]

    kpis = f"""<div class="kpi-row">
        {render_kpi(t["kpi_products"], int(row["products"]))}
        {render_kpi(t["kpi_reviews"], int(row["reviews"]))}
        {render_kpi(t["kpi_avg_rating"], f'{row["avg_rating"]}/5')}
        {render_kpi(t["kpi_sources"], int(row["sources"]))}
        {render_kpi(t["kpi_categories"], int(row["categories"]))}
        {render_kpi(t["kpi_brands"], int(row["brands"]))}
    </div>"""
    st.markdown(kpis, unsafe_allow_html=True)

    st.markdown(f'<div class="section-title">{t["product_overview"]}</div>', unsafe_allow_html=True)
    summary = query("SELECT * FROM v_product_summary ORDER BY avg_rating DESC")
    if not summary.empty:
        rows_html = ""
        for _, r in summary.iterrows():
            stars = render_stars(r["avg_rating"])
            rows_html += f"""<tr>
                <td><strong>{r["product"]}</strong></td>
                <td>{r["category"]}</td>
                <td>{r["source"]}</td>
                <td>{r["review_count"]}</td>
                <td>{stars} {r["avg_rating"]}</td>
                <td style="color:#22c55e">{int(r["positive"])}</td>
                <td style="color:#ef4444">{int(r["negative"])}</td>
            </tr>"""
        table = f"""<table class="styled-table">
            <thead><tr><th>{"Produit" if t["lang"]=="EN" else "Product"}</th><th>{"Categorie" if t["lang"]=="EN" else "Category"}</th>
            <th>Source</th><th>{"Avis" if t["lang"]=="EN" else "Reviews"}</th>
            <th>Note</th><th>+</th><th>-</th></tr></thead>
            <tbody>{rows_html}</tbody></table>"""
        st.markdown(table, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="section-title">{t["by_category"]}</div>', unsafe_allow_html=True)
        cat = query("""SELECT p.category, COUNT(r.review_id) as reviews, ROUND(AVG(r.rating),2) as avg_rating
            FROM reviews r JOIN products p ON p.product_id=r.product_id GROUP BY p.category ORDER BY avg_rating DESC""")
        if not cat.empty:
            st.bar_chart(cat.set_index("category")["avg_rating"])

    with col2:
        st.markdown(f'<div class="section-title">{t["rating_dist"]}</div>', unsafe_allow_html=True)
        dist = query("SELECT rating, COUNT(*) as count FROM reviews GROUP BY rating ORDER BY rating")
        if not dist.empty:
            st.bar_chart(dist.set_index("rating"))


def tab_products(t):
    categories = [""] + query("SELECT DISTINCT category FROM products ORDER BY category")["category"].tolist()
    cat_labels = [t["all_categories"]] + categories[1:]
    selected_cat = st.selectbox(t["select_category"], cat_labels)

    if selected_cat == t["all_categories"]:
        products = query("SELECT * FROM v_product_summary ORDER BY avg_rating DESC")
    else:
        products = query("SELECT * FROM v_product_summary WHERE category=:cat ORDER BY avg_rating DESC", {"cat": selected_cat})

    if not products.empty:
        st.markdown(f'<div class="section-title">{t["by_brand"]}</div>', unsafe_allow_html=True)
        brand_stats = query("""SELECT p.brand, COUNT(DISTINCT p.product_id) as products,
            COUNT(r.review_id) as reviews, ROUND(AVG(r.rating),2) as avg_rating,
            ROUND(100.0*SUM(CASE WHEN r.rating>=4 THEN 1 ELSE 0 END)/COUNT(*),1) as satisfaction
            FROM products p JOIN reviews r ON r.product_id=p.product_id GROUP BY p.brand ORDER BY avg_rating DESC""")
        st.dataframe(brand_stats, use_container_width=True, hide_index=True)

        st.markdown(f'<div class="section-title">{t["rating_dist"]}</div>', unsafe_allow_html=True)
        st.dataframe(
            query("SELECT * FROM v_rating_distribution"),
            use_container_width=True, hide_index=True
        )


def tab_reviews(t):
    products_list = query("SELECT product_id, name FROM products ORDER BY name")
    selected = st.selectbox(t["select_product"], products_list["name"].tolist())

    if selected:
        pid = products_list[products_list["name"] == selected]["product_id"].iloc[0]

        st.markdown(f'<div class="section-title">{t["top_reviews"]}</div>', unsafe_allow_html=True)
        reviews = query("""SELECT author, rating, title, content, review_date, helpful_count,
            CASE WHEN verified=1 THEN 'Yes' ELSE 'No' END as verified
            FROM reviews WHERE product_id=:pid ORDER BY helpful_count DESC, review_date DESC LIMIT 30""",
            {"pid": int(pid)})

        if not reviews.empty:
            for _, r in reviews.iterrows():
                stars = render_stars(r["rating"])
                verified_badge = ' <span style="color:#22c55e;font-size:11px">[Verified]</span>' if r["verified"] == "Yes" else ""
                st.markdown(f"""<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:14px;margin-bottom:8px">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <span><strong>{r["author"]}</strong>{verified_badge}</span>
                        <span style="font-size:12px;color:#64748b">{r["review_date"]}</span>
                    </div>
                    <div>{stars} <strong>{r["title"]}</strong></div>
                    <p style="margin:6px 0 0;font-size:13px;color:#475569">{r["content"]}</p>
                    <span style="font-size:11px;color:#94a3b8">{"Utile" if t["lang"]=="EN" else "Helpful"}: {r["helpful_count"]}</span>
                </div>""", unsafe_allow_html=True)


def tab_insights(t):
    st.markdown(f'<div class="section-title">{t["monthly_trends"]}</div>', unsafe_allow_html=True)
    monthly = query("""SELECT SUBSTR(review_date,1,7) as month, COUNT(*) as reviews,
        ROUND(AVG(rating),2) as avg_rating FROM reviews
        GROUP BY SUBSTR(review_date,1,7) ORDER BY month""")
    if not monthly.empty:
        st.line_chart(monthly.set_index("month")[["reviews", "avg_rating"]])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="section-title">{t["verified_comparison"]}</div>', unsafe_allow_html=True)
        verified = query("""SELECT CASE WHEN verified=1 THEN 'Verified' ELSE 'Unverified' END as status,
            COUNT(*) as count, ROUND(AVG(rating),2) as avg_rating, ROUND(AVG(LENGTH(content)),0) as avg_length
            FROM reviews GROUP BY verified""")
        if not verified.empty:
            st.dataframe(verified, use_container_width=True, hide_index=True)

    with col2:
        st.markdown(f'<div class="section-title">{t["review_length"]}</div>', unsafe_allow_html=True)
        length = query("""SELECT rating, COUNT(*) as count, ROUND(AVG(LENGTH(content)),0) as avg_chars
            FROM reviews GROUP BY rating ORDER BY rating DESC""")
        if not length.empty:
            st.bar_chart(length.set_index("rating")["avg_chars"])


def tab_sql(t):
    st.markdown(f'<p style="font-size:13px;color:#64748b;">{t["sql_info"]}</p>', unsafe_allow_html=True)
    sql_input = st.text_area(t["sql_label"], height=120, value="SELECT * FROM v_product_summary;")
    if st.button(t["sql_run"], type="primary"):
        try:
            result = query(sql_input)
            st.dataframe(result, use_container_width=True, hide_index=True)
            st.caption(f"{len(result)} rows")
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
        let inner = '<span class="clone-title">ReviewScope</span>';
        tabs.forEach((tab, i) => {
            const label = tab.textContent;
            const cls = tab.getAttribute('aria-selected') === 'true' ? 'active' : '';
            inner += `<button class="${cls}" data-idx="${i}">${label}</button>`;
        });
        clone.innerHTML = inner;
        root.body.appendChild(clone);
        clone.querySelectorAll('button').forEach(btn => {
            btn.addEventListener('click', () => {
                const idx = parseInt(btn.dataset.idx);
                tabs[idx]?.click();
                setTimeout(() => { clone.querySelectorAll('button').forEach((b, j) => { b.className = j === idx ? 'active' : ''; }); }, 100);
            });
        });
        scrollContainer.addEventListener('scroll', () => {
            const rect = tabList.getBoundingClientRect();
            const mainRect = scrollContainer.getBoundingClientRect();
            if (rect.top < mainRect.top) {
                clone.style.display = 'block';
                clone.style.top = mainRect.top + 'px';
                tabs.forEach((tab, i) => { clone.querySelectorAll('button')[i].className = tab.getAttribute('aria-selected') === 'true' ? 'active' : ''; });
            } else { clone.style.display = 'none'; }
        });
    };
    setTimeout(run, 800);
})();
</script>
"""


def main():
    st.set_page_config(page_title="ReviewScope", page_icon="", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    if "lang" not in st.session_state:
        st.session_state.lang = "fr"
    t = COPY[st.session_state.lang]

    header_html = f"""<div class="app-header">
        <div><h1>{t["title"]}</h1><p>{t["subtitle"]}</p></div>
    </div>"""
    st.markdown(header_html, unsafe_allow_html=True)

    col1, col2 = st.columns([10, 1])
    with col2:
        if st.button(t["lang"], key="lang_toggle"):
            st.session_state.lang = "en" if st.session_state.lang == "fr" else "fr"
            st.rerun()

    if not ensure_db():
        st.warning(t["no_data"])
        st.code("python scraper.py --demo", language="bash")
        return

    tabs = st.tabs([t["tab_dashboard"], t["tab_products"], t["tab_reviews"], t["tab_insights"], t["tab_sql"]])

    with tabs[0]: tab_dashboard(t)
    with tabs[1]: tab_products(t)
    with tabs[2]: tab_reviews(t)
    with tabs[3]: tab_insights(t)
    with tabs[4]: tab_sql(t)

    components.html(STICKY_JS, height=0)


if __name__ == "__main__":
    main()

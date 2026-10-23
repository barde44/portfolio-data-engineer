"""WeatherPulse -- Weather Data Collection & Analytics (Streamlit)."""

import sqlite3
import os
import sys
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "weather.db")
SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")

COPY = {
    "fr": {
        "title": "WeatherPulse",
        "subtitle": "Collecte de donnees meteo via API et stockage SQL",
        "tab_dashboard": "Dashboard",
        "tab_cities": "Villes",
        "tab_trends": "Tendances",
        "tab_alerts": "Alertes",
        "tab_sql": "Console SQL",
        "kpi_cities": "Villes",
        "kpi_records": "Enregistrements",
        "kpi_avg_temp": "Temp. moyenne",
        "kpi_avg_humidity": "Humidite moy.",
        "kpi_last_update": "Derniere mise a jour",
        "kpi_days_covered": "Jours couverts",
        "current_weather": "Meteo actuelle par ville",
        "temp_distribution": "Distribution des temperatures",
        "conditions_breakdown": "Conditions meteorologiques",
        "city_comparison": "Comparaison des villes",
        "daily_evolution": "Evolution journaliere",
        "select_city": "Selectionnez une ville",
        "temp_over_time": "Temperature dans le temps",
        "humidity_over_time": "Humidite dans le temps",
        "high_humidity": "Alertes humidite elevee (>85%)",
        "wind_ranking": "Classement du vent",
        "collection_log": "Journal de collecte",
        "sql_label": "Ecrivez votre requete SQL",
        "sql_run": "Executer",
        "sql_info": "Base SQLite en lecture seule. Essayez : SELECT * FROM v_weather_latest;",
        "lang": "EN",
        "no_data": "Aucune donnee. Executez d'abord : python collector.py --demo",
        "temp_unit": "C",
    },
    "en": {
        "title": "WeatherPulse",
        "subtitle": "Weather API Data Collection & SQL Storage",
        "tab_dashboard": "Dashboard",
        "tab_cities": "Cities",
        "tab_trends": "Trends",
        "tab_alerts": "Alerts",
        "tab_sql": "SQL Console",
        "kpi_cities": "Cities",
        "kpi_records": "Records",
        "kpi_avg_temp": "Avg Temp",
        "kpi_avg_humidity": "Avg Humidity",
        "kpi_last_update": "Last Update",
        "kpi_days_covered": "Days Covered",
        "current_weather": "Current weather by city",
        "temp_distribution": "Temperature distribution",
        "conditions_breakdown": "Weather conditions",
        "city_comparison": "City comparison",
        "daily_evolution": "Daily evolution",
        "select_city": "Select a city",
        "temp_over_time": "Temperature over time",
        "humidity_over_time": "Humidity over time",
        "high_humidity": "High humidity alerts (>85%)",
        "wind_ranking": "Wind ranking",
        "collection_log": "Collection log",
        "sql_label": "Write your SQL query",
        "sql_run": "Execute",
        "sql_info": "Read-only SQLite database. Try: SELECT * FROM v_weather_latest;",
        "lang": "FR",
        "no_data": "No data. Run first: python collector.py --demo",
        "temp_unit": "C",
    },
}


def ensure_db():
    if not os.path.exists(DB_PATH):
        return False
    return True


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

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1100px;
    padding-top: 1rem !important;
    padding-bottom: 2rem;
}

.app-header {
    background: linear-gradient(135deg, #0c2340 0%, #1a4f6e 50%, #2d8a8e 100%);
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
    color: #94d2bd;
    font-weight: 400;
}

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
.kpi-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 10px;
    margin-bottom: 16px;
}
.kpi-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.kpi-card .value {
    font-size: 26px;
    font-weight: 700;
    color: #1a4f6e;
    margin: 0;
    line-height: 1.2;
}
.kpi-card .label {
    font-size: 12px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
}

/* Section headers */
.section-title {
    font-size: 16px;
    font-weight: 600;
    color: #1e293b;
    margin: 20px 0 10px;
    padding-bottom: 6px;
    border-bottom: 2px solid #2d8a8e;
    display: inline-block;
}

/* Table styling */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-top: 8px;
}
.styled-table thead th {
    background: #0c2340;
    color: #ffffff;
    padding: 10px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}
.styled-table tbody td {
    padding: 9px 12px;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
}
.styled-table tbody tr:hover {
    background: #f0fdfa;
}
.styled-table tbody tr:nth-child(even) {
    background: #f8fafc;
}

/* Weather icon style */
.weather-icon {
    font-size: 20px;
    margin-right: 4px;
}

/* Alert row */
.alert-row {
    background: #fef3c7 !important;
}

/* Sticky tabs clone */
#sticky-tabs-clone {
    display: none;
    position: fixed;
    left: 0; right: 0;
    z-index: 9999999;
    background: #0c2340;
    padding: 8px 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
#sticky-tabs-clone .clone-title {
    color: #94d2bd;
    font-weight: 600;
    font-size: 14px;
    margin-right: 16px;
}
#sticky-tabs-clone button {
    background: transparent;
    border: none;
    color: #94a3b8;
    font-size: 13px;
    font-weight: 500;
    padding: 6px 14px;
    cursor: pointer;
    border-radius: 4px;
    margin-right: 2px;
}
#sticky-tabs-clone button:hover { background: rgba(255,255,255,0.1); }
#sticky-tabs-clone button.active {
    color: #ffffff;
    background: rgba(45,138,142,0.3);
    border-bottom: 2px solid #2d8a8e;
}
</style>
"""

WEATHER_ICONS = {
    "Clear": "&#9728;&#65039;",
    "Clouds": "&#9729;&#65039;",
    "Rain": "&#127783;&#65039;",
    "Drizzle": "&#127782;&#65039;",
    "Thunderstorm": "&#9889;",
    "Snow": "&#10052;&#65039;",
    "Mist": "&#127787;&#65039;",
    "Haze": "&#127787;&#65039;",
    "Fog": "&#127787;&#65039;",
}


def get_icon(condition):
    return WEATHER_ICONS.get(condition, "&#127777;&#65039;")


def render_kpi(label, value):
    return f'<div class="kpi-card"><p class="value">{value}</p><p class="label">{label}</p></div>'


def tab_dashboard(t):
    stats = query("SELECT COUNT(DISTINCT city_id) as cities, COUNT(*) as records, ROUND(AVG(temperature),1) as avg_temp, ROUND(AVG(humidity),0) as avg_humidity, MIN(collected_at) as first_date, MAX(collected_at) as last_date, COUNT(DISTINCT DATE(collected_at)) as days FROM weather_records")
    row = stats.iloc[0]

    kpis = f"""<div class="kpi-row">
        {render_kpi(t["kpi_cities"], int(row["cities"]))}
        {render_kpi(t["kpi_records"], int(row["records"]))}
        {render_kpi(t["kpi_avg_temp"], f'{row["avg_temp"]}°{t["temp_unit"]}')}
        {render_kpi(t["kpi_avg_humidity"], f'{int(row["avg_humidity"])}%')}
        {render_kpi(t["kpi_days_covered"], int(row["days"]))}
        {render_kpi(t["kpi_last_update"], str(row["last_date"])[:10])}
    </div>"""
    st.markdown(kpis, unsafe_allow_html=True)

    st.markdown(f'<div class="section-title">{t["current_weather"]}</div>', unsafe_allow_html=True)
    latest = query("SELECT * FROM v_weather_latest ORDER BY city")
    if not latest.empty:
        rows_html = ""
        for _, r in latest.iterrows():
            icon = get_icon(r["weather_main"])
            rows_html += f"""<tr>
                <td><strong>{r["city"]}</strong></td>
                <td>{r["country"]}</td>
                <td>{r["temperature"]}°{t["temp_unit"]}</td>
                <td>{r["feels_like"]}°{t["temp_unit"]}</td>
                <td>{r["humidity"]}%</td>
                <td>{r["wind_speed"]} m/s</td>
                <td>{icon} {r["weather_desc"]}</td>
            </tr>"""
        table = f"""<table class="styled-table">
            <thead><tr><th>{"Ville" if t["lang"]=="EN" else "City"}</th><th>Pays</th>
            <th>Temp</th><th>Ressenti</th><th>{"Humidite" if t["lang"]=="EN" else "Humidity"}</th>
            <th>Vent</th><th>Conditions</th></tr></thead>
            <tbody>{rows_html}</tbody></table>"""
        st.markdown(table, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="section-title">{t["temp_distribution"]}</div>', unsafe_allow_html=True)
        temp_data = query("SELECT c.name as city, ROUND(AVG(w.temperature),1) as avg_temp, ROUND(MIN(w.temperature),1) as min_temp, ROUND(MAX(w.temperature),1) as max_temp FROM weather_records w JOIN cities c ON c.city_id=w.city_id GROUP BY c.city_id ORDER BY avg_temp DESC")
        if not temp_data.empty:
            st.bar_chart(temp_data.set_index("city")[["min_temp", "avg_temp", "max_temp"]])

    with col2:
        st.markdown(f'<div class="section-title">{t["conditions_breakdown"]}</div>', unsafe_allow_html=True)
        cond = query("SELECT weather_main as condition, COUNT(*) as count FROM weather_records GROUP BY weather_main ORDER BY count DESC")
        if not cond.empty:
            chart_data = cond.set_index("condition")
            st.bar_chart(chart_data)


def tab_cities(t):
    st.markdown(f'<div class="section-title">{t["city_comparison"]}</div>', unsafe_allow_html=True)
    city_stats = query("SELECT * FROM v_weather_stats ORDER BY avg_temp DESC")
    if not city_stats.empty:
        rows_html = ""
        for _, r in city_stats.iterrows():
            rows_html += f"""<tr>
                <td><strong>{r["city"]}</strong></td>
                <td>{r["country"]}</td>
                <td>{r["total_records"]}</td>
                <td>{r["avg_temp"]}°{t["temp_unit"]}</td>
                <td>{r["min_temp"]}°{t["temp_unit"]}</td>
                <td>{r["max_temp"]}°{t["temp_unit"]}</td>
                <td>{int(r["avg_humidity"])}%</td>
                <td>{r["avg_wind_speed"]} m/s</td>
            </tr>"""
        hdr_ville = "Ville" if t["lang"] == "EN" else "City"
        table = f"""<table class="styled-table">
            <thead><tr><th>{hdr_ville}</th><th>Pays</th><th>Records</th>
            <th>Moy</th><th>Min</th><th>Max</th><th>{"Humidite" if t["lang"]=="EN" else "Humidity"}</th>
            <th>Vent</th></tr></thead>
            <tbody>{rows_html}</tbody></table>"""
        st.markdown(table, unsafe_allow_html=True)

    st.markdown(f'<div class="section-title">{t["conditions_breakdown"]}</div>', unsafe_allow_html=True)
    freq = query("""SELECT c.name as city, w.weather_main as condition, COUNT(*) as count,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY c.city_id), 1) as pct
        FROM weather_records w JOIN cities c ON c.city_id=w.city_id
        GROUP BY c.city_id, w.weather_main ORDER BY c.name, count DESC""")
    if not freq.empty:
        st.dataframe(freq, use_container_width=True, hide_index=True)


def tab_trends(t):
    cities_list = query("SELECT name FROM cities ORDER BY name")["name"].tolist()
    selected = st.selectbox(t["select_city"], cities_list)

    if selected:
        st.markdown(f'<div class="section-title">{t["temp_over_time"]} - {selected}</div>', unsafe_allow_html=True)
        daily = query("""SELECT DATE(w.collected_at) as date, ROUND(AVG(w.temperature),1) as avg_temp,
            ROUND(MIN(w.temp_min),1) as min_temp, ROUND(MAX(w.temp_max),1) as max_temp
            FROM weather_records w JOIN cities c ON c.city_id=w.city_id
            WHERE c.name=:city GROUP BY DATE(w.collected_at) ORDER BY date""",
            {"city": selected})
        if not daily.empty:
            st.line_chart(daily.set_index("date")[["min_temp", "avg_temp", "max_temp"]])

        st.markdown(f'<div class="section-title">{t["humidity_over_time"]} - {selected}</div>', unsafe_allow_html=True)
        humidity = query("""SELECT DATE(w.collected_at) as date, ROUND(AVG(w.humidity),0) as avg_humidity
            FROM weather_records w JOIN cities c ON c.city_id=w.city_id
            WHERE c.name=:city GROUP BY DATE(w.collected_at) ORDER BY date""",
            {"city": selected})
        if not humidity.empty:
            st.line_chart(humidity.set_index("date"))


def tab_alerts(t):
    st.markdown(f'<div class="section-title">{t["high_humidity"]}</div>', unsafe_allow_html=True)
    alerts = query("""SELECT c.name as city, w.humidity, w.temperature, w.weather_desc, w.collected_at
        FROM weather_records w JOIN cities c ON c.city_id=w.city_id
        WHERE w.humidity > 85 ORDER BY w.collected_at DESC LIMIT 50""")
    if not alerts.empty:
        rows_html = ""
        for _, r in alerts.iterrows():
            rows_html += f"""<tr class="alert-row">
                <td><strong>{r["city"]}</strong></td>
                <td>{r["humidity"]}%</td>
                <td>{r["temperature"]}°{t["temp_unit"]}</td>
                <td>{r["weather_desc"]}</td>
                <td>{str(r["collected_at"])[:16]}</td>
            </tr>"""
        hdr_ville = "Ville" if t["lang"] == "EN" else "City"
        table = f"""<table class="styled-table">
            <thead><tr><th>{hdr_ville}</th><th>{"Humidite" if t["lang"]=="EN" else "Humidity"}</th>
            <th>Temp</th><th>Conditions</th><th>Date</th></tr></thead>
            <tbody>{rows_html}</tbody></table>"""
        st.markdown(table, unsafe_allow_html=True)
    else:
        st.info("No high-humidity alerts" if t["lang"] == "FR" else "Aucune alerte humidite")

    st.markdown(f'<div class="section-title">{t["wind_ranking"]}</div>', unsafe_allow_html=True)
    wind = query("""SELECT c.name as city, ROUND(MAX(w.wind_speed),1) as max_wind,
        ROUND(AVG(w.wind_speed),1) as avg_wind,
        COUNT(CASE WHEN w.wind_speed > 10 THEN 1 END) as windy_readings
        FROM weather_records w JOIN cities c ON c.city_id=w.city_id
        GROUP BY c.city_id ORDER BY max_wind DESC""")
    if not wind.empty:
        st.dataframe(wind, use_container_width=True, hide_index=True)

    st.markdown(f'<div class="section-title">{t["collection_log"]}</div>', unsafe_allow_html=True)
    log = query("""SELECT DATE(collected_at) as date, COUNT(*) as records, COUNT(DISTINCT city_id) as cities
        FROM weather_records GROUP BY DATE(collected_at) ORDER BY date DESC LIMIT 30""")
    if not log.empty:
        st.dataframe(log, use_container_width=True, hide_index=True)


def tab_sql(t):
    st.markdown(f'<p style="font-size:13px;color:#64748b;">{t["sql_info"]}</p>', unsafe_allow_html=True)
    sql_input = st.text_area(t["sql_label"], height=120, value="SELECT * FROM v_weather_latest;")
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

        let inner = '<span class="clone-title">WeatherPulse</span>';
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
                setTimeout(() => {
                    clone.querySelectorAll('button').forEach((b, j) => {
                        b.className = j === idx ? 'active' : '';
                    });
                }, 100);
            });
        });

        scrollContainer.addEventListener('scroll', () => {
            const rect = tabList.getBoundingClientRect();
            const mainRect = scrollContainer.getBoundingClientRect();
            if (rect.top < mainRect.top) {
                clone.style.display = 'block';
                clone.style.top = mainRect.top + 'px';
                tabs.forEach((tab, i) => {
                    const selected = tab.getAttribute('aria-selected') === 'true';
                    clone.querySelectorAll('button')[i].className = selected ? 'active' : '';
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


def main():
    st.set_page_config(page_title="WeatherPulse", page_icon="", layout="wide")
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
        st.code("python collector.py --demo", language="bash")
        return

    tabs = st.tabs([
        t["tab_dashboard"],
        t["tab_cities"],
        t["tab_trends"],
        t["tab_alerts"],
        t["tab_sql"],
    ])

    with tabs[0]:
        tab_dashboard(t)
    with tabs[1]:
        tab_cities(t)
    with tabs[2]:
        tab_trends(t)
    with tabs[3]:
        tab_alerts(t)
    with tabs[4]:
        tab_sql(t)

    components.html(STICKY_JS, height=0)


if __name__ == "__main__":
    main()

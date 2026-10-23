"""
Weather data collector — fetches current weather from OpenWeatherMap API
and stores it in a SQLite database.
"""
import os
import sys
import json
import sqlite3
import logging
from datetime import datetime, timezone

import requests

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "weather.db")
SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")
LOG_PATH = os.path.join(os.path.dirname(__file__), "data", "collector.log")

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

DEFAULT_CITIES = [
    ("Lome", "TG", 6.1375, 1.2123),
    ("Ndjamena", "TD", 12.1348, 15.0557),
    ("Paris", "FR", 48.8566, 2.3522),
    ("New York", "US", 40.7128, -74.0060),
    ("Douala", "CM", 4.0483, 9.7043),
    ("Dakar", "SN", 14.6928, -17.4467),
    ("Nairobi", "KE", -1.2921, 36.8219),
    ("London", "GB", 51.5074, -0.1278),
    ("Tokyo", "JP", 35.6762, 139.6503),
    ("Dubai", "AE", 25.2048, 55.2708),
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    schema_path = os.path.join(SQL_DIR, "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    return conn


def seed_cities(conn):
    cursor = conn.cursor()
    for name, country, lat, lon in DEFAULT_CITIES:
        cursor.execute(
            "INSERT OR IGNORE INTO cities (name, country, latitude, longitude) VALUES (?, ?, ?, ?)",
            (name, country, lat, lon),
        )
    conn.commit()
    logger.info("Seeded %d default cities", len(DEFAULT_CITIES))


def get_cities(conn):
    cursor = conn.execute("SELECT city_id, name, latitude, longitude FROM cities")
    return cursor.fetchall()


def fetch_weather(lat, lon, api_key, units="metric"):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": units,
    }
    resp = requests.get(OPENWEATHER_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def parse_weather(data):
    main = data.get("main", {})
    wind = data.get("wind", {})
    clouds = data.get("clouds", {})
    weather = data.get("weather", [{}])[0]
    sys_data = data.get("sys", {})

    sunrise_ts = sys_data.get("sunrise")
    sunset_ts = sys_data.get("sunset")

    return {
        "temperature": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "temp_min": main.get("temp_min"),
        "temp_max": main.get("temp_max"),
        "pressure": main.get("pressure"),
        "humidity": main.get("humidity"),
        "wind_speed": wind.get("speed"),
        "wind_deg": wind.get("deg"),
        "clouds": clouds.get("all"),
        "visibility": data.get("visibility"),
        "weather_main": weather.get("main"),
        "weather_desc": weather.get("description"),
        "weather_icon": weather.get("icon"),
        "sunrise": datetime.fromtimestamp(sunrise_ts, tz=timezone.utc).isoformat() if sunrise_ts else None,
        "sunset": datetime.fromtimestamp(sunset_ts, tz=timezone.utc).isoformat() if sunset_ts else None,
    }


def store_weather(conn, city_id, weather_data):
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """INSERT INTO weather_records
           (city_id, collected_at, temperature, feels_like, temp_min, temp_max,
            pressure, humidity, wind_speed, wind_deg, clouds, visibility,
            weather_main, weather_desc, weather_icon, sunrise, sunset)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            city_id, now,
            weather_data["temperature"], weather_data["feels_like"],
            weather_data["temp_min"], weather_data["temp_max"],
            weather_data["pressure"], weather_data["humidity"],
            weather_data["wind_speed"], weather_data["wind_deg"],
            weather_data["clouds"], weather_data["visibility"],
            weather_data["weather_main"], weather_data["weather_desc"],
            weather_data["weather_icon"],
            weather_data["sunrise"], weather_data["sunset"],
        ),
    )
    conn.commit()


def collect_all(api_key):
    conn = init_db()
    seed_cities(conn)
    cities = get_cities(conn)

    success = 0
    errors = 0

    for city_id, name, lat, lon in cities:
        try:
            raw = fetch_weather(lat, lon, api_key)
            parsed = parse_weather(raw)
            store_weather(conn, city_id, parsed)
            logger.info(
                "%s: %.1f C, %s",
                name, parsed["temperature"], parsed["weather_desc"],
            )
            success += 1
        except requests.RequestException as e:
            logger.error("Failed to fetch %s: %s", name, e)
            errors += 1
        except Exception as e:
            logger.error("Error processing %s: %s", name, e)
            errors += 1

    conn.close()
    logger.info("Collection complete: %d success, %d errors", success, errors)
    return success, errors


def generate_sample_data():
    """Generate realistic sample data for demonstration without API key."""
    import random

    conn = init_db()
    seed_cities(conn)
    cities = get_cities(conn)

    sample_conditions = [
        ("Clear", "clear sky", "01d"),
        ("Clouds", "few clouds", "02d"),
        ("Clouds", "scattered clouds", "03d"),
        ("Clouds", "overcast clouds", "04d"),
        ("Rain", "light rain", "10d"),
        ("Rain", "moderate rain", "09d"),
        ("Drizzle", "light drizzle", "09d"),
        ("Thunderstorm", "thunderstorm", "11d"),
        ("Mist", "mist", "50d"),
    ]

    climate_profiles = {
        "Lome":     {"temp_base": 28, "temp_var": 4, "humidity_base": 78, "wind_base": 3.5},
        "Ndjamena": {"temp_base": 33, "temp_var": 6, "humidity_base": 40, "wind_base": 4.0},
        "Paris":    {"temp_base": 14, "temp_var": 8, "humidity_base": 70, "wind_base": 4.5},
        "New York": {"temp_base": 16, "temp_var": 10, "humidity_base": 65, "wind_base": 5.0},
        "Douala":   {"temp_base": 27, "temp_var": 3, "humidity_base": 82, "wind_base": 2.5},
        "Dakar":    {"temp_base": 25, "temp_var": 5, "humidity_base": 72, "wind_base": 5.5},
        "Nairobi":  {"temp_base": 20, "temp_var": 5, "humidity_base": 60, "wind_base": 3.0},
        "London":   {"temp_base": 12, "temp_var": 7, "humidity_base": 75, "wind_base": 5.0},
        "Tokyo":    {"temp_base": 18, "temp_var": 9, "humidity_base": 68, "wind_base": 3.5},
        "Dubai":    {"temp_base": 34, "temp_var": 6, "humidity_base": 55, "wind_base": 4.0},
    }

    records_per_city = 30
    logger.info("Generating %d sample records per city...", records_per_city)

    for city_id, name, lat, lon in cities:
        profile = climate_profiles.get(name, {"temp_base": 20, "temp_var": 5, "humidity_base": 65, "wind_base": 3.5})

        for day_offset in range(records_per_city):
            base_date = datetime(2026, 9, 24, 8, 0, 0, tzinfo=timezone.utc)
            from datetime import timedelta
            record_date = base_date + timedelta(days=day_offset, hours=random.randint(0, 12))

            temp = round(profile["temp_base"] + random.uniform(-profile["temp_var"], profile["temp_var"]), 1)
            feels = round(temp + random.uniform(-2, 2), 1)
            temp_min = round(temp - random.uniform(1, 3), 1)
            temp_max = round(temp + random.uniform(1, 3), 1)
            humidity = max(10, min(100, int(profile["humidity_base"] + random.randint(-15, 15))))
            wind = round(max(0, profile["wind_base"] + random.uniform(-2, 3)), 1)
            pressure = random.randint(1005, 1025)
            clouds_pct = random.randint(0, 100)
            visibility = random.randint(3000, 10000)
            condition = random.choice(sample_conditions)

            conn.execute(
                """INSERT INTO weather_records
                   (city_id, collected_at, temperature, feels_like, temp_min, temp_max,
                    pressure, humidity, wind_speed, wind_deg, clouds, visibility,
                    weather_main, weather_desc, weather_icon, sunrise, sunset)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    city_id, record_date.isoformat(),
                    temp, feels, temp_min, temp_max,
                    pressure, humidity, wind, random.randint(0, 360),
                    clouds_pct, visibility,
                    condition[0], condition[1], condition[2],
                    record_date.replace(hour=6, minute=random.randint(0, 30)).isoformat(),
                    record_date.replace(hour=18, minute=random.randint(0, 30)).isoformat(),
                ),
            )

    conn.commit()
    total = records_per_city * len(cities)
    logger.info("Generated %d sample records for %d cities", total, len(cities))
    conn.close()
    return total


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Weather data collector")
    parser.add_argument("--api-key", help="OpenWeatherMap API key")
    parser.add_argument("--demo", action="store_true", help="Generate sample data without API")
    args = parser.parse_args()

    if args.demo:
        generate_sample_data()
    elif args.api_key:
        collect_all(args.api_key)
    else:
        api_key = os.environ.get("OPENWEATHER_API_KEY")
        if api_key:
            collect_all(api_key)
        else:
            logger.info("No API key provided. Use --demo to generate sample data, or --api-key YOUR_KEY")
            sys.exit(1)

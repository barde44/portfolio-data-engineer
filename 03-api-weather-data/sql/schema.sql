CREATE TABLE IF NOT EXISTS cities (
    city_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL UNIQUE,
    country    TEXT    NOT NULL,
    latitude   REAL    NOT NULL,
    longitude  REAL    NOT NULL,
    added_at   TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS weather_records (
    record_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id         INTEGER NOT NULL,
    collected_at    TEXT    NOT NULL,
    temperature     REAL,
    feels_like      REAL,
    temp_min        REAL,
    temp_max        REAL,
    pressure        INTEGER,
    humidity        INTEGER,
    wind_speed      REAL,
    wind_deg        INTEGER,
    clouds          INTEGER,
    visibility      INTEGER,
    weather_main    TEXT,
    weather_desc    TEXT,
    weather_icon    TEXT,
    sunrise         TEXT,
    sunset          TEXT,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

CREATE INDEX IF NOT EXISTS idx_weather_city ON weather_records(city_id);
CREATE INDEX IF NOT EXISTS idx_weather_date ON weather_records(collected_at);
CREATE INDEX IF NOT EXISTS idx_weather_city_date ON weather_records(city_id, collected_at);

CREATE VIEW IF NOT EXISTS v_weather_latest AS
SELECT
    c.name AS city,
    c.country,
    w.temperature,
    w.feels_like,
    w.humidity,
    w.wind_speed,
    w.weather_main,
    w.weather_desc,
    w.collected_at
FROM weather_records w
JOIN cities c ON c.city_id = w.city_id
WHERE w.collected_at = (
    SELECT MAX(w2.collected_at)
    FROM weather_records w2
    WHERE w2.city_id = w.city_id
);

CREATE VIEW IF NOT EXISTS v_weather_stats AS
SELECT
    c.name AS city,
    c.country,
    COUNT(*) AS total_records,
    ROUND(AVG(w.temperature), 1) AS avg_temp,
    ROUND(MIN(w.temperature), 1) AS min_temp,
    ROUND(MAX(w.temperature), 1) AS max_temp,
    ROUND(AVG(w.humidity), 0) AS avg_humidity,
    ROUND(AVG(w.wind_speed), 1) AS avg_wind_speed,
    MIN(w.collected_at) AS first_record,
    MAX(w.collected_at) AS last_record
FROM weather_records w
JOIN cities c ON c.city_id = w.city_id
GROUP BY c.city_id;

CREATE VIEW IF NOT EXISTS v_daily_summary AS
SELECT
    c.name AS city,
    DATE(w.collected_at) AS date,
    COUNT(*) AS records_count,
    ROUND(AVG(w.temperature), 1) AS avg_temp,
    ROUND(MIN(w.temp_min), 1) AS min_temp,
    ROUND(MAX(w.temp_max), 1) AS max_temp,
    ROUND(AVG(w.humidity), 0) AS avg_humidity,
    ROUND(AVG(w.wind_speed), 1) AS avg_wind_speed,
    GROUP_CONCAT(DISTINCT w.weather_main) AS conditions
FROM weather_records w
JOIN cities c ON c.city_id = w.city_id
GROUP BY c.city_id, DATE(w.collected_at)
ORDER BY date DESC;

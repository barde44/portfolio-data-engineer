-- Q1: Current weather for all tracked cities
SELECT
    c.name,
    c.country,
    w.temperature,
    w.feels_like,
    w.humidity,
    w.wind_speed,
    w.weather_desc,
    w.collected_at
FROM weather_records w
JOIN cities c ON c.city_id = w.city_id
WHERE w.collected_at = (
    SELECT MAX(w2.collected_at)
    FROM weather_records w2
    WHERE w2.city_id = w.city_id
)
ORDER BY c.name;

-- Q2: Temperature extremes per city
SELECT
    c.name,
    ROUND(MIN(w.temperature), 1) AS coldest,
    ROUND(MAX(w.temperature), 1) AS hottest,
    ROUND(MAX(w.temperature) - MIN(w.temperature), 1) AS temp_range,
    COUNT(*) AS total_readings
FROM weather_records w
JOIN cities c ON c.city_id = w.city_id
GROUP BY c.city_id
ORDER BY temp_range DESC;

-- Q3: Average conditions by city
SELECT
    c.name,
    ROUND(AVG(w.temperature), 1) AS avg_temp,
    ROUND(AVG(w.humidity), 0) AS avg_humidity,
    ROUND(AVG(w.wind_speed), 1) AS avg_wind,
    ROUND(AVG(w.pressure), 0) AS avg_pressure
FROM weather_records w
JOIN cities c ON c.city_id = w.city_id
GROUP BY c.city_id
ORDER BY avg_temp DESC;

-- Q4: Daily temperature evolution for a specific city
SELECT
    DATE(w.collected_at) AS date,
    ROUND(AVG(w.temperature), 1) AS avg_temp,
    ROUND(MIN(w.temp_min), 1) AS min_temp,
    ROUND(MAX(w.temp_max), 1) AS max_temp,
    ROUND(AVG(w.humidity), 0) AS avg_humidity
FROM weather_records w
JOIN cities c ON c.city_id = w.city_id
WHERE c.name = :city_name
GROUP BY DATE(w.collected_at)
ORDER BY date DESC
LIMIT 30;

-- Q5: Most frequent weather conditions per city
SELECT
    c.name,
    w.weather_main,
    COUNT(*) AS occurrences,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY c.city_id), 1) AS pct
FROM weather_records w
JOIN cities c ON c.city_id = w.city_id
GROUP BY c.city_id, w.weather_main
ORDER BY c.name, occurrences DESC;

-- Q6: Humidity alerts (above 85%)
SELECT
    c.name,
    w.humidity,
    w.temperature,
    w.weather_desc,
    w.collected_at
FROM weather_records w
JOIN cities c ON c.city_id = w.city_id
WHERE w.humidity > 85
ORDER BY w.collected_at DESC;

-- Q7: Wind speed ranking
SELECT
    c.name,
    ROUND(MAX(w.wind_speed), 1) AS max_wind,
    ROUND(AVG(w.wind_speed), 1) AS avg_wind,
    COUNT(CASE WHEN w.wind_speed > 10 THEN 1 END) AS windy_readings
FROM weather_records w
JOIN cities c ON c.city_id = w.city_id
GROUP BY c.city_id
ORDER BY max_wind DESC;

-- Q8: Collection activity log
SELECT
    DATE(collected_at) AS date,
    COUNT(*) AS records_collected,
    COUNT(DISTINCT city_id) AS cities_covered
FROM weather_records
GROUP BY DATE(collected_at)
ORDER BY date DESC
LIMIT 30;

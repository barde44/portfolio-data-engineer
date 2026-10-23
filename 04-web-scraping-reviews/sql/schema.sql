CREATE TABLE IF NOT EXISTS sources (
    source_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    url         TEXT,
    added_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS products (
    product_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    category    TEXT,
    brand       TEXT,
    source_id   INTEGER NOT NULL,
    url         TEXT,
    avg_rating  REAL,
    total_reviews INTEGER DEFAULT 0,
    scraped_at  TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (source_id) REFERENCES sources(source_id)
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id  INTEGER NOT NULL,
    author      TEXT,
    rating      INTEGER CHECK(rating BETWEEN 1 AND 5),
    title       TEXT,
    content     TEXT,
    review_date TEXT,
    helpful_count INTEGER DEFAULT 0,
    verified    INTEGER DEFAULT 0,
    scraped_at  TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_reviews_date ON reviews(review_date);
CREATE INDEX IF NOT EXISTS idx_reviews_product_rating ON reviews(product_id, rating);
CREATE INDEX IF NOT EXISTS idx_products_source ON products(source_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);

CREATE VIEW IF NOT EXISTS v_product_summary AS
SELECT
    p.product_id,
    p.name AS product,
    p.category,
    p.brand,
    s.name AS source,
    COUNT(r.review_id) AS review_count,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    SUM(CASE WHEN r.rating >= 4 THEN 1 ELSE 0 END) AS positive,
    SUM(CASE WHEN r.rating <= 2 THEN 1 ELSE 0 END) AS negative,
    SUM(CASE WHEN r.rating = 3 THEN 1 ELSE 0 END) AS neutral,
    MIN(r.review_date) AS first_review,
    MAX(r.review_date) AS last_review
FROM products p
JOIN sources s ON s.source_id = p.source_id
LEFT JOIN reviews r ON r.product_id = p.product_id
GROUP BY p.product_id;

CREATE VIEW IF NOT EXISTS v_rating_distribution AS
SELECT
    p.name AS product,
    p.category,
    r.rating,
    COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY p.product_id), 1) AS pct
FROM reviews r
JOIN products p ON p.product_id = r.product_id
GROUP BY p.product_id, r.rating
ORDER BY p.name, r.rating DESC;

CREATE VIEW IF NOT EXISTS v_monthly_activity AS
SELECT
    p.name AS product,
    SUBSTR(r.review_date, 1, 7) AS month,
    COUNT(*) AS review_count,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM reviews r
JOIN products p ON p.product_id = r.product_id
GROUP BY p.product_id, SUBSTR(r.review_date, 1, 7)
ORDER BY month DESC;

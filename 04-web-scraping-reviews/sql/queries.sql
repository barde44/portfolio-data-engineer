-- Q1: Product overview with rating summary
SELECT
    p.name,
    p.category,
    p.brand,
    COUNT(r.review_id) AS reviews,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    SUM(CASE WHEN r.rating >= 4 THEN 1 ELSE 0 END) AS positive,
    SUM(CASE WHEN r.rating <= 2 THEN 1 ELSE 0 END) AS negative
FROM products p
LEFT JOIN reviews r ON r.product_id = p.product_id
GROUP BY p.product_id
ORDER BY avg_rating DESC;

-- Q2: Rating distribution per product
SELECT
    p.name,
    r.rating,
    COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY p.product_id), 1) AS pct
FROM reviews r
JOIN products p ON p.product_id = r.product_id
GROUP BY p.product_id, r.rating
ORDER BY p.name, r.rating DESC;

-- Q3: Most helpful reviews
SELECT
    p.name AS product,
    r.author,
    r.rating,
    r.title,
    SUBSTR(r.content, 1, 100) || '...' AS excerpt,
    r.helpful_count,
    r.review_date
FROM reviews r
JOIN products p ON p.product_id = r.product_id
WHERE r.helpful_count > 0
ORDER BY r.helpful_count DESC
LIMIT 20;

-- Q4: Monthly review trends
SELECT
    SUBSTR(r.review_date, 1, 7) AS month,
    COUNT(*) AS total_reviews,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(DISTINCT r.product_id) AS products_reviewed
FROM reviews r
GROUP BY SUBSTR(r.review_date, 1, 7)
ORDER BY month DESC;

-- Q5: Sentiment analysis by category
SELECT
    p.category,
    COUNT(*) AS total,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    ROUND(100.0 * SUM(CASE WHEN r.rating >= 4 THEN 1 ELSE 0 END) / COUNT(*), 1) AS positive_pct,
    ROUND(100.0 * SUM(CASE WHEN r.rating <= 2 THEN 1 ELSE 0 END) / COUNT(*), 1) AS negative_pct
FROM reviews r
JOIN products p ON p.product_id = r.product_id
GROUP BY p.category
ORDER BY avg_rating DESC;

-- Q6: Review length vs rating correlation
SELECT
    r.rating,
    COUNT(*) AS count,
    ROUND(AVG(LENGTH(r.content)), 0) AS avg_length,
    ROUND(MIN(LENGTH(r.content)), 0) AS min_length,
    ROUND(MAX(LENGTH(r.content)), 0) AS max_length
FROM reviews r
GROUP BY r.rating
ORDER BY r.rating DESC;

-- Q7: Verified vs unverified purchase comparison
SELECT
    CASE WHEN r.verified = 1 THEN 'Verified' ELSE 'Unverified' END AS status,
    COUNT(*) AS count,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    ROUND(AVG(LENGTH(r.content)), 0) AS avg_review_length
FROM reviews r
GROUP BY r.verified;

-- Q8: Brand performance ranking
SELECT
    p.brand,
    COUNT(DISTINCT p.product_id) AS products,
    COUNT(r.review_id) AS total_reviews,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    ROUND(100.0 * SUM(CASE WHEN r.rating >= 4 THEN 1 ELSE 0 END) / COUNT(*), 1) AS satisfaction_pct
FROM products p
JOIN reviews r ON r.product_id = p.product_id
GROUP BY p.brand
ORDER BY avg_rating DESC;

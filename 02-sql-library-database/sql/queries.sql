-- ============================================================
-- LibraryDB -- Requetes analytiques et Vues
-- ============================================================

-- ============================================================
-- REQUETES ANALYTIQUES
-- ============================================================

-- Q1: Livres actuellement empruntes (non retournes)
SELECT b.title, a.first_name || ' ' || a.last_name AS author,
       br.first_name || ' ' || br.last_name AS borrower,
       l.loan_date, l.due_date,
       CASE WHEN l.due_date < date('now') THEN 'EN RETARD' ELSE 'En cours' END AS status
FROM loans l
JOIN books b ON l.book_id = b.book_id
JOIN authors a ON b.author_id = a.author_id
JOIN borrowers br ON l.borrower_id = br.borrower_id
WHERE l.return_date IS NULL
ORDER BY l.due_date;

-- Q2: Auteurs ayant publie le plus de livres dans la bibliotheque
SELECT a.first_name || ' ' || a.last_name AS author,
       a.nationality,
       COUNT(b.book_id) AS total_books,
       GROUP_CONCAT(b.title, ', ') AS titles
FROM authors a
JOIN books b ON a.author_id = b.author_id
GROUP BY a.author_id
ORDER BY total_books DESC
LIMIT 5;

-- Q3: Emprunteurs les plus actifs (total emprunts)
SELECT br.first_name || ' ' || br.last_name AS borrower,
       br.email,
       COUNT(l.loan_id) AS total_loans,
       SUM(CASE WHEN l.return_date IS NOT NULL THEN 1 ELSE 0 END) AS returned,
       SUM(CASE WHEN l.return_date IS NULL THEN 1 ELSE 0 END) AS active
FROM borrowers br
JOIN loans l ON br.borrower_id = l.borrower_id
GROUP BY br.borrower_id
ORDER BY total_loans DESC;

-- Q4: Livres les plus empruntes
SELECT b.title,
       a.first_name || ' ' || a.last_name AS author,
       c.name AS category,
       COUNT(l.loan_id) AS times_borrowed
FROM books b
JOIN authors a ON b.author_id = a.author_id
JOIN categories c ON b.category_id = c.category_id
JOIN loans l ON b.book_id = l.book_id
GROUP BY b.book_id
ORDER BY times_borrowed DESC
LIMIT 10;

-- Q5: Emprunts en retard
SELECT br.first_name || ' ' || br.last_name AS borrower,
       br.email,
       b.title,
       l.loan_date,
       l.due_date,
       CAST(julianday('now') - julianday(l.due_date) AS INTEGER) AS days_overdue
FROM loans l
JOIN books b ON l.book_id = b.book_id
JOIN borrowers br ON l.borrower_id = br.borrower_id
WHERE l.return_date IS NULL AND l.due_date < date('now')
ORDER BY days_overdue DESC;

-- Q6: Repartition des livres par categorie
SELECT c.name AS category,
       COUNT(b.book_id) AS total_books,
       SUM(b.copies_available) AS total_copies,
       ROUND(COUNT(b.book_id) * 100.0 / (SELECT COUNT(*) FROM books), 1) AS pct
FROM categories c
LEFT JOIN books b ON c.category_id = b.category_id
GROUP BY c.category_id
ORDER BY total_books DESC;

-- Q7: Duree moyenne d'emprunt par categorie
SELECT c.name AS category,
       ROUND(AVG(julianday(l.return_date) - julianday(l.loan_date)), 1) AS avg_days,
       MIN(CAST(julianday(l.return_date) - julianday(l.loan_date) AS INTEGER)) AS min_days,
       MAX(CAST(julianday(l.return_date) - julianday(l.loan_date) AS INTEGER)) AS max_days
FROM loans l
JOIN books b ON l.book_id = b.book_id
JOIN categories c ON b.category_id = c.category_id
WHERE l.return_date IS NOT NULL
GROUP BY c.category_id
ORDER BY avg_days DESC;

-- Q8: Activite mensuelle (emprunts par mois)
SELECT strftime('%Y-%m', loan_date) AS month,
       COUNT(*) AS total_loans,
       SUM(CASE WHEN return_date IS NOT NULL THEN 1 ELSE 0 END) AS returned,
       SUM(CASE WHEN return_date IS NULL THEN 1 ELSE 0 END) AS pending
FROM loans
GROUP BY month
ORDER BY month;

-- ============================================================
-- VUES
-- ============================================================

-- Vue: Catalogue complet avec disponibilite
CREATE VIEW IF NOT EXISTS v_catalog AS
SELECT b.book_id, b.title, b.isbn, b.publication_year,
       a.first_name || ' ' || a.last_name AS author,
       c.name AS category,
       b.copies_available,
       b.copies_available - COALESCE(
           (SELECT COUNT(*) FROM loans l WHERE l.book_id = b.book_id AND l.return_date IS NULL), 0
       ) AS copies_on_shelf
FROM books b
JOIN authors a ON b.author_id = a.author_id
JOIN categories c ON b.category_id = c.category_id;

-- Vue: Emprunts actifs avec details
CREATE VIEW IF NOT EXISTS v_active_loans AS
SELECT l.loan_id, b.title, b.isbn,
       a.first_name || ' ' || a.last_name AS author,
       br.first_name || ' ' || br.last_name AS borrower,
       br.email,
       l.loan_date, l.due_date,
       CASE
           WHEN l.due_date < date('now') THEN 'EN RETARD'
           WHEN l.due_date = date('now') THEN 'Echoit aujourd''hui'
           ELSE 'En cours'
       END AS status,
       CASE
           WHEN l.due_date < date('now')
           THEN CAST(julianday('now') - julianday(l.due_date) AS INTEGER)
           ELSE NULL
       END AS days_overdue
FROM loans l
JOIN books b ON l.book_id = b.book_id
JOIN authors a ON b.author_id = a.author_id
JOIN borrowers br ON l.borrower_id = br.borrower_id
WHERE l.return_date IS NULL;

-- Vue: Statistiques par auteur
CREATE VIEW IF NOT EXISTS v_author_stats AS
SELECT a.author_id,
       a.first_name || ' ' || a.last_name AS author,
       a.nationality,
       COUNT(DISTINCT b.book_id) AS total_books,
       COALESCE(SUM(b.copies_available), 0) AS total_copies,
       COUNT(DISTINCT l.loan_id) AS total_loans
FROM authors a
LEFT JOIN books b ON a.author_id = b.author_id
LEFT JOIN loans l ON b.book_id = l.book_id
GROUP BY a.author_id;

-- Vue: Tableau de bord global
CREATE VIEW IF NOT EXISTS v_dashboard AS
SELECT
    (SELECT COUNT(*) FROM books) AS total_books,
    (SELECT SUM(copies_available) FROM books) AS total_copies,
    (SELECT COUNT(*) FROM authors) AS total_authors,
    (SELECT COUNT(*) FROM borrowers) AS total_borrowers,
    (SELECT COUNT(*) FROM loans) AS total_loans,
    (SELECT COUNT(*) FROM loans WHERE return_date IS NULL) AS active_loans,
    (SELECT COUNT(*) FROM loans WHERE return_date IS NULL AND due_date < date('now')) AS overdue_loans,
    (SELECT COUNT(*) FROM categories) AS total_categories;

-- ============================================================
-- LibraryDB -- Sample Data
-- ============================================================

-- Categories
INSERT INTO categories (name, description) VALUES
('Fiction', 'Romans, nouvelles et recits fictifs'),
('Science-Fiction', 'Recits futuristes et technologiques'),
('Histoire', 'Ouvrages historiques et biographies'),
('Informatique', 'Programmation, bases de donnees, reseaux'),
('Philosophie', 'Essais et textes philosophiques'),
('Sciences', 'Physique, chimie, biologie, mathematiques'),
('Economie', 'Finance, management, economie politique');

-- Auteurs
INSERT INTO authors (first_name, last_name, birth_year, nationality) VALUES
('Victor', 'Hugo', 1802, 'Francais'),
('Albert', 'Camus', 1913, 'Francais'),
('Chinua', 'Achebe', 1930, 'Nigerian'),
('Isaac', 'Asimov', 1920, 'Americain'),
('Yuval Noah', 'Harari', 1976, 'Israelien'),
('Robert C.', 'Martin', 1952, 'Americain'),
('Thomas', 'Cormen', 1956, 'Americain'),
('Frantz', 'Fanon', 1925, 'Martiniquais'),
('Mariama', 'Ba', 1929, 'Senegalaise'),
('Ngugi wa', 'Thiongo', 1938, 'Kenyan'),
('Chimamanda Ngozi', 'Adichie', 2977, 'Nigeriane'),
('Martin', 'Kleppmann', 1984, 'Allemand'),
('Thomas', 'Piketty', 1971, 'Francais'),
('Marie', 'Curie', 1867, 'Polonaise'),
('Stephen', 'Hawking', 1942, 'Britannique');

-- Correction: Adichie nee en 1977
UPDATE authors SET birth_year = 1977 WHERE last_name = 'Adichie';

-- Livres
INSERT INTO books (title, author_id, category_id, isbn, publication_year, copies_available) VALUES
('Les Miserables', 1, 1, '978-2-07-040850-4', 1862, 3),
('Notre-Dame de Paris', 1, 1, '978-2-07-041239-6', 1831, 2),
('L''Etranger', 2, 1, '978-2-07-036024-8', 1942, 4),
('La Peste', 2, 1, '978-2-07-036042-2', 1947, 2),
('Things Fall Apart', 3, 1, '978-0-385-47454-2', 1958, 3),
('Fondation', 4, 2, '978-2-07-041538-0', 1951, 2),
('I, Robot', 4, 2, '978-0-553-29438-5', 1950, 1),
('Sapiens', 5, 3, '978-2-226-25781-3', 2011, 5),
('Homo Deus', 5, 3, '978-2-226-39300-0', 2015, 3),
('Clean Code', 6, 4, '978-0-13-235088-4', 2008, 4),
('Introduction to Algorithms', 7, 4, '978-0-262-03384-8', 2009, 2),
('Les Damnes de la Terre', 8, 5, '978-2-07-032291-8', 1961, 2),
('Une si longue lettre', 9, 1, '978-2-7087-0838-0', 1979, 3),
('Decolonising the Mind', 10, 5, '978-0-85255-501-3', 1986, 1),
('Americanah', 11, 1, '978-0-307-45592-0', 2013, 4),
('Half of a Yellow Sun', 11, 1, '978-1-4000-9520-3', 2006, 2),
('Designing Data-Intensive Applications', 12, 4, '978-1-449-37332-0', 2017, 3),
('Le Capital au XXIe siecle', 13, 7, '978-2-02-108228-9', 2013, 2),
('Une breve histoire du temps', 15, 6, '978-2-08-128181-2', 1988, 3),
('The Agile Samurai', 6, 4, '978-1-93435-658-6', 2010, 2);

-- Emprunteurs
INSERT INTO borrowers (first_name, last_name, email, phone, registration_date) VALUES
('Amina', 'Diallo', 'amina.diallo@mail.com', '+235-66-12-34-56', '2025-09-01'),
('Moussa', 'Traore', 'moussa.traore@mail.com', '+235-66-23-45-67', '2025-09-05'),
('Fatou', 'Ndiaye', 'fatou.ndiaye@mail.com', '+228-90-34-56-78', '2025-09-10'),
('Ibrahim', 'Mahamat', 'ibrahim.mahamat@mail.com', '+235-66-45-67-89', '2025-10-01'),
('Aissatou', 'Barry', 'aissatou.barry@mail.com', '+224-62-56-78-90', '2025-10-15'),
('Yves', 'Kouame', 'yves.kouame@mail.com', '+225-07-67-89-01', '2025-11-01'),
('Ngozi', 'Okafor', 'ngozi.okafor@mail.com', '+234-80-78-90-12', '2025-11-20'),
('Jean-Pierre', 'Habimana', 'jp.habimana@mail.com', '+250-78-89-01-23', '2026-01-10'),
('Kofi', 'Mensah', 'kofi.mensah@mail.com', '+233-24-90-12-34', '2026-02-15'),
('Mariame', 'Coulibaly', 'mariame.coulibaly@mail.com', '+223-76-01-23-45', '2026-03-01');

-- Emprunts (mix de retournes et en cours)
INSERT INTO loans (book_id, borrower_id, loan_date, due_date, return_date) VALUES
-- Emprunts retournes
(1, 1, '2026-06-01', '2026-06-15', '2026-06-14'),
(3, 2, '2026-06-05', '2026-06-19', '2026-06-18'),
(5, 3, '2026-06-10', '2026-06-24', '2026-06-22'),
(8, 4, '2026-07-01', '2026-07-15', '2026-07-10'),
(10, 1, '2026-07-05', '2026-07-19', '2026-07-19'),
(13, 5, '2026-07-10', '2026-07-24', '2026-07-20'),
(15, 6, '2026-07-15', '2026-07-29', '2026-07-28'),
(17, 7, '2026-08-01', '2026-08-15', '2026-08-12'),
(6, 2, '2026-08-05', '2026-08-19', '2026-08-15'),
(11, 8, '2026-08-10', '2026-08-24', '2026-08-23'),
(4, 3, '2026-08-15', '2026-08-29', '2026-08-28'),
(9, 9, '2026-09-01', '2026-09-15', '2026-09-12'),
(2, 4, '2026-09-05', '2026-09-19', '2026-09-18'),
(18, 10, '2026-09-10', '2026-09-24', '2026-09-20'),
(7, 1, '2026-09-15', '2026-09-29', '2026-09-25'),
(12, 5, '2026-09-20', '2026-10-04', '2026-10-01'),
(19, 6, '2026-09-25', '2026-10-09', '2026-10-05'),
(14, 7, '2026-10-01', '2026-10-15', '2026-10-10'),
(20, 8, '2026-10-05', '2026-10-19', '2026-10-15'),
-- Emprunts en cours (non retournes)
(1, 9, '2026-10-10', '2026-10-24', NULL),
(8, 10, '2026-10-12', '2026-10-26', NULL),
(3, 1, '2026-10-15', '2026-10-29', NULL),
(15, 2, '2026-10-16', '2026-10-30', NULL),
(10, 3, '2026-10-18', '2026-11-01', NULL),
(5, 4, '2026-10-19', '2026-11-02', NULL),
(17, 5, '2026-10-20', '2026-11-03', NULL),
-- Emprunts en retard
(16, 6, '2026-09-15', '2026-09-29', NULL),
(6, 9, '2026-09-20', '2026-10-04', NULL);

-- 1. INSERT — добавление новых записей 

INSERT INTO Users (full_name, login, password_hash, email, role_id)
VALUES ('Морозов Андрей Петрович', 'morozov', 'hash_morozov', 'morozov@example.com', 3);

INSERT INTO Categories (name)
VALUES ('Безопасность');

INSERT INTO Requests (request_number, topic, description, priority, category_id, status_id, requester_id)
VALUES ('REQ-2026-009', 'Настройка антивируса', 'Установить антивирус на рабочем компьютере.', 'Средний', 2, 1, 4);

INSERT INTO Comments (request_id, author_id, text)
VALUES (1, 2, 'Заявка принята в обработку, ожидайте.');

INSERT INTO RequestHistory (request_id, user_id, action, old_value, new_value)
VALUES (1, 2, 'Изменение статуса', 'Новая', 'В работе');

-- 2. SELECT — простые выборки 

SELECT * FROM Roles;

SELECT u.id, u.full_name, u.login, r.name AS role
FROM Users u
JOIN Roles r ON u.role_id = r.id;

SELECT * FROM Categories;

SELECT * FROM Statuses;

SELECT * FROM Requests
ORDER BY created_at DESC;

-- 3. SELECT с WHERE — фильтрация 

SELECT id, request_number, topic, status_id
FROM Requests
WHERE status_id = 1;

SELECT id, request_number, topic, priority
FROM Requests
WHERE priority = 'Высокий';

SELECT id, request_number, topic, created_at
FROM Requests
WHERE created_at BETWEEN '2026-10-01' AND '2026-10-03';

-- 4. SELECT с JOIN — объединение таблиц 

SELECT 
    c.id,
    c.text,
    u.full_name AS author,
    r.request_number,
    c.created_at
FROM Comments c
JOIN Users u ON c.author_id = u.id
JOIN Requests r ON c.request_id = r.id;

-- 5. UPDATE — изменение данных 

UPDATE Requests
SET status_id = 2
WHERE id = 1;

UPDATE Requests
SET assignee_id = 3
WHERE id = 6;

-- 6. DELETE — удаление данных 

DELETE FROM Comments
WHERE id = 1;

DELETE FROM Requests
WHERE id = 8;
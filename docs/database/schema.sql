PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS RequestHistory;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Requests;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Statuses;
DROP TABLE IF EXISTS Roles;

CREATE TABLE Roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role_id INTEGER NOT NULL,

    FOREIGN KEY (role_id)
        REFERENCES Roles(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Statuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_number TEXT NOT NULL UNIQUE,
    topic TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'Средний',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    category_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    requester_id INTEGER NOT NULL,
    assignee_id INTEGER,

    FOREIGN KEY (category_id)
        REFERENCES Categories(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (status_id)
        REFERENCES Statuses(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (requester_id)
        REFERENCES Users(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (assignee_id)
        REFERENCES Users(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE Comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (request_id)
        REFERENCES Requests(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (author_id)
        REFERENCES Users(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE RequestHistory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (request_id)
        REFERENCES Requests(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (user_id)
        REFERENCES Users(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Ускорение поиска
CREATE INDEX idx_request_status ON Requests(status_id);
CREATE INDEX idx_request_category ON Requests(category_id);
CREATE INDEX idx_request_requester ON Requests(requester_id);
CREATE INDEX idx_request_assignee ON Requests(assignee_id);
CREATE INDEX idx_comment_request ON Comments(request_id);
CREATE INDEX idx_history_request ON RequestHistory(request_id);
CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serial TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE fee_uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class TEXT NOT NULL,         -- Form1–Form6
    stream TEXT NOT NULL,        -- e.g. A, B, Science, Arts
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    extension TEXT,
    uploaded_by TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fee_date DATE NOT NULL       -- date entered by admin
);

CREATE TABLE meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,          -- Meeting title
    platform TEXT NOT NULL,       -- 'google' or 'zoom'
    link TEXT NOT NULL,           -- Meeting URL
    date TEXT NOT NULL,           -- YYYY-MM-DD
    time TEXT NOT NULL,           -- HH:MM
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


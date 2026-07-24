CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serial TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin','teacher','student','parent')) NOT NULL,
    class_stream TEXT NOT NULL
);



CREATE TABLE result_uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class TEXT NOT NULL,         -- Form1–Form6
    stream TEXT NOT NULL,        -- e.g. A, B, Science, Arts
    filename TEXT NOT NULL,      -- original file name
    filepath TEXT NOT NULL,      -- server storage path
    extension TEXT,              -- file extension (.pdf, .xlsx, etc.)
    uploaded_by TEXT,            -- admin username
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    exam_date DATE NOT NULL      -- date entered by admin
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


CREATE TABLE IF NOT EXISTS suspensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    reason TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS parental_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_name TEXT NOT NULL,
    email TEXT NOT NULL,
    contact_number TEXT,
    suggestion TEXT NOT NULL,
    approved BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE joining_instructions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    original_name TEXT NOT NULL,
    uploader TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_type TEXT,
    size INTEGER
);
-- Books
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    category TEXT, -- Science/Arts/Business
    uploaded_by TEXT,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Home Packages
CREATE TABLE packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    category TEXT,
    stream TEXT,
    class_name TEXT,
    uploaded_by TEXT,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT,
    description TEXT
);

CREATE TABLE pastpapers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    category TEXT,
    class_name TEXT,
    year INTEGER,
    uploaded_by TEXT,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE downloads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER,
    file_type TEXT,
    user TEXT,
    downloaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    target_role TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- Attendance table
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    class_stream TEXT NOT NULL,
    date DATE NOT NULL,
    status TEXT CHECK(status IN ('Present','Absent','Late','Sick','Excuse')) NOT NULL,
    marked_by TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id)
);


-- Chat table
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    channel TEXT NOT NULL,
    message TEXT NOT NULL,
    tag TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Admins
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    serial TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin','teacher','student','parent')) NOT NULL
);

-- Fee uploads
CREATE TABLE fee_uploads (
    id SERIAL PRIMARY KEY,
    class TEXT NOT NULL,
    stream TEXT NOT NULL,
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    extension TEXT,
    uploaded_by TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fee_date DATE NOT NULL
);

-- Meetings
CREATE TABLE meetings (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    platform TEXT NOT NULL,
    link TEXT NOT NULL,
    date DATE NOT NULL,
    time TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Latecomers
CREATE TABLE latecomers (
    id SERIAL PRIMARY KEY,
    student_name TEXT NOT NULL,
    expected_opening DATE NOT NULL,
    arrival_date DATE NOT NULL,
    punishment TEXT,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Suspensions
CREATE TABLE suspensions (
    id SERIAL PRIMARY KEY,
    student_name TEXT NOT NULL,
    reason TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Parental suggestions
CREATE TABLE parental_suggestions (
    id SERIAL PRIMARY KEY,
    parent_name TEXT NOT NULL,
    email TEXT NOT NULL,
    contact_number TEXT,
    suggestion TEXT NOT NULL,
    approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Joining instructions
CREATE TABLE joining_instructions (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    original_name TEXT NOT NULL,
    uploader TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_type TEXT,
    size INTEGER
);

-- Books
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    category TEXT,
    uploaded_by TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Packages
CREATE TABLE packages (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    category TEXT,
    stream TEXT,
    class_name TEXT,
    uploaded_by TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Links
CREATE TABLE links (
    id SERIAL PRIMARY KEY,
    title TEXT,
    url TEXT,
    description TEXT
);

-- Pastpapers
CREATE TABLE pastpapers (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    category TEXT,
    class_name TEXT,
    year INTEGER,
    uploaded_by TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Downloads
CREATE TABLE downloads (
    id SERIAL PRIMARY KEY,
    file_id INTEGER,
    file_type TEXT,
    user TEXT,
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notifications
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    message TEXT,
    target_role TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attendance
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_stream TEXT NOT NULL,
    date DATE NOT NULL,
    status TEXT CHECK(status IN ('Present','Absent','Late','Sick','Excuse')) NOT NULL,
    marked_by TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat messages
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    sender TEXT NOT NULL,
    channel TEXT NOT NULL,
    message TEXT NOT NULL,
    tag TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admin
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');

-- =========================
-- Students: 20 per stream
-- =========================

-- Form1A
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882F1A001', 'userpass1', 'student', 'Form1A'),
('S4882F1A002', 'userpass2', 'student', 'Form1A'),
('S4882F1A003', 'userpass3', 'student', 'Form1A'),
('S4882F1A004', 'userpass4', 'student', 'Form1A'),
('S4882F1A005', 'userpass5', 'student', 'Form1A'),
('S4882F1A006', 'userpass6', 'student', 'Form1A'),
('S4882F1A007', 'userpass7', 'student', 'Form1A'),
('S4882F1A008', 'userpass8', 'student', 'Form1A'),
('S4882F1A009', 'userpass9', 'student', 'Form1A'),
('S4882F1A010', 'userpass10', 'student', 'Form1A'),
('S4882F1A011', 'userpass11', 'student', 'Form1A'),
('S4882F1A012', 'userpass12', 'student', 'Form1A'),
('S4882F1A013', 'userpass13', 'student', 'Form1A'),
('S4882F1A014', 'userpass14', 'student', 'Form1A'),
('S4882F1A015', 'userpass15', 'student', 'Form1A'),
('S4882F1A016', 'userpass16', 'student', 'Form1A'),
('S4882F1A017', 'userpass17', 'student', 'Form1A'),
('S4882F1A018', 'userpass18', 'student', 'Form1A'),
('S4882F1A019', 'userpass19', 'student', 'Form1A'),
('S4882F1A020', 'userpass20', 'student', 'Form1A');

-- Form1B
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882F1B001', 'userpass21', 'student', 'Form1B'),
('S4882F1B002', 'userpass22', 'student', 'Form1B'),
...
('S4882F1B020', 'userpass40', 'student', 'Form1B');

-- Form1C
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882F1C001', 'userpass41', 'student', 'Form1C'),
...
('S4882F1C020', 'userpass60', 'student', 'Form1C');

-- Form1D
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882F1D001', 'userpass61', 'student', 'Form1D'),
...
('S4882F1D020', 'userpass80', 'student', 'Form1D');

-- Form1E
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882F1E001', 'userpass81', 'student', 'Form1E'),
...
('S4882F1E020', 'userpass100', 'student', 'Form1E');

-- Form2A–E (S4882F2A001 → S4882F2E020)
-- Form3A–E (S4882F3A001 → S4882F3E020)
-- Form4A–E (S4882F4A001 → S4882F4E020)

-- =========================
-- Teachers: 1 per stream
-- =========================
INSERT INTO users (serial, password, role, class_stream) VALUES
('TeacherF1A#', 'Teacher@123#', 'teacher', 'Form1A'),
('TeacherF1B#', 'Teacher@123#', 'teacher', 'Form1B'),
('TeacherF1C#', 'Teacher@123#', 'teacher', 'Form1C'),
('TeacherF1D#', 'Teacher@123#', 'teacher', 'Form1D'),
('TeacherF1E#', 'Teacher@123#', 'teacher', 'Form1E'),

('TeacherF2A#', 'Teacher@123#', 'teacher', 'Form2A'),
('TeacherF2B#', 'Teacher@123#', 'teacher', 'Form2B'),
('TeacherF2C#', 'Teacher@123#', 'teacher', 'Form2C'),
('TeacherF2D#', 'Teacher@123#', 'teacher', 'Form2D'),
('TeacherF2E#', 'Teacher@123#', 'teacher', 'Form2E'),

('TeacherF3A#', 'Teacher@123#', 'teacher', 'Form3A'),
('TeacherF3B#', 'Teacher@123#', 'teacher', 'Form3B'),
('TeacherF3C#', 'Teacher@123#', 'teacher', 'Form3C'),
('TeacherF3D#', 'Teacher@123#', 'teacher', 'Form3D'),
('TeacherF3E#', 'Teacher@123#', 'teacher', 'Form3E'),

('TeacherF4A#', 'Teacher@123#', 'teacher', 'Form4A'),
('TeacherF4B#', 'Teacher@123#', 'teacher', 'Form4B'),
('TeacherF4C#', 'Teacher@123#', 'teacher', 'Form4C'),
('TeacherF4D#', 'Teacher@123#', 'teacher', 'Form4D'),
('TeacherF4E#', 'Teacher@123#', 'teacher', 'Form4E');

-- Admin
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');

-- =========================
-- Students: 20 per stream
-- =========================

-- Form1A
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882.0001.2020', 'userpass1', 'student', 'Form1A'),
('S4882.0002.2020', 'userpass2', 'student', 'Form1A'),
...
('S4882.0020.2020', 'userpass20', 'student', 'Form1A');

-- Form1B
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882.0021.2020', 'userpass21', 'student', 'Form1B'),
...
('S4882.0040.2020', 'userpass40', 'student', 'Form1B');

-- Continue same pattern for Form1C, Form1D, Form1E
-- Then repeat for Form2A–E, Form3A–E, Form4A–E
-- Each stream gets 20 students with incrementing serials and passwords

-- =========================
-- Teachers: 1 per stream
-- =========================
INSERT INTO users (serial, password, role, class_stream) VALUES
('T001', 'Teacher@123#', 'teacher', 'Form1A'),
('T002', 'Teacher@123#', 'teacher', 'Form1B'),
('T003', 'Teacher@123#', 'teacher', 'Form1C'),
('T004', 'Teacher@123#', 'teacher', 'Form1D'),
('T005', 'Teacher@123#', 'teacher', 'Form1E'),

('T006', 'Teacher@123#', 'teacher', 'Form2A'),
('T007', 'Teacher@123#', 'teacher', 'Form2B'),
('T008', 'Teacher@123#', 'teacher', 'Form2C'),
('T009', 'Teacher@123#', 'teacher', 'Form2D'),
('T010', 'Teacher@123#', 'teacher', 'Form2E'),

('T011', 'Teacher@123#', 'teacher', 'Form3A'),
('T012', 'Teacher@123#', 'teacher', 'Form3B'),
('T013', 'Teacher@123#', 'teacher', 'Form3C'),
('T014', 'Teacher@123#', 'teacher', 'Form3D'),
('T015', 'Teacher@123#', 'teacher', 'Form3E'),

('T016', 'Teacher@123#', 'teacher', 'Form4A'),
('T017', 'Teacher@123#', 'teacher', 'Form4B'),
('T018', 'Teacher@123#', 'teacher', 'Form4C'),
('T019', 'Teacher@123#', 'teacher', 'Form4D'),
('T020', 'Teacher@123#', 'teacher', 'Form4E');

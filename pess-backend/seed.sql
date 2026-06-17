-- Admin
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');

-- Students Form1A
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882F1A001', 'userpass1', 'student', 'Form1A'),
('S4882F1A002', 'userpass2', 'student', 'Form1A'),
...
('S4882F1A020', 'userpass20', 'student', 'Form1A');

-- Students Form1B
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882F1B001', 'userpass21', 'student', 'Form1B'),
...
('S4882F1B020', 'userpass40', 'student', 'Form1B');

-- Continue same pattern for Form1C–E, Form2A–E, Form3A–E, Form4A–E

-- Teachers
INSERT INTO users (serial, password, role, class_stream) VALUES
('TeacherF1A#', 'Teacher@123#', 'teacher', 'Form1A'),
('TeacherF1B#', 'Teacher@123#', 'teacher', 'Form1B'),
...
('TeacherF4E#', 'Teacher@123#', 'teacher', 'Form4E');

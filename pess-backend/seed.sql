-- Admin
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');

-- =========================
-- Students: 10 per stream
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
('S4882F1A010', 'userpass10', 'student', 'Form1A');

-- Form1B
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882F1B001', 'userpass11', 'student', 'Form1B'),
('S4882F1B002', 'userpass12', 'student', 'Form1B'),
('S4882F1B003', 'userpass13', 'student', 'Form1B'),
('S4882F1B004', 'userpass14', 'student', 'Form1B'),
('S4882F1B005', 'userpass15', 'student', 'Form1B'),
('S4882F1B006', 'userpass16', 'student', 'Form1B'),
('S4882F1B007', 'userpass17', 'student', 'Form1B'),
('S4882F1B008', 'userpass18', 'student', 'Form1B'),
('S4882F1B009', 'userpass19', 'student', 'Form1B'),
('S4882F1B010', 'userpass20', 'student', 'Form1B');

-- Form1C
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882F1C001', 'userpass21', 'student', 'Form1C'),
('S4882F1C002', 'userpass22', 'student', 'Form1C'),
('S4882F1C003', 'userpass23', 'student', 'Form1C'),
('S4882F1C004', 'userpass24', 'student', 'Form1C'),
('S4882F1C005', 'userpass25', 'student', 'Form1C'),
('S4882F1C006', 'userpass26', 'student', 'Form1C'),
('S4882F1C007', 'userpass27', 'student', 'Form1C'),
('S4882F1C008', 'userpass28', 'student', 'Form1C'),
('S4882F1C009', 'userpass29', 'student', 'Form1C'),
('S4882F1C010', 'userpass30', 'student', 'Form1C');

-- Form1D
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882F1D001', 'userpass31', 'student', 'Form1D'),
('S4882F1D002', 'userpass32', 'student', 'Form1D'),
('S4882F1D003', 'userpass33', 'student', 'Form1D'),
('S4882F1D004', 'userpass34', 'student', 'Form1D'),
('S4882F1D005', 'userpass35', 'student', 'Form1D'),
('S4882F1D006', 'userpass36', 'student', 'Form1D'),
('S4882F1D007', 'userpass37', 'student', 'Form1D'),
('S4882F1D008', 'userpass38', 'student', 'Form1D'),
('S4882F1D009', 'userpass39', 'student', 'Form1D'),
('S4882F1D010', 'userpass40', 'student', 'Form1D');

-- Form1E
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882F1E001', 'userpass41', 'student', 'Form1E'),
('S4882F1E002', 'userpass42', 'student', 'Form1E'),
('S4882F1E003', 'userpass43', 'student', 'Form1E'),
('S4882F1E004', 'userpass44', 'student', 'Form1E'),
('S4882F1E005', 'userpass45', 'student', 'Form1E'),
('S4882F1E006', 'userpass46', 'student', 'Form1E'),
('S4882F1E007', 'userpass47', 'student', 'Form1E'),
('S4882F1E008', 'userpass48', 'student', 'Form1E'),
('S4882F1E009', 'userpass49', 'student', 'Form1E'),
('S4882F1E010', 'userpass50', 'student', 'Form1E');

-- =========================
-- Teachers: 1 per stream
-- =========================
INSERT INTO users (serial, password, role, class_stream) VALUES
('TeacherF1A#', 'Teacher@123#', 'teacher', 'Form1A'),
('TeacherF1B#', 'Teacher@123#', 'teacher', 'Form1B'),
('TeacherF1C#', 'Teacher@123#', 'teacher', 'Form1C'),
('TeacherF1D#', 'Teacher@123#', 'teacher', 'Form1D'),
('TeacherF1E#', 'Teacher@123#', 'teacher', 'Form1E');

-- Example students in users table
INSERT INTO users (id, serial, username, role, class_stream)
VALUES 
(1, 'S4882F1E001', 'John Wurtz', 'student', 'Form1A'),
(2, 'S4882F1E002', 'Mary Ann', 'student', 'Form1B');

-- Example latecomers tied to users.id
-- Admin account
INSERT INTO users (serial, username, role, class_stream, password)
VALUES ('ADMIN001', 'System Admin', 'admin', NULL, 'Admin@123');

-- Student accounts
INSERT INTO users (serial, username, role, class_stream, password)
VALUES ('S4882F1E001', 'John Wurtz', 'student', 'Form1A', 'Student@123');









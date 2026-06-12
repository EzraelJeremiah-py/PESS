-- Admins
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');

-- Students
INSERT INTO users (serial, password, role) VALUES ('S4882.0001.2020', 'userpass1', 'student');
INSERT INTO users (serial, password, role) VALUES ('S4882.0002.2020', 'userpass2', 'student');

-- Teachers
INSERT INTO users (serial, password, role) VALUES ('T001', 'Teacher@123#', 'teacher');
INSERT INTO users (serial, password, role) VALUES ('T002', 'Teacher@123#', 'teacher');

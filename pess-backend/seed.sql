-- Admins
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');

-- Students
INSERT INTO users (serial, password, role, class_stream) 
VALUES ('S4882.0001.2020', 'userpass1', 'student', 'Form1A');

INSERT INTO users (serial, password, role, class_stream) 
VALUES ('S4882.0002.2020', 'userpass2', 'student', 'Form1B');



-- Parents (optional example)
INSERT INTO users (serial, password, role, class_stream) 
VALUES ('P001', 'Parent@123#', 'parent', 'Form1A');

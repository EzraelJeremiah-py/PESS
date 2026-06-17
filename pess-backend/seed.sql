-- Admins
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');

-- Students
INSERT INTO users (serial, password, role, class_stream) 
VALUES ('S4882.0001.2020', 'userpass1', 'student', 'Form1A');
INSERT INTO users (serial, password, role, class_stream) 
VALUES ('S4882.0002.2020', 'userpass2', 'student', 'Form1A');
INSERT INTO users (serial, password, role, class_stream) 
VALUES ('S4882.0003.2020', 'userpass3', 'student', 'Form1A');
INSERT INTO users (serial, password, role, class_stream) 
VALUES ('S4882.0004.2020', 'userpass4', 'student', 'Form1A');

INSERT INTO users (serial, password, role, class_stream) 
VALUES ('S4882.0005.2020', 'userpass5', 'student', 'Form1B');
INSERT INTO users (serial, password, role, class_stream) 
VALUES ('S4882.0006.2020', 'userpass6', 'student', 'Form1B');
INSERT INTO users (serial, password, role, class_stream) 
VALUES ('S4882.0007.2020', 'userpass7', 'student', 'Form1B');
INSERT INTO users (serial, password, role, class_stream) 
VALUES ('S4882.0008.2020', 'userpass8', 'student', 'Form1B');



-- Teachers
INSERT INTO users (serial, password, role, class_stream) 
VALUES ('T001', 'Teacher@123#', 'teacher', 'Form1A');

INSERT INTO users (serial, password, role, class_stream) 
VALUES ('T002', 'Teacher@123#', 'teacher', 'Form1B');

-- Parents
INSERT INTO users (serial, password, role, class_stream) 
VALUES ('P001', 'Parent@123#', 'parent', 'Form1A');

-- Admins table seed
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');


-- Students
INSERT INTO users (username, serial, password, role)
VALUES ('S4882.0001.2020', 'S4882.0001.2020', 'userpass1', 'student');

INSERT INTO users (username, serial, password, role)
VALUES ('S4882.0002.2020', 'S4882.0002.2020', 'userpass2', 'student');


INSERT INTO users (username, serial, password, role)
VALUES ('S4882.0003.2020', 'S4882.0003.2020', 'userpass3', 'student');


-- Teachers
INSERT INTO users (username, serial, password, role)
VALUES ('T001', 'T001', 'Teacher@123#', 'teacher');

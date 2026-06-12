-- Admins table seed
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');

-- Users table seed
INSERT INTO users (serial, password) VALUES ('S4882.0001.2020', 'userpass1');
INSERT INTO users (serial, password) VALUES ('S4882.0002.2020', 'userpass2');
INSERT INTO users (serial, password) VALUES ('S4882.0003.2020', 'userpass3');


-- Admins table seed
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');


-- Teachers table seed
INSERT INTO users (username, serial, password, role) 
VALUES ('Ezrael Jeremiah', 'T001', 'Teacher@123#', 'teacher');

INSERT INTO users (username, serial, password, role) 
VALUES ('Mary John', 'T002', 'Teacher@123#', 'teacher');

INSERT INTO users (username, serial, password, role) 
VALUES ('Peter Smith', 'T003', 'Teacher@123#', 'teacher');

INSERT INTO users (username, serial, password, role) 
VALUES ('Grace Daniel', 'T004', 'Teacher@123#', 'teacher');


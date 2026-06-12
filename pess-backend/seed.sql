-- Admins table seed
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');

-- Users table seed (students only, no role column yet)
INSERT INTO users (serial, password) VALUES ('S4882.0001.2020', 'userpass1');
INSERT INTO users (serial, password) VALUES ('S4882.0002.2020', 'userpass2');
INSERT INTO users (serial, password) VALUES ('S4882.0003.2020', 'userpass3');

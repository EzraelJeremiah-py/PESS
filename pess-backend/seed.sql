-- Admin
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');

-- =========================
-- Students: 10 per stream
-- =========================

-- Form1A
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882.0001.2020', 'userpass1#', 'student', 'Form1A'),
('S4882.0002.2020', 'userpass2#', 'student', 'Form1A'),
('S4882.0003.2020', 'userpass3#', 'student', 'Form1A'),
('S4882.0004.2020', 'userpass4#', 'student', 'Form1A'),
('S4882.0005.2020', 'userpass5#', 'student', 'Form1A'),
('S4882.0006.2020', 'userpass6#', 'student', 'Form1A'),
('S4882.0007.2020', 'userpass7#', 'student', 'Form1A'),
('S4882.0008.2020', 'userpass8#', 'student', 'Form1A'),
('S4882.0009.2020', 'userpass9#', 'student', 'Form1A'),
('S4882.0010.2020', 'userpass10#', 'student', 'Form1A');

-- Form1B
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882.0011.2020', 'userpass11#', 'student', 'Form1B'),
('S4882.0012.2020', 'userpass12#', 'student', 'Form1B'),
('S4882.0013.2020', 'userpass13#', 'student', 'Form1B'),
('S4882.0014.2020', 'userpass14#', 'student', 'Form1B'),
('S4882.0015.2020', 'userpass15#', 'student', 'Form1B'),
('S4882.0016.2020', 'userpass16#', 'student', 'Form1B'),
('S4882.0017.2020', 'userpass17#', 'student', 'Form1B'),
('S4882.0018.2020', 'userpass18#', 'student', 'Form1B'),
('S4882.0019.2020', 'userpass19#', 'student', 'Form1B'),
('S4882.0020.2020', 'userpass20#', 'student', 'Form1B');

-- Form1C
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882.0021.2020', 'userpass21#', 'student', 'Form1C'),
('S4882.0022.2020', 'userpass22#', 'student', 'Form1C'),
('S4882.0023.2020', 'userpass23#', 'student', 'Form1C'),
('S4882.0024.2020', 'userpass24#', 'student', 'Form1C'),
('S4882.0025.2020', 'userpass25#', 'student', 'Form1C'),
('S4882.0026.2020', 'userpass26#', 'student', 'Form1C'),
('S4882.0027.2020', 'userpass27#', 'student', 'Form1C'),
('S4882.0028.2020', 'userpass28#', 'student', 'Form1C'),
('S4882.0029.2020', 'userpass29#', 'student', 'Form1C'),
('S4882.0030.2020', 'userpass30#', 'student', 'Form1C');

-- Form1D
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882.0031.2020', 'userpass31#', 'student', 'Form1D'),
('S4882.0032.2020', 'userpass32#', 'student', 'Form1D'),
('S4882.0033.2020', 'userpass33#', 'student', 'Form1D'),
('S4882.0034.2020', 'userpass34#', 'student', 'Form1D'),
('S4882.0035.2020', 'userpass35#', 'student', 'Form1D'),
('S4882.0036.2020', 'userpass36#', 'student', 'Form1D'),
('S4882.0037.2020', 'userpass37#', 'student', 'Form1D'),
('S4882.0038.2020', 'userpass38#', 'student', 'Form1D'),
('S4882.0039.2020', 'userpass39#', 'student', 'Form1D'),
('S4882.0040.2020', 'userpass40#', 'student', 'Form1D');

-- Form1E
INSERT INTO users (serial, password, role, class_stream) VALUES
('S4882.0041.2020', 'userpass41#', 'student', 'Form1E'),
('S4882.0042.2020', 'userpass42#', 'student', 'Form1E'),
('S4882.0043.2020', 'userpass43#', 'student', 'Form1E'),
('S4882.0044.2020', 'userpass44#', 'student', 'Form1E'),
('S4882.0045.2020', 'userpass45#', 'student', 'Form1E'),
('S4882.0046.2020', 'userpass46#', 'student', 'Form1E'),
('S4882.0047.2020', 'userpass47#', 'student', 'Form1E'),
('S4882.0048.2020', 'userpass48#', 'student', 'Form1E'),
('S4882.0049.2020', 'userpass49#', 'student', 'Form1E'),
('S4882.0050.2020', 'userpass50#', 'student', 'Form1E');

-- =========================
-- Teachers: 1 per stream
-- =========================
INSERT INTO users (serial, password, role, class_stream) VALUES
('TeacherF1A#', 'Teacher@123#', 'teacher', 'Form1A'),
('TeacherF1B#', 'Teacher@123#', 'teacher', 'Form1B'),
('TeacherF1C#', 'Teacher@123#', 'teacher', 'Form1C'),
('TeacherF1D#', 'Teacher@123#', 'teacher', 'Form1D'),
('TeacherF1E#', 'Teacher@123#', 'teacher', 'Form1E');

import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "pess.db")

def run_migrations():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    with open("fix_unique_serial.sql", "r") as f:
        cur.executescript(f.read())
    conn.commit()
    conn.close()

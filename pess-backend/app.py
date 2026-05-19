from flask import Flask, redirect, url_for
from routes import blueprints
import sqlite3, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_PATH = os.path.join(os.path.dirname(__file__), "pess.db")

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        base_dir = os.path.dirname(__file__)
        with open(os.path.join(base_dir, "schema.sql"), "r") as f:
            conn.executescript(f.read())
        with open(os.path.join(base_dir, "seed.sql"), "r") as f:
            conn.executescript(f.read())
        conn.close()
        print("✅ Database initialized")

def run_migrations():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "fix_unique_serial.sql"), "r") as f:
        cur.executescript(f.read())
    conn.commit()
    conn.close()
    print("🔒 Migrations applied (unique constraints enforced)")

# ✅ Run DB setup and migrations at startup
init_db()
run_migrations()

# Register blueprints
for bp in blueprints:
    app.register_blueprint(bp)

@app.route("/")
def index():
    return redirect(url_for("auth.login"))  # or return "Welcome to PESS Backend!"

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, redirect, url_for, session, render_template, flash
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
        try:
            cur.executescript(f.read())
            print("🔒 Migrations applied (unique constraints enforced)")
        except sqlite3.OperationalError as e:
            # Skip duplicate column errors or other conflicts
            print(f"⚠️ Migration skipped: {e}")
    conn.commit()
    conn.close()

# ✅ Run DB setup and migrations at startup
init_db()
run_migrations()

# Register blueprints
for bp in blueprints:
    app.register_blueprint(bp)

@app.route("/")
def index():
    # If logged in, send to the right dashboard
    if "role" in session:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Recent activity: last 5 files and safe links
        try:
            cur.execute("SELECT * FROM library ORDER BY uploaded_at DESC LIMIT 5")
            recent_files = cur.fetchall()
        except sqlite3.Error:
            recent_files = []

        try:
            cur.execute("SELECT * FROM safe_links ORDER BY id DESC LIMIT 5")
            recent_links = cur.fetchall()
        except sqlite3.Error:
            recent_links = []

        conn.close()

        if session["role"] == "admin":
            return render_template("admin_dashboard.html",
                                   user_count=query_count("users"),
                                   file_count=query_count("library"),
                                   link_count=query_count("safe_links"),
                                   recent_files=recent_files,
                                   recent_links=recent_links)
        elif session["role"] == "user":
            return render_template("user_dashboard.html",
                                   file_count=query_count("library"),
                                   link_count=query_count("safe_links"),
                                   recent_files=recent_files,
                                   recent_links=recent_links)

    # If not logged in, send to login
    return redirect(url_for("auth.login"))

def query_count(table):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        conn.close()
        return count
    except sqlite3.Error:
        return 0

if __name__ == "__main__":
    app.run(debug=True)

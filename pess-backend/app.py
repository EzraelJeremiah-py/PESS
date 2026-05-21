from flask import Flask, render_template, redirect, url_for
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

init_db()

# Register blueprints
for bp in blueprints:
    app.register_blueprint(bp)

# 🔹 Root route → login page
@app.route("/")
def index():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)

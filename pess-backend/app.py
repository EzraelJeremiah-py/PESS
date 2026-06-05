from flask import Flask, render_template, redirect, url_for
from routes import blueprints
import sqlite3, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ✅ Absolute path to pess.db
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "pess.db")
app.config["JOINING_FOLDER"] = os.path.join(BASE_DIR, "uploads/joining")
os.makedirs(app.config["JOINING_FOLDER"], exist_ok=True)

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        with open(os.path.join(BASE_DIR, "schema.sql"), "r") as f:
            conn.executescript(f.read())
        with open(os.path.join(BASE_DIR, "seed.sql"), "r") as f:
            conn.executescript(f.read())
        conn.close()
        print("✅ Database initialized")

# Initialize DB if missing
init_db()

# Register all blueprints (auth, user, admin, etc.)
for bp in blueprints:
    app.register_blueprint(bp)

# 🔹 Root route → redirect to login blueprint
@app.route("/")
def index():
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)

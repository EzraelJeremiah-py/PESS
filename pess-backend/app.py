from flask import Flask, render_template, redirect, url_for
from routes import blueprints
import psycopg2, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ✅ Postgres connection
def get_db_connection():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return conn

# Register all blueprints (auth, user, admin, etc.)
for bp in blueprints:
    app.register_blueprint(bp)

# 🔹 Root route → redirect to login blueprint
@app.route("/")
def index():
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)

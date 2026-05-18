from flask import Flask
from routes import blueprints
import sqlite3, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_PATH = "pess.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())
        with open("seed.sql", "r") as f:
            conn.executescript(f.read())
        conn.close()
        print("✅ Database initialized")

init_db()

# Register all blueprints
for bp in blueprints:
    app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)


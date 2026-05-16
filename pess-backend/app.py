from flask import Flask
from routes import blueprints

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Register all blueprints from routes/__init__.py
for bp in blueprints:
    app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)

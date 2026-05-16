from flask import Flask
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)


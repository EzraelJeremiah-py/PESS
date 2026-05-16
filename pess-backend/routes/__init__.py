from .auth import auth_bp
from .admin import admin_bp
from .user import user_bp

# This makes it easy to import all blueprints at once
blueprints = [auth_bp, admin_bp, user_bp]


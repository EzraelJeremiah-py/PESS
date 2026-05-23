from .auth import auth_bp
from .admin import admin_bp
from .user import user_bp
from routes.fees import fees_bp
from routes.meeting import meeting_bp


# This makes it easy to import all blueprints at once
blueprints = [auth_bp, admin_bp, user_bp, fees_bp, meeting_bp]

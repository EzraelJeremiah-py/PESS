# routes/__init__.py

from .auth import auth_bp
from .admin import admin_bp
from .user import user_bp
from .fees import fees_bp
from .meeting import meeting_bp
from .late import late_bp
from .suspensions import suspensions_bp
from .parental import parental_bp
from .joining_instructions import joining_bp
from .library import library_bp
from .chat import chat_bp
from .teacher import teacher_bp

# Collect all blueprints in one list
blueprints = [
    auth_bp,
    admin_bp,
    user_bp,
    fees_bp,
    meeting_bp,
    late_bp,
    suspensions_bp,
    parental_bp,
    joining_bp,
    library_bp,
    chat_bp,
    teacher_bp,
]

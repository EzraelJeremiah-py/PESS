from functools import wraps
from flask import session, redirect, url_for

def login_required(role="teacher"):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "role" not in session or session["role"] != role:
                return redirect(url_for("login_bp.login"))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

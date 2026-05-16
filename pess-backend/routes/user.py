from flask import Blueprint, session, redirect, url_for

user_bp = Blueprint("user", __name__)

@user_bp.route("/user/dashboard")
def dashboard():
    if session.get("role") == "user":
        return "User Dashboard"
    return redirect(url_for("auth.login"))


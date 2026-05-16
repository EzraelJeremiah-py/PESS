from flask import Blueprint, session, redirect, url_for

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard")
def dashboard():
    if session.get("role") == "admin":
        return "Admin Dashboard"
    return redirect(url_for("auth.login"))


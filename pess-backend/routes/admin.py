from flask import Blueprint, session, redirect, url_for, render_template

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
def dashboard():
    if session.get("role") == "admin":
        return render_template("admin.html")
    return redirect(url_for("auth.login"))

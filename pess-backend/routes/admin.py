from flask import Blueprint, render_template, session, redirect, url_for

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard", methods=["GET"])
def dashboard():
    if not session.get("is_admin"):
        return redirect(url_for("dashboard.dashboard"))
    return render_template("admin/dashboard.html", username=session.get("username"))

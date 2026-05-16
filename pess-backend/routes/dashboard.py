from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login.login"))
    return render_template(
        "dashboard.html",
        username=session.get("username"),
        is_admin=session.get("is_admin")  # ✅ pass flag to template
    )
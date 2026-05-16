from flask import Blueprint, session, redirect, url_for, render_template

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/dashboard")
def dashboard():
    if session.get("role") == "user":
        return render_template("user.html")
    return redirect(url_for("auth.login"))

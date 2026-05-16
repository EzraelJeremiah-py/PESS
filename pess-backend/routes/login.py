from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):   # ✅ use check_password
            session["user_id"] = user.id
            session["is_admin"] = user.is_admin
            flash("Login successful!", "success")
            if user.is_admin:
                return redirect(url_for("admin.dashboard"))
            else:
                return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")
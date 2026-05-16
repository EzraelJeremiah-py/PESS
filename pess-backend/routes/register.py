from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.user import User

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash("Username already taken!", "danger")
            return render_template("register.html")

        # Create new user
        new_user = User(username=username, is_admin=False)
        new_user.set_password(password)   # ✅ hash password
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login.login"))

    return render_template("register.html")

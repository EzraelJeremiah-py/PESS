from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import re

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin@123#"

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Admin check
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["role"] = "admin"
            return redirect(url_for("admin.dashboard"))

        # User check (serial number format)
        serial_pattern = r"^S\d{4}\.\d{4}\.\d{4}$"
        if re.match(serial_pattern, username):
            # password can be anything
            session["role"] = "user"
            return redirect(url_for("user.dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))

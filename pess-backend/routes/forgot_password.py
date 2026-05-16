from flask import Blueprint, render_template, request, flash, redirect, url_for

forgot_password_bp = Blueprint("forgot_password", __name__)

@forgot_password_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        # For now, just flash a message. Later you can add email reset logic.
        flash("Password reset instructions have been sent to your email (demo).", "info")
        return redirect(url_for("login.login"))
    return render_template("forgot_password.html")

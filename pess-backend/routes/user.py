from flask import Blueprint, render_template, session, flash, redirect, url_for
import sqlite3, os

user_bp = Blueprint("user", __name__, url_prefix="/user")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

# Prevent cached pages after logout
@admin_bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@user_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "student":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    return render_template("user_dashboard.html")

@user_bp.route("/fees")
def view_fees():
    if session.get("role") != "user":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    fee_files = []
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM fee_uploads ORDER BY uploaded_at DESC")
        fee_files = cur.fetchall()
        conn.close()
    except sqlite3.Error as e:
        flash(f"Database error: {e}", "danger")

    return render_template("fees/user_fees.html", fee_files=fee_files)

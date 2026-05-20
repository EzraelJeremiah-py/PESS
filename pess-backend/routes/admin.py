from flask import Blueprint, render_template, session, flash, redirect, url_for
import sqlite3, os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

@admin_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))
    return render_template("admin_dashboard.html")

@admin_bp.route("/users/delete/<int:id>")
def delete_user(id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        flash("User deleted successfully!", "success")
    except sqlite3.Error as e:
        flash(f"Database error: {e}", "danger")

    return redirect(url_for("admin.dashboard"))

from flask import Blueprint, render_template, session, flash, redirect, url_for
import sqlite3

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
DB_PATH = "pess.db"

@admin_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Count users
    cur.execute("SELECT COUNT(*) FROM users")
    user_count = cur.fetchone()[0]

    # Count files in library
    cur.execute("SELECT COUNT(*) FROM library")
    file_count = cur.fetchone()[0]

    # Count safe links
    cur.execute("SELECT COUNT(*) FROM safe_links")
    link_count = cur.fetchone()[0]

    conn.close()

    return render_template("admin_dashboard.html",
                           user_count=user_count,
                           file_count=file_count,
                           link_count=link_count)

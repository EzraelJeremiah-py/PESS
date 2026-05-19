from flask import Blueprint, render_template, session, flash, redirect, url_for
import sqlite3

user_bp = Blueprint("user", __name__, url_prefix="/user")
DB_PATH = "pess.db"

@user_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "user":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Count files in library
    cur.execute("SELECT COUNT(*) FROM library")
    file_count = cur.fetchone()[0]

    # Count safe links
    cur.execute("SELECT COUNT(*) FROM safe_links")
    link_count = cur.fetchone()[0]

    conn.close()

    return render_template("user_dashboard.html",
                           file_count=file_count,
                           link_count=link_count)

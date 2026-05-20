from flask import Blueprint, render_template, session, flash, redirect, url_for
import sqlite3, os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

@admin_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    user_count, file_count, link_count, recent_files, recent_links = 0, 0, 0, [], []

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Counts
        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0] or 0

        cur.execute("SELECT COUNT(*) FROM library")
        file_count = cur.fetchone()[0] or 0

        cur.execute("SELECT COUNT(*) FROM safe_links")
        link_count = cur.fetchone()[0] or 0

        # Recent activity
        cur.execute("SELECT filename FROM library ORDER BY uploaded_at DESC LIMIT 5")
        recent_files = [r["filename"] for r in cur.fetchall()]

        cur.execute("SELECT title, url FROM safe_links ORDER BY id DESC LIMIT 5")
        recent_links = cur.fetchall()

        conn.close()
    except sqlite3.Error as e:
        flash(f"Database error: {e}", "danger")

    return render_template("admin_dashboard.html",
                           user_count=user_count,
                           file_count=file_count,
                           link_count=link_count,
                           recent_files=recent_files,
                           recent_links=recent_links)

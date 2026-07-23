from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os

parental_bp = Blueprint("parental", __name__, url_prefix="/parental")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

@parental_bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# ------------------ Parent: Submit Suggestion ------------------
@parental_bp.route("/", methods=["GET", "POST"])
def parental_form():
    if request.method == "POST":
        parent_name = request.form["parent_name"]
        email = request.form["email"]
        contact_number = request.form["contact_number"]
        suggestion = request.form["suggestion"]

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO parental_suggestions (parent_name, email, contact_number, suggestion, approved)
            VALUES (?, ?, ?, ?, 0)
        """, (parent_name, email, contact_number, suggestion))
        conn.commit()
        conn.close()
        flash("Suggestion submitted! Awaiting admin approval.", "info")
        return redirect(url_for("parental.parental_form"))

    return render_template("parental/parental_form.html")

# ------------------ Admin: Manage Suggestions ------------------
@parental_bp.route("/admin")
def manage_suggestions():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM parental_suggestions ORDER BY created_at DESC")
    suggestions = cur.fetchall()
    conn.close()
    return render_template("parental/manage_suggestions.html", suggestions=suggestions)

@parental_bp.route("/approve/<int:id>")
def approve_suggestion(id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE parental_suggestions SET approved=1 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Suggestion approved!", "success")
    return redirect(url_for("parental.manage_suggestions"))

@parental_bp.route("/delete/<int:id>")
def delete_suggestion(id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM parental_suggestions WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Suggestion deleted!", "danger")
    return redirect(url_for("parental.manage_suggestions"))

# ------------------ Public: View Approved Suggestions ------------------
@parental_bp.route("/recent_suggestions")
def recent_suggestions():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM parental_suggestions WHERE approved=1 ORDER BY created_at DESC")
    suggestions = cur.fetchall()
    conn.close()
    return render_template("parental/recent_suggestions.html", suggestions=suggestions)

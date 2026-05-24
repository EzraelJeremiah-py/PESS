from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os

suspensions_bp = Blueprint("suspensions", __name__, url_prefix="/suspensions")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

# ------------------ Admin: List Suspensions ------------------
@suspensions_bp.route("/")
def list_suspensions():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM suspensions ORDER BY start_date DESC")
    suspensions = cur.fetchall()
    conn.close()
    return render_template("suspensions/suspensions.html", suspensions=suspensions)

# ------------------ Admin: Add Suspension ------------------
@suspensions_bp.route("/add", methods=["GET", "POST"])
def add_suspension():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        student_name = request.form["student_name"]
        reason = request.form["reason"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        status = request.form.get("status", "active")

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO suspensions (student_name, reason, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (student_name, reason, start_date, end_date, status))
        conn.commit()
        conn.close()
        flash("Suspension added successfully!", "success")
        return redirect(url_for("suspensions.list_suspensions"))

    return render_template("suspensions/add_suspension.html")

# ------------------ Admin: Delete Suspension ------------------
@suspensions_bp.route("/delete/<int:id>")
def delete_suspension(id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM suspensions WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Suspension deleted successfully!", "success")
    return redirect(url_for("suspensions.list_suspensions"))

# ------------------ Public View (Students) ------------------
@suspensions_bp.route("/public")
def public_suspensions():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM suspensions ORDER BY start_date DESC")
    suspensions = cur.fetchall()
    conn.close()
    return render_template("suspensions/public_suspensions.html", suspensions=suspensions)

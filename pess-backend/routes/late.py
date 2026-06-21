from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os

late_bp = Blueprint("late", __name__, url_prefix="/late")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

# Admin: List all latecomers
@late_bp.route("/")
def list_latecomers():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM latecomers ORDER BY arrival_date DESC")
    latecomers = cur.fetchall()
    conn.close()
    return render_template("late/latecomers.html", latecomers=latecomers)

# Admin: Add latecomer
@late_bp.route("/add", methods=["GET", "POST"])
def add_latecomer():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        student_serial = request.form["student_serial"]
        student_name = request.form["student_name"]
        expected_opening = request.form["expected_opening"]
        arrival_date = request.form["arrival_date"]
        punishment = request.form["punishment"]
        reason = request.form["reason"]

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO latecomers (student_serial, student_name, expected_opening, arrival_date, punishment, reason)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_serial, student_name, expected_opening, arrival_date, punishment, reason))
        conn.commit()
        conn.close()
        flash("Latecomer added successfully!", "success")
        return redirect(url_for("late.list_latecomers"))

    return render_template("late/add_latecomer.html")

# Admin: Delete latecomer
@late_bp.route("/delete/<int:id>")
def delete_latecomer(id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM latecomers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Latecomer deleted successfully!", "success")
    return redirect(url_for("late.list_latecomers"))

# Student: View own latecomers
@late_bp.route("/user")
def user_latecomer():
    if session.get("role") != "student":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    serial = session.get("serial")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM latecomers WHERE student_serial=?", (serial,))
    latecomers = cur.fetchall()
    conn.close()
    return render_template("late/user_latecomers.html", latecomers=latecomers)

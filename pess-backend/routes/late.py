from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os

late_bp = Blueprint("late", __name__, url_prefix="/late")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

# ------------------ Admin: List Latecomers ------------------
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

# ------------------ Admin: Register Latecomer ------------------
@late_bp.route("/register", methods=["GET", "POST"])
def register_latecomer():
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
        flash("Latecomer registered successfully!", "success")
        return redirect(url_for("late.list_latecomers"))

    return render_template("late/register_latecomer.html")

# ------------------ Admin: Delete Latecomer ------------------
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
    flash("Latecomer record deleted successfully!", "success")
    return redirect(url_for("late.list_latecomers"))

# ------------------ User: View Own Latecomer Record ------------------
@late_bp.route("/user")
def user_latecomer():
    if session.get("role") != "student":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # ✅ Now query by student_serial
    cur.execute("SELECT * FROM latecomers WHERE student_serial=?", (session.get("serial"),))
    late_record = cur.fetchone()
    conn.close()

    return render_template("late/user_latecomer.html", late_record=late_record)

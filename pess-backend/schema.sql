from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os
from datetime import datetime

attendance_bp = Blueprint("attendance", __name__, url_prefix="/attendance")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Attendance Panel (form)
@attendance_bp.route("/panel")
def attendance_panel():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))
    return render_template("attendance_panel.html")


# ✅ Mark Attendance (POST handler)
@attendance_bp.route("/mark", methods=["POST"])
def mark_attendance():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    teacher_username = session.get("username")
    class_stream = request.form.get("class")

    attendance_records = []
    for key, value in request.form.items():
        if key.startswith("student_"):  # e.g. student_a, student_b
            student_name = key.replace("student_", "").capitalize()
            status = value
            attendance_records.append((student_name, class_stream, status))

    conn = get_db_connection()
    cur = conn.cursor()
    for student_name, class_stream, status in attendance_records:
        cur.execute("""
            INSERT INTO attendance (student_id, class_stream, date, status, marked_by, timestamp)
            VALUES (
                (SELECT id FROM students WHERE name=?),
                ?, ?, ?, ?, ?
            )
        """, (student_name, class_stream, datetime.now().date(), status, teacher_username, datetime.now()))
    conn.commit()
    conn.close()

    flash("Attendance saved successfully!", "success")
    return redirect(url_for("teacher.dashboard"))    i think you must loose some important codes something i dont broh

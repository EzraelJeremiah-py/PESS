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
        if key.startswith("student_"):  # e.g. student_101, student_102
            student_serial = key.replace("student_", "")
            status = value
            attendance_records.append((student_serial, class_stream, status))

    conn = get_db_connection()
    cur = conn.cursor()
    for student_serial, class_stream, status in attendance_records:
        cur.execute("""
            INSERT INTO attendance (student_id, class_stream, date, status, marked_by, timestamp)
            VALUES (
                (SELECT id FROM students WHERE serial=?),
                ?, ?, ?, ?, ?
            )
        """, (student_serial, class_stream, datetime.now().date(), status, teacher_username, datetime.now()))
    conn.commit()
    conn.close()

    flash("Attendance saved successfully!", "success")
    return redirect(url_for("teacher.dashboard"))

# ✅ Student Dashboard Attendance
@attendance_bp.route("/my")
def my_attendance():
    if session.get("role") != "student":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    student_serial = session.get("serial")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.date, a.status, a.class_stream, a.marked_by
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE s.serial = ?
        ORDER BY a.date DESC
        LIMIT 10
    """, (student_serial,))
    attendance_history = cur.fetchall()
    conn.close()

    # Render the user dashboard with attendance history
    return render_template("user_dashboard.html", attendance_history=attendance_history)

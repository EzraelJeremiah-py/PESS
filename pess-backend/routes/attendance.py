from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os
from datetime import datetime

attendance_bp = Blueprint("attendance", __name__, url_prefix="/attendance")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Teacher: Attendance Panel
@attendance_bp.route("/panel")
def attendance_panel():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))
    return render_template("attendance_panel.html")

# Teacher: Mark Attendance
@attendance_bp.route("/mark", methods=["POST"])
def mark_attendance():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    teacher_username = session.get("username")
    class_stream = request.form.get("class")

    attendance_records = []
    for key, value in request.form.items():
        if key.startswith("student_"):  # e.g. student_101
            student_serial = key.replace("student_", "")
            status = value
            attendance_records.append((student_serial, class_stream, status))

    conn = get_db_connection()
    cur = conn.cursor()
    for student_serial, class_stream, status in attendance_records:
        cur.execute("""
            INSERT INTO attendance (student_id, class_stream, date, status, marked_by, timestamp)
            VALUES (
                (SELECT id FROM users WHERE serial=? AND role='student'),
                ?, ?, ?, ?, ?
            )
        """, (student_serial, class_stream, datetime.now().date(), status, teacher_username, datetime.now()))
    conn.commit()
    conn.close()

    flash("Attendance saved successfully!", "success")
    return redirect(url_for("teacher.dashboard"))

# Student: Dedicated Attendance View
@attendance_bp.route("/view")
def view_attendance():
    if session.get("role") != "student":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    student_serial = session.get("serial")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.date, a.status, a.class_stream, a.marked_by
        FROM attendance a
        JOIN users u ON a.student_id = u.id
        WHERE u.serial = ? AND u.role='student'
        ORDER BY a.date DESC
    """, (student_serial,))
    attendance_history = cur.fetchall()
    conn.close()

    return render_template("my_attendance.html", attendance_history=attendance_history)

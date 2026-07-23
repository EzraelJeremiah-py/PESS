from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os
from datetime import datetime

attendance_bp = Blueprint("attendance", __name__, url_prefix="/attendance")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

# Prevent cached pages after logout
@admin_bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Attendance Panel (form for teachers)
@attendance_bp.route("/panel")
def attendance_panel():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))
    return render_template("attendance_panel.html")

# ✅ Mark Attendance (POST handler for teachers)
@attendance_bp.route("/mark", methods=["POST"])
def mark_attendance():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    teacher_username = session.get("username")
    class_stream = request.form.get("class")

    attendance_records = []
    for key, value in request.form.items():
        if key.startswith("student_"):  # e.g. student_S4882F1A001
            student_serial = key.replace("student_", "")
            status = value
            attendance_records.append((student_serial, class_stream, status))

    conn = get_db_connection()
    cur = conn.cursor()
    for student_serial, class_stream, status in attendance_records:
        cur.execute("""
            INSERT INTO attendance (student_id, class_stream, date, status, marked_by, timestamp)
            VALUES (
                (SELECT id FROM users WHERE serial=?),
                ?, ?, ?, ?, ?
            )
        """, (student_serial, class_stream, datetime.now().date(), status, teacher_username, datetime.now()))
    conn.commit()
    conn.close()

    flash("Attendance saved successfully!", "success")
    return redirect(url_for("teacher.dashboard"))

# ✅ Student view: see own attendance
@attendance_bp.route("/user")
def user_attendance():
    if session.get("role") != "student":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    student_id = session.get("user_id")  # stored at login
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT date, status, class_stream, marked_by, timestamp
        FROM attendance
        WHERE student_id=?
        ORDER BY date DESC
    """, (student_id,))
    records = cur.fetchall()
    conn.close()
    return render_template("attendance/user_attendance.html", records=records)

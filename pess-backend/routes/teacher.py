from flask import Blueprint, render_template, session, flash, redirect, url_for, request, Response
import sqlite3, os
from datetime import datetime

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")
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

# ✅ Teacher Dashboard
@teacher_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    teacher_serial = session.get("serial")
    teacher_stream = session.get("class_stream")

    # Attendance records marked by this teacher (last 10)
    cur.execute("""
        SELECT a.*, u.serial AS student_serial
        FROM attendance a
        JOIN users u ON a.student_id = u.id
        WHERE a.marked_by = ? AND a.class_stream = ?
        ORDER BY a.timestamp DESC LIMIT 10
    """, (teacher_serial, teacher_stream))
    attendance_records = cur.fetchall()

    # Chat messages sent by this teacher (last 10)
    cur.execute("""
        SELECT * FROM chat_messages
        WHERE sender = ?
        ORDER BY timestamp DESC LIMIT 10
    """, (teacher_serial,))
    chat_messages = cur.fetchall()

    # Notifications targeted to teachers
    try:
        cur.execute("""
            SELECT * FROM notifications
            WHERE target_role = 'teacher'
            ORDER BY created_at DESC LIMIT 10
        """)
        notifications = cur.fetchall()
    except sqlite3.OperationalError:
        notifications = []

    # Stats (scoped to teacher's stream)
    cur.execute("SELECT COUNT(*) AS total_students FROM users WHERE role='student' AND class_stream=?", (teacher_stream,))
    total_students = cur.fetchone()["total_students"]

    cur.execute("SELECT COUNT(*) AS total_classes FROM attendance WHERE marked_by=? AND class_stream=?", (teacher_serial, teacher_stream))
    total_classes = cur.fetchone()["total_classes"]

    cur.execute("SELECT COUNT(*) AS today_attendance FROM attendance WHERE marked_by=? AND class_stream=? AND date=DATE('now')", (teacher_serial, teacher_stream))
    today_attendance = cur.fetchone()["today_attendance"]

    conn.close()

    return render_template("teacher_dashboard.html",
                           attendance_records=attendance_records,
                           chat_messages=chat_messages,
                           notifications=notifications,
                           total_students=total_students,
                           total_classes=total_classes,
                           today_attendance=today_attendance)

# ✅ Attendance Panel (mark attendance)
@teacher_bp.route("/attendance", methods=["GET", "POST"])
def attendance():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    teacher_stream = session.get("class_stream")
    teacher_serial = session.get("serial")

    # Load only students from teacher's stream
    cur.execute("SELECT serial FROM users WHERE role='student' AND class_stream=?", (teacher_stream,))
    students = cur.fetchall()

    if request.method == "POST":
        for key, value in request.form.items():
            if key.startswith("student_"):
                student_serial = key.replace("student_", "")
                cur.execute("""
                    INSERT INTO attendance (student_id, class_stream, date, status, marked_by, timestamp)
                    VALUES ((SELECT id FROM users WHERE serial=? AND role='student'),
                            ?, DATE('now'), ?, ?, ?)
                """, (student_serial, teacher_stream, value, teacher_serial, datetime.now()))
        conn.commit()
        conn.close()

        flash("Attendance saved successfully!", "success")
        return redirect(url_for("teacher.dashboard"))

    conn.close()
    return render_template("attendance_panel.html", students=students)

# ✅ Attendance Logs (with filters)
@teacher_bp.route("/attendance_logs")
def attendance_logs():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    teacher_serial = session.get("serial")
    teacher_stream = session.get("class_stream")

    # Filters
    class_stream = request.args.get("class_stream") or teacher_stream
    date = request.args.get("date")

    query = """
        SELECT a.*, u.serial AS student_serial
        FROM attendance a
        JOIN users u ON a.student_id = u.id
        WHERE a.marked_by = ? AND a.class_stream = ?
    """
    params = [teacher_serial, class_stream]

    if date:
        query += " AND a.date = ?"
        params.append(date)

    query += " ORDER BY a.timestamp DESC"

    cur.execute(query, params)
    attendance_records = cur.fetchall()
    conn.close()

    return render_template("attendance_logs.html", attendance_records=attendance_records)

# ✅ Export Attendance Logs to CSV
@teacher_bp.route("/export_attendance_logs")
def export_attendance_logs():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    teacher_serial = session.get("serial")
    teacher_stream = session.get("class_stream")

    # Filters
    class_stream = request.args.get("class_stream") or teacher_stream
    date = request.args.get("date")

    query = """
        SELECT a.*, u.serial AS student_serial
        FROM attendance a
        JOIN users u ON a.student_id = u.id
        WHERE a.marked_by = ? AND a.class_stream = ?
    """
    params = [teacher_serial, class_stream]

    if date:
        query += " AND a.date = ?"
        params.append(date)

    query += " ORDER BY a.timestamp DESC"

    cur.execute(query, params)
    attendance_records = cur.fetchall()
    conn.close()

    # Build CSV response
    def generate():
        yield "Student Serial,Status,Class Stream,Date,Marked By,Timestamp\n"
        for record in attendance_records:
            yield f"{record['student_serial']},{record['status']},{record['class_stream']},{record['date']},{record['marked_by']},{record['timestamp']}\n"

    return Response(generate(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=attendance_logs.csv"})

# ✅ Chat Zone (send messages)
@teacher_bp.route("/chat", methods=["GET", "POST"])
def chat():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        teacher_serial = session.get("serial")
        channel = request.form.get("channel")
        message = request.form.get("message")
        tag = request.form.get("tag")

        if message.strip():
            cur.execute("""
                INSERT INTO chat_messages (sender, channel, message, tag, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (teacher_serial, channel, message, tag, datetime.now()))
            conn.commit()
            flash("Message sent!", "success")
        else:
            flash("Message cannot be empty!", "warning")

    cur.execute("SELECT * FROM chat_messages ORDER BY timestamp DESC LIMIT 50")
    messages = cur.fetchall()
    conn.close()

    return render_template("chat_zone.html", messages=messages)

# ✅ Chat Logs (view all messages)
@teacher_bp.route("/chat_logs")
def chat_logs():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM chat_messages ORDER BY timestamp DESC LIMIT 100")
    messages = cur.fetchall()
    conn.close()

    return render_template("chat_logs.html", messages=messages)

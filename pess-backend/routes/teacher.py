from flask import Blueprint, render_template, session, flash, redirect, url_for, request
import sqlite3, os
from datetime import datetime

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

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
    return render_template("teacher_dashboard.html")

# ✅ Attendance Panel
@teacher_bp.route("/attendance", methods=["GET", "POST"])
def attendance():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        class_stream = request.form.get("class")
        teacher_serial = session.get("serial")  # use serial instead of username

        conn = get_db_connection()
        cur = conn.cursor()
        for key, value in request.form.items():
            if key.startswith("student_"):
                student_serial = key.replace("student_", "")
                cur.execute("""
                    INSERT INTO attendance (student_id, class_stream, date, status, marked_by, timestamp)
                    VALUES ((SELECT id FROM users WHERE serial=? AND role='student'), ?, DATE('now'), ?, ?, ?)
                """, (student_serial, class_stream, value, teacher_serial, datetime.now()))
        conn.commit()
        conn.close()

        flash("Attendance saved successfully!", "success")
        return redirect(url_for("teacher.dashboard"))

    return render_template("attendance_panel.html")

# ✅ Chat Zone
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

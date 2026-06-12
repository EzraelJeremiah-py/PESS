from flask import Blueprint, render_template, session, flash, redirect, url_for, request
import sqlite3, os

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

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
        teacher_username = session.get("username")

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        for key, value in request.form.items():
            if key.startswith("student_"):
                student_name = key.replace("student_", "").capitalize()
                cur.execute("""
                    INSERT INTO attendance (student_id, class_stream, date, status, marked_by)
                    VALUES ((SELECT id FROM students WHERE name=?), ?, DATE('now'), ?, ?)
                """, (student_name, class_stream, value, teacher_username))
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

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if request.method == "POST":
        teacher_username = session.get("username")
        channel = request.form.get("channel")
        message = request.form.get("message")
        tag = request.form.get("tag")

        cur.execute("""
            INSERT INTO chat_messages (sender, channel, message, tag)
            VALUES (?, ?, ?, ?)
        """, (teacher_username, channel, message, tag))
        conn.commit()

    cur.execute("SELECT * FROM chat_messages ORDER BY timestamp DESC LIMIT 50")
    messages = cur.fetchall()
    conn.close()

    return render_template("chat_zone.html", messages=messages)

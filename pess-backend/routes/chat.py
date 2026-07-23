from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os
from datetime import datetime

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

@chat_bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Chat Zone (view + send)
@chat_bp.route("/zone", methods=["GET", "POST"])
def chat_zone():
    if session.get("role") != "teacher":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        sender = session.get("username")
        channel = request.form.get("channel")
        message = request.form.get("message")
        tag = request.form.get("tag")

        if not message.strip():
            flash("Message cannot be empty!", "warning")
        else:
            cur.execute("""
                INSERT INTO chat_messages (sender, channel, message, tag, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (sender, channel, message, tag, datetime.now()))
            conn.commit()
            flash("Message sent!", "success")

    # Load latest 50 messages
    cur.execute("SELECT * FROM chat_messages ORDER BY timestamp DESC LIMIT 50")
    messages = cur.fetchall()
    conn.close()

    return render_template("chat_zone.html", messages=messages)

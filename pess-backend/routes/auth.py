from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os

meeting_bp = Blueprint("meeting", __name__, url_prefix="/meeting")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

# ------------------ Admin: List Meetings ------------------
@meeting_bp.route("/")
def list_meetings():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM meetings ORDER BY date, time")
    meetings = cur.fetchall()
    conn.close()
    return render_template("meetings/meetings.html", meetings=meetings)

# ------------------ Admin: Create Meeting ------------------
@meeting_bp.route("/create", methods=["GET", "POST"])
def create_meeting():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        title = request.form["title"]
        platform = request.form["platform"]
        link = request.form["link"]
        date = request.form["date"]
        time = request.form["time"]

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO meetings (title, platform, link, date, time) VALUES (?, ?, ?, ?, ?)",
            (title, platform, link, date, time)
        )
        conn.commit()
        conn.close()
        flash("Meeting created successfully!", "success")
        return redirect(url_for("meeting.list_meetings"))

    return render_template("meetings/create_meeting.html")

# ------------------ Admin: Manage Meeting ------------------
@meeting_bp.route("/manage/<int:id>", methods=["GET", "POST"])
def manage_meeting(id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        platform = request.form["platform"]
        link = request.form["link"]
        date = request.form["date"]
        time = request.form["time"]

        cur.execute(
            "UPDATE meetings SET title=?, platform=?, link=?, date=?, time=? WHERE id=?",
            (title, platform, link, date, time, id)
        )
        conn.commit()
        conn.close()
        flash("Meeting updated successfully!", "success")
        return redirect(url_for("meeting.list_meetings"))

    cur.execute("SELECT * FROM meetings WHERE id=?", (id,))
    meeting = cur.fetchone()
    conn.close()
    return render_template("meetings/manage_meeting.html", meeting=meeting)

# ------------------ Admin: Delete Meeting ------------------
@meeting_bp.route("/delete/<int:id>")
def delete_meeting(id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM meetings WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Meeting deleted successfully!", "success")
    return redirect(url_for("meeting.list_meetings"))

# ------------------ Student: View & Join Meetings ------------------
@meeting_bp.route("/user")
def user_meetings():
    if session.get("role") != "student":   # ✅ fixed: match login role
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM meetings ORDER BY date, time")
    meetings = cur.fetchall()
    conn.close()

    return render_template("meetings/user_meetings.html", meetings=meetings)

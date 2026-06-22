from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os

late_bp = Blueprint("late", __name__, url_prefix="/late")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

# -----------------------------
# Admin: List all latecomers
# -----------------------------
@late_bp.route("/")
def list_latecomers():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT l.*, u.username, u.serial, u.class_stream
        FROM latecomers l
        JOIN users u ON l.student_id = u.id
        ORDER BY l.arrival_date DESC
    """)
    latecomers = cur.fetchall()
    conn.close()
    return render_template("late/latecomers.html", latecomers=latecomers)

# -----------------------------
# Admin: Add latecomer
# -----------------------------
@late_bp.route("/add", methods=["GET", "POST"])
def add_latecomer():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        student_id = request.form["student_id"]   # ✅ now tied to users.id
        reason = request.form["reason"]
        expected_opening = request.form["expected_opening"]
        arrival_date = request.form["arrival_date"]
        punishment = request.form.get("punishment", "")
        status = request.form.get("status", "active")

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO latecomers (student_id, reason, expected_opening, arrival_date, punishment, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, reason, expected_opening, arrival_date, punishment, status))
        conn.commit()
        conn.close()
        flash("Latecomer added successfully!", "success")
        return redirect(url_for("late.list_latecomers"))

    # You can pass a list of students to the template for selection
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, username, serial, class_stream FROM users WHERE role='student'")
    students = cur.fetchall()
    conn.close()

    return render_template("late/add_latecomer.html", students=students)

# -----------------------------
# Admin: Delete latecomer
# -----------------------------
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
    flash("Latecomer deleted successfully!", "success")
    return redirect(url_for("late.list_latecomers"))

# -----------------------------
# Student: View their own latecomers
# -----------------------------
@late_bp.route("/user")
def user_latecomer():
    if session.get("role") != "student":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    student_id = session.get("user_id")  # ✅ matches users.id
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT expected_opening, arrival_date, reason, punishment
        FROM latecomers
        WHERE student_id=?
        ORDER BY arrival_date DESC
    """, (student_id,))
    latecomers = cur.fetchall()
    conn.close()

    return render_template("late/user_latecomers.html", latecomers=latecomers)

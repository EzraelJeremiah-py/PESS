from flask import Blueprint, render_template, session, flash, redirect, url_for, request
import sqlite3, os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
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

# ✅ Admin Dashboard
@admin_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()

    # Load latest attendance records
    cur.execute("""
        SELECT a.*, u.serial AS student_serial
        FROM attendance a
        JOIN users u ON a.student_id = u.id
        WHERE u.role = 'student'
        ORDER BY a.timestamp DESC LIMIT 10
    """)
    attendance_records = cur.fetchall()

    # Load latest chat messages
    cur.execute("SELECT * FROM chat_messages ORDER BY timestamp DESC LIMIT 10")
    chat_messages = cur.fetchall()

    conn.close()

    return render_template("admin_dashboard.html",
                           attendance_records=attendance_records,
                           chat_messages=chat_messages)

# ✅ List all users
@admin_bp.route("/users")
def list_users():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()

    return render_template("users.html", users=users)

# ✅ Edit user
@admin_bp.route("/users/edit/<int:id>", methods=["GET", "POST"])
def edit_user(id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        serial = request.form["serial"]
        password = request.form["password"]
        cur.execute("UPDATE users SET serial=?, password=? WHERE id=?", (serial, password, id))
        conn.commit()
        conn.close()
        flash("User updated successfully!", "success")
        return redirect(url_for("admin.list_users"))

    cur.execute("SELECT * FROM users WHERE id=?", (id,))
    user = cur.fetchone()
    conn.close()

    if not user:
        flash("User not found!", "danger")
        return redirect(url_for("admin.list_users"))

    return render_template("edit_user.html", user=user)

# ✅ Delete user
@admin_bp.route("/users/delete/<int:id>")
def delete_user(id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash("User deleted successfully!", "success")
    return redirect(url_for("admin.list_users"))

# ✅ Attendance Logs
@admin_bp.route("/attendance/logs")
def attendance_logs():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.*, u.serial AS student_serial
        FROM attendance a
        JOIN users u ON a.student_id = u.id
        WHERE u.role = 'student'
        ORDER BY a.timestamp DESC
    """)
    records = cur.fetchall()
    conn.close()

    return render_template("attendance_logs.html", attendance_records=records)

# ✅ Chat Logs
@admin_bp.route("/chat/logs")
def chat_logs():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM chat_messages ORDER BY timestamp DESC")
    messages = cur.fetchall()
    conn.close()

    return render_template("chat_logs.html", chat_messages=messages)

# ✅ Delete Book
@admin_bp.route("/delete/book/<int:book_id>")
def delete_book(book_id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    flash("Book deleted successfully!", "success")
    return redirect(url_for("library.books"))

# ✅ Delete Package
@admin_bp.route("/delete/package/<int:package_id>")
def delete_package(package_id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM packages WHERE id=?", (package_id,))
    conn.commit()
    conn.close()

    flash("Package deleted successfully!", "success")
    return redirect(url_for("library.packages"))

# ✅ Delete Link
@admin_bp.route("/delete/link/<int:link_id>")
def delete_link(link_id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM links WHERE id=?", (link_id,))
    conn.commit()
    conn.close()

    flash("Link deleted successfully!", "success")
    return redirect(url_for("library.links"))

# ✅ Delete Past Paper
@admin_bp.route("/delete/paper/<int:paper_id>")
def delete_paper(paper_id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM pastpapers WHERE id=?", (paper_id,))
    conn.commit()
    conn.close()

    flash("Past paper deleted successfully!", "success")
    return redirect(url_for("library.pastpapers"))

# ✅ Delete Notification
@admin_bp.route("/delete/notification/<int:note_id>")
def delete_notification(note_id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notifications WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

    flash("Notification deleted successfully!", "success")
    return redirect(url_for("library.notifications"))


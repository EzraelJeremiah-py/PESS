from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os, re
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

# Prevent cached pages after logout
@auth_bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# ✅ Login (serial + password only)
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        serial = request.form["serial"].strip()
        password = request.form["password"]

        # Check admin table (admins still use username)
        admin = query_db("SELECT * FROM admins WHERE username=?", (serial,), one=True)
        if admin and check_password_hash(admin["password"], password):
            session.clear()
            session["role"] = "admin"
            session["username"] = admin["username"]
            return redirect(url_for("admin.dashboard"))

        # Check users table (students/teachers/parents use serial)
        user = query_db("SELECT * FROM users WHERE serial=?", (serial,), one=True)
        if user and check_password_hash(user["password"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["serial"] = user["serial"]
            session["class_stream"] = user["class_stream"]

            if user["role"] == "teacher":
                return redirect(url_for("teacher.dashboard"))
            elif user["role"] == "student":
                return redirect(url_for("user.dashboard"))
            elif user["role"] == "parent":
                return redirect(url_for("parent.dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")

# ✅ Register Teacher
@auth_bp.route("/register/teacher", methods=["GET", "POST"])
def register_teacher():
    if request.method == "POST":
        serial = request.form["serial"].strip()
        password = request.form["password"]
        class_stream = request.form["class_stream"]

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE serial=?", (serial,))
        existing = cur.fetchone()
        if existing:
            flash("Serial already exists!", "danger")
            conn.close()
            return redirect(url_for("auth.register_teacher"))

        hashed_pw = generate_password_hash(password)
        cur.execute(
            "INSERT INTO users (serial, password, role, class_stream) VALUES (?, ?, 'teacher', ?)",
            (serial, hashed_pw, class_stream)
        )
        conn.commit()
        conn.close()
        flash("Teacher registered successfully!", "success")
        return redirect(url_for("auth.login"))

    return render_template("register_teacher.html")

# ✅ Register Student
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        serial = request.form["serial"].strip()
        password = request.form["password"]
        class_stream = request.form["class_stream"]

        # Validate serial format (e.g. S4882F1A001)
        serial_pattern = r"^S\d{4}[A-Z]\d{3}$"
        if not re.match(serial_pattern, serial):
            flash("Invalid serial format! Use e.g. S4882F1A001", "danger")
            return redirect(url_for("auth.register"))

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE serial=?", (serial,))
        existing = cur.fetchone()
        if existing:
            flash("Serial already exists!", "danger")
            conn.close()
            return redirect(url_for("auth.register"))

        hashed_pw = generate_password_hash(password)
        cur.execute(
            "INSERT INTO users (serial, password, role, class_stream) VALUES (?, ?, 'student', ?)",
            (serial, hashed_pw, class_stream)
        )
        conn.commit()
        conn.close()
        flash("Student registered successfully!", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

# ✅ Admin Reset Password
@auth_bp.route("/reset/<int:user_id>", methods=["POST"])
def reset_password(user_id):
    if session.get("role") != "admin":
        flash("Unauthorized!", "danger")
        return redirect(url_for("auth.login"))

    new_pw = request.form["new_password"]
    hashed_pw = generate_password_hash(new_pw)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE users SET password=? WHERE id=?", (hashed_pw, user_id))
    conn.commit()
    conn.close()

    flash("Password reset successfully!", "success")
    return redirect(url_for("admin.manage_users"))

# ✅ Session info
@auth_bp.route("/session")
def session_info():
    return dict(session)

# ✅ Logout
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))

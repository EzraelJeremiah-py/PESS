from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os, re

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

# ✅ Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_input = request.form["username"]
        password = request.form["password"]

        # Check admin table
        admin = query_db("SELECT * FROM admins WHERE username=? AND password=?", 
                         (user_input, password), one=True)
        if admin:
            session.clear()
            session["role"] = "admin"
            session["username"] = admin["username"]
            return redirect(url_for("admin.dashboard"))

        # ✅ Check users table
        user = query_db("SELECT * FROM users WHERE serial=? AND password=?", 
                        (user_input, password), one=True)
        if user:
            session.clear()
            session["user_id"] = user["id"]        # ✅ store primary key for attendance
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

# ✅ Register Teacher (no regex check)
@auth_bp.route("/register/teacher", methods=["GET", "POST"])
def register_teacher():
    if request.method == "POST":
        serial = request.form["serial"]
        password = request.form["password"]
        class_stream = request.form["class_stream"]

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # 🔍 Check if serial already exists
        cur.execute("SELECT id FROM users WHERE serial=?", (serial,))
        existing = cur.fetchone()

        if existing:
            flash("Serial already exists!", "danger")
            conn.close()
            return redirect(url_for("auth.register_teacher"))

        # ✅ Insert new teacher
        cur.execute(
            "INSERT INTO users (serial, password, role, class_stream) VALUES (?, ?, 'teacher', ?)",
            (serial, password, class_stream)
        )
        conn.commit()
        conn.close()
        flash("Teacher registered successfully!", "success")
        return redirect(url_for("auth.login"))

    return render_template("register_teacher.html")

# ✅ Register Student (with regex validation)
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        serial = request.form["serial"].strip()
        password = request.form["password"]
        class_stream = request.form["class_stream"]

        # ✅ Validate student serial format (e.g. S4882F1A001)
        serial_pattern = r"^S\d{4}[A-Z]\d{3}$"
        if not re.match(serial_pattern, serial):
            flash("Invalid serial format! Use e.g. S4882F1A001", "danger")
            return redirect(url_for("auth.register"))

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # 🔍 Check if serial already exists
        cur.execute("SELECT id FROM users WHERE serial=?", (serial,))
        existing = cur.fetchone()

        if existing:
            flash("Serial already exists!", "danger")
            conn.close()
            return redirect(url_for("auth.register"))

        # ✅ Insert new student
        cur.execute(
            "INSERT INTO users (serial, password, role, class_stream) VALUES (?, ?, 'student', ?)",
            (serial, password, class_stream)
        )
        conn.commit()
        conn.close()
        flash("Student registered successfully!", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

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

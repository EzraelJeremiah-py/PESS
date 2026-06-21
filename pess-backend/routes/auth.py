corrcet this . full code scripts from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

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

        # Check users table
        user = query_db("SELECT * FROM users WHERE serial=? AND password=?", 
                        (user_input, password), one=True)
        if user:
            session.clear()
            session["role"] = user["role"]
            session["serial"] = user["serial"]
            session["class_stream"] = user["class_stream"]

            if user["role"] == "teacher":
                return redirect(url_for("teacher.dashboard"))
            elif user["role"] == "student":
                return redirect(url_for("user.dashboard"))
            elif user["role"] == "parent":
                return redirect(url_for("parent.dashboard"))  # ✅ fixed

        flash("Invalid credentials", "danger")

    return render_template("login.html")

# ✅ Register Teacher
@auth_bp.route("/register/teacher", methods=["GET", "POST"])
def register_teacher():
    if request.method == "POST":
        serial = request.form["serial"]
        password = request.form["password"]
        class_stream = request.form["class_stream"]

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (serial, password, role, class_stream) VALUES (?, ?, 'teacher', ?)",
                (serial, password, class_stream)
            )
            conn.commit()
            conn.close()
            flash("Teacher registered successfully!", "success")
            return redirect(url_for("auth.login"))
        except sqlite3.IntegrityError:
            flash("Serial already exists!", "danger")

    return render_template("register_teacher.html")

# ✅ Register Student
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        serial = request.form["serial"]
        password = request.form["password"]
        class_stream = request.form["class_stream"]

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (serial, password, role, class_stream) VALUES (?, ?, 'student', ?)",
                (serial, password, class_stream)
            )
            conn.commit()
            conn.close()
            flash("Student registered successfully!", "success")
            return redirect(url_for("auth.login"))
        except sqlite3.IntegrityError:
            flash("Serial already exists!", "danger")

    return render_template("register.html")

# ✅ Session info
@auth_bp.route("/session")
def session_info():
    return dict(session)

# ✅ Logout
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")  # ✅ fixed
    return redirect(url_for("auth.login"))

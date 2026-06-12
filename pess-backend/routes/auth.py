from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3, os

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
DB_PATH = "pess.db"

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
        username = request.form["username"]
        password = request.form["password"]

        # Check admin table
        admin = query_db("SELECT * FROM admins WHERE username=? AND password=?", 
                         (username, password), one=True)
        if admin:
            session["role"] = "admin"
            session["username"] = admin["username"]
            return redirect(url_for("admin.dashboard"))

        # Check users table (teachers, students, parents)
        user = query_db("SELECT * FROM users WHERE serial=? AND password=?", 
                        (username, password), one=True)
        if user:
            session["role"] = user["role"]
            session["username"] = user["username"]

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
        username = request.form["username"]
        serial = request.form["serial"]
        password = request.form["password"]

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, serial, password, role) VALUES (?, ?, ?, 'teacher')",
                (username, serial, password)
            )
            conn.commit()
            conn.close()
            flash("Teacher registered successfully!", "success")
            return redirect(url_for("auth.login"))
        except sqlite3.IntegrityError:
            flash("Username or serial already exists!", "danger")

    return render_template("register_teacher.html")


# ✅ Register Student/Parent (default role = student)
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        serial = request.form["serial"]
        password = request.form["password"]

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, serial, password, role) VALUES (?, ?, ?, 'student')",
                (username, serial, password)
            )
            conn.commit()
            conn.close()
            flash("User registered successfully!", "success")
            return redirect(url_for("auth.login"))
        except sqlite3.IntegrityError:
            flash("Username or serial already exists!", "danger")

    return render_template("register.html")


# ✅ Session info
@auth_bp.route("/session")
def session_info():
    role = session.get("role")
    return {"role": role} if role else {"role": None}


# ✅ Logout
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))

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

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check admin
        admin = query_db("SELECT * FROM admins WHERE username=? AND password=?", 
                         (username, password), one=True)
        if admin:
            session["role"] = "admin"
            session["username"] = admin["username"]   # ✅ store admin username
            return redirect(url_for("admin.dashboard"))

        # Check user
        user = query_db("SELECT * FROM users WHERE serial=? AND password=?", 
                        (username, password), one=True)
        if user:
            session["role"] = "user"
            session["serial"] = user["serial"]       # ✅ store user serial
            return redirect(url_for("user.dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")

@auth_bp.route("/session")
def session_info():
    role = session.get("role")
    if role:
        return {"role": role}
    return {"role": None}

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        serial = request.form["serial"]
        password = request.form["password"]

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("INSERT INTO users (serial, password) VALUES (?, ?)", (serial, password))
            conn.commit()
            conn.close()
            flash("User registered successfully!", "success")
            return redirect(url_for("auth.login"))
        except sqlite3.IntegrityError:
            flash("Serial already exists!", "danger")

    return render_template("register.html")

@auth_bp.route("/users")
def list_users():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    users = query_db("SELECT * FROM users")
    return render_template("users.html", users=users)

@auth_bp.route("/delete/<int:user_id>")
def delete_user(user_id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    flash("User deleted successfully!", "info")
    return redirect(url_for("auth.list_users"))

@auth_bp.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        serial = request.form["serial"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("UPDATE users SET serial=?, password=? WHERE id=?", (serial, password, user_id))
        conn.commit()
        conn.close()
        flash("User updated successfully!", "success")
        return redirect(url_for("auth.list_users"))

    user = query_db("SELECT * FROM users WHERE id=?", (user_id,), one=True)
    return render_template("edit_user.html", user=user)

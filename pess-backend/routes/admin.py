from flask import Blueprint, render_template, session, flash, redirect, url_for, request
import sqlite3, os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")

@admin_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))
    return render_template("admin_dashboard.html")

# ✅ List all users
@admin_bp.route("/users")
def list_users():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
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

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
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

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash("User deleted successfully!", "success")
    return redirect(url_for("admin.list_users"))

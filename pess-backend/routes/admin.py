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


# ✅ Delete Book
@admin_bp.route("/delete/book/<int:book_id>")
def delete_book(book_id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
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

    conn = sqlite3.connect(DB_PATH)
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

    conn = sqlite3.connect(DB_PATH)
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

    conn = sqlite3.connect(DB_PATH)
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

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM notifications WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

    flash("Notification deleted successfully!", "success")
    return redirect(url_for("library.notifications"))



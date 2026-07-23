# routes/library.py
import os, sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, session
from werkzeug.utils import secure_filename
from flask import send_from_directory

library_bp = Blueprint("library", __name__, url_prefix="/library")

DB_PATH = "pess.db"   # adjust to your DB file

# Prevent cached pages after logout
@admin_bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads/library")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Serve file for viewing in browser
@library_bp.route("/view/<filename>")
def serve_file(filename):
    # This will try to display the file inline if the browser supports it (PDF, images, etc.)
    return send_from_directory(UPLOAD_FOLDER, filename)
    
def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# 📚 Books
@library_bp.route("/books")
def books():
    books = query_db("SELECT * FROM books")
    return render_template("library/books.html", books=books)

@library_bp.route("/books/upload", methods=["POST"])
def upload_book():
    file = request.files["file"]
    category = request.form.get("category")
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        query_db("INSERT INTO books (filename, category, uploaded_by) VALUES (?, ?, ?)",
                 (filename, category, session.get("username")))
        flash("Book uploaded successfully!", "success")
    return redirect(url_for("library.books"))

# 🏠 Packages
@library_bp.route("/packages")
def packages():
    packages = query_db("SELECT * FROM packages")
    return render_template("library/packages.html", packages=packages)

@library_bp.route("/packages/upload", methods=["POST"])
def upload_package():
    file = request.files["file"]
    category = request.form.get("category")
    stream = request.form.get("stream")
    class_name = request.form.get("class_name")
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        query_db("INSERT INTO packages (filename, category, stream, class_name, uploaded_by) VALUES (?, ?, ?, ?, ?)",
                 (filename, category, stream, class_name, session.get("username")))
        flash("Package uploaded successfully!", "success")
    return redirect(url_for("library.packages"))

# 🌐 Links
@library_bp.route("/links")
def links():
    links = query_db("SELECT * FROM links")
    return render_template("library/links.html", links=links)

@library_bp.route("/links/add", methods=["POST"])
def add_link():
    title = request.form.get("title")
    url = request.form.get("url")
    description = request.form.get("description")
    query_db("INSERT INTO links (title, url, description) VALUES (?, ?, ?)",
             (title, url, description))
    flash("Link added successfully!", "success")
    return redirect(url_for("library.links"))

# 📄 Past Papers
@library_bp.route("/pastpapers")
def pastpapers():
    papers = query_db("SELECT * FROM pastpapers")
    return render_template("library/pastpapers.html", papers=papers)

@library_bp.route("/pastpapers/upload", methods=["POST"])
def upload_paper():
    file = request.files["file"]
    category = request.form.get("category")
    class_name = request.form.get("class_name")
    year = request.form.get("year")
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        query_db("INSERT INTO pastpapers (filename, category, class_name, year, uploaded_by) VALUES (?, ?, ?, ?, ?)",
                 (filename, category, class_name, year, session.get("username")))
        flash("Past paper uploaded successfully!", "success")
    return redirect(url_for("library.pastpapers"))

# 📊 Downloads (Analytics)
@library_bp.route("/download/<file_type>/<int:file_id>/<filename>")
def download_file(file_type, file_id, filename):
    query_db("INSERT INTO downloads (file_id, file_type, user) VALUES (?, ?, ?)",
             (file_id, file_type, session.get("username")))
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# 🔔 Notifications
@library_bp.route("/notifications")
def notifications():
    notes = query_db("SELECT * FROM notifications")
    return render_template("library/notifications.html", notes=notes)

@library_bp.route("/notifications/add", methods=["POST"])
def add_notification():
    message = request.form.get("message")
    target_role = request.form.get("target_role")
    query_db("INSERT INTO notifications (message, target_role) VALUES (?, ?)",
             (message, target_role))
    flash("Notification added!", "success")
    return redirect(url_for("library.notifications"))

from flask import Blueprint, render_template, request, session, flash, redirect, url_for, send_from_directory
import sqlite3, os
from werkzeug.utils import secure_filename

results_bp = Blueprint("results", __name__, url_prefix="/results")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads", "results")

# Prevent cached pages after logout
@results_bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------ Upload Results File (Admin) ------------------
@results_bp.route("/upload", methods=["GET", "POST"])
def upload_result_file():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        class_name = request.form["class"]
        stream = request.form["stream"]
        exam_date = request.form["exam_date"]
        file = request.files["file"]

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO result_uploads (class, stream, filename, filepath, extension, uploaded_by, exam_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (class_name, stream, filename, filepath,
                  os.path.splitext(filename)[1],
                  session.get("username", "admin"),
                  exam_date))
            conn.commit()
            conn.close()

            flash("Result file uploaded successfully!", "success")
            return redirect(url_for("results.upload_result_file"))

    return render_template("results/upload_results.html")

# ------------------ Manage Results Files (Admin View) ------------------
@results_bp.route("/view")
def view_result_files():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM result_uploads ORDER BY uploaded_at DESC")
    result_files = cur.fetchall()
    conn.close()

    return render_template("results/manage_results.html", result_files=result_files)

# ------------------ Delete Result File (Admin) ------------------
@results_bp.route("/delete/<int:id>")
def delete_result_file(id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM result_uploads WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash("Result file deleted successfully!", "success")
    return redirect(url_for("results.view_result_files"))

# ------------------ Serve Files (View/Download) ------------------
@results_bp.route("/files/<filename>")
def serve_result_file(filename):
    download = request.args.get("download")
    return send_from_directory(
        UPLOAD_FOLDER,
        filename,
        as_attachment=True if download else False
    )

# ------------------ User View (Students) ------------------
@results_bp.route("/user")
def user_result_files():
    if session.get("role") != "student":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM result_uploads ORDER BY uploaded_at DESC")
    result_files = cur.fetchall()
    conn.close()

    return render_template("results/user_results.html", result_files=result_files)

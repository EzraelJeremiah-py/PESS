from flask import Blueprint, render_template, request, session, flash, redirect, url_for, send_from_directory
import sqlite3, os
from werkzeug.utils import secure_filename

fees_bp = Blueprint("fees", __name__, url_prefix="/fees")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads", "fees")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------ Upload Fee File (Admin) ------------------
@fees_bp.route("/upload", methods=["GET", "POST"])
def upload_fee_file():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        class_name = request.form["class"]
        stream = request.form["stream"]
        fee_date = request.form["fee_date"]
        file = request.files["file"]

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO fee_uploads (class, stream, filename, filepath, extension, uploaded_by, fee_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (class_name, stream, filename, filepath,
                  os.path.splitext(filename)[1],
                  session.get("username", "admin"),
                  fee_date))
            conn.commit()
            conn.close()

            flash("Fee file uploaded successfully!", "success")
            return redirect(url_for("fees.upload_fee_file"))

    return render_template("fees/upload_fee.html")

# ------------------ Manage Fee Files (Admin View) ------------------
@fees_bp.route("/view")
def view_fee_files():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM fee_uploads ORDER BY uploaded_at DESC")
    fee_files = cur.fetchall()
    conn.close()

    return render_template("fees/manage_fees.html", fee_files=fee_files)

# ------------------ Delete Fee File (Admin) ------------------
@fees_bp.route("/delete/<int:id>")
def delete_fee_file(id):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM fee_uploads WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash("Fee file deleted successfully!", "success")
    return redirect(url_for("fees.view_fee_files"))

# ------------------ Serve Files (View/Download) ------------------
@fees_bp.route("/files/<filename>")
def serve_fee_file(filename):
    download = request.args.get("download")
    return send_from_directory(
        UPLOAD_FOLDER,
        filename,
        as_attachment=True if download else False
    )

# ------------------ User View (Students) ------------------
@fees_bp.route("/user")
def user_fee_files():
    if session.get("role") != "user":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM fee_uploads ORDER BY uploaded_at DESC")
    fee_files = cur.fetchall()
    conn.close()

    return render_template("fees/user_fees.html", fee_files=fee_files)

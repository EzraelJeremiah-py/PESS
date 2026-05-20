from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import sqlite3, os
from werkzeug.utils import secure_filename

fees_bp = Blueprint("fees", __name__, url_prefix="/fees")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pess.db")
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads", "fees")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
            """, (class_name, stream, filename, filepath, os.path.splitext(filename)[1], session.get("username", "admin"), fee_date))
            conn.commit()
            conn.close()

            flash("Fee file uploaded successfully!", "success")
            return redirect(url_for("fees.upload_fee_file"))

    return render_template("fees/upload_fee.html")

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
    return redirect(url_for("fees.upload_fee_file"))

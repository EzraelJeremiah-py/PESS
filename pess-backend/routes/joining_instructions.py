import os, sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, send_from_directory
from werkzeug.utils import secure_filename

joining_bp = Blueprint("joining", __name__, url_prefix="/joining")

ALLOWED_EXTENSIONS = {
    "pdf","doc","docx","xls","xlsx","ppt","pptx","txt","rtf","odt",
    "csv","jpg","jpeg","png","gif","zip","tar","7z","mp4","mp3"
}

@joining_bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    db_path = os.path.join(current_app.root_path, "pess.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Admin: Manage files
@joining_bp.route("/admin", methods=["GET","POST"])
def manage_files():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    upload_folder = current_app.config["JOINING_FOLDER"]

    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("No file selected!", "danger")
        elif allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO joining_instructions (filename, original_name, uploader, file_type, size)
                VALUES (?, ?, ?, ?, ?)
            """, (filename, file.filename, session.get("username"), filename.split(".")[-1], os.path.getsize(filepath)))
            conn.commit()
            conn.close()

            flash("File uploaded successfully!", "success")
        else:
            flash("File type not allowed!", "danger")
        return redirect(url_for("joining.manage_files"))

    conn = get_db()
    files = conn.execute("SELECT * FROM joining_instructions ORDER BY uploaded_at DESC").fetchall()
    conn.close()
    return render_template("school_joining_instructs/manage_school_joining_instruct.html", files=files)

# Admin: Upload page
@joining_bp.route("/admin/upload", methods=["GET","POST"])
def upload_file():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        file = request.files.get("file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config["JOINING_FOLDER"], filename)
            file.save(filepath)
            conn = get_db()
            conn.execute("""
                INSERT INTO joining_instructions (filename, original_name, uploader, file_type, size)
                VALUES (?, ?, ?, ?, ?)
            """, (filename, file.filename, session.get("username"), filename.split(".")[-1], os.path.getsize(filepath)))
            conn.commit()
            conn.close()
            flash("File uploaded successfully!", "success")
            return redirect(url_for("joining.manage_files"))
    return render_template("school_joining_instructs/upload.html")

# Admin: Delete
@joining_bp.route("/admin/delete/<int:file_id>")
def delete_file(file_id):
    conn = get_db()
    file = conn.execute("SELECT * FROM joining_instructions WHERE id=?", (file_id,)).fetchone()
    if file:
        upload_folder = current_app.config["JOINING_FOLDER"]
        filepath = os.path.join(upload_folder, file["filename"])
        if os.path.exists(filepath):
            os.remove(filepath)
        conn.execute("DELETE FROM joining_instructions WHERE id=?", (file_id,))
        conn.commit()
    conn.close()
    flash("File deleted!", "success")
    return redirect(url_for("joining.manage_files"))

# Admin: Rename
@joining_bp.route("/admin/rename/<int:file_id>", methods=["POST"])
def rename_file(file_id):
    new_name = request.form.get("new_name")
    conn = get_db()
    file = conn.execute("SELECT * FROM joining_instructions WHERE id=?", (file_id,)).fetchone()
    if file and new_name:
        upload_folder = current_app.config["JOINING_FOLDER"]
        old_path = os.path.join(upload_folder, file["filename"])
        new_path = os.path.join(upload_folder, new_name)
        os.rename(old_path, new_path)
        conn.execute("UPDATE joining_instructions SET filename=? WHERE id=?", (new_name, file_id))
        conn.commit()
        flash("File renamed successfully!", "success")
    conn.close()
    return redirect(url_for("joining.manage_files"))

# User: View + Download
@joining_bp.route("/user")
def user_view():
    conn = get_db()
    files = conn.execute("SELECT * FROM joining_instructions ORDER BY uploaded_at DESC").fetchall()
    conn.close()
    return render_template("school_joining_instructs/official_school_joining_instruct.html", files=files)

@joining_bp.route("/download/<int:file_id>")
def download_file(file_id):
    conn = get_db()
    file = conn.execute("SELECT * FROM joining_instructions WHERE id=?", (file_id,)).fetchone()
    conn.close()
    upload_folder = current_app.config["JOINING_FOLDER"]
    return send_from_directory(upload_folder, file["filename"], as_attachment=True)

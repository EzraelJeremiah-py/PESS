import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, send_from_directory

joining_bp = Blueprint("joining", __name__, url_prefix="/joining")

# ✅ Allowed extensions (15+ common ones)
ALLOWED_EXTENSIONS = {
    "pdf","doc","docx","xls","xlsx","ppt","pptx","txt","rtf","odt",
    "csv","jpg","jpeg","png","gif","zip","tar","7z","mp4","mp3"
}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Admin: Manage files
@joining_bp.route("/admin", methods=["GET","POST"])
def manage_files():
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    upload_folder = current_app.config["JOINING_FOLDER"]

    # Upload
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("No file selected!", "danger")
        elif allowed_file(file.filename):
            filepath = os.path.join(upload_folder, file.filename)
            file.save(filepath)
            flash("File uploaded successfully!", "success")
        else:
            flash("File type not allowed!", "danger")
        return redirect(url_for("joining.manage_files"))

    files = os.listdir(upload_folder) if os.path.exists(upload_folder) else []
    return render_template("admin/joining.html", files=files)

# Admin: Delete file
@joining_bp.route("/admin/delete/<filename>")
def delete_file(filename):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    upload_folder = current_app.config["JOINING_FOLDER"]
    filepath = os.path.join(upload_folder, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash("File deleted!", "success")
    return redirect(url_for("joining.manage_files"))

# Admin: Rename file
@joining_bp.route("/admin/rename/<filename>", methods=["POST"])
def rename_file(filename):
    if session.get("role") != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.login"))

    new_name = request.form.get("new_name")
    upload_folder = current_app.config["JOINING_FOLDER"]
    old_path = os.path.join(upload_folder, filename)
    new_path = os.path.join(upload_folder, new_name)

    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        flash("File renamed successfully!", "success")
    else:
        flash("File not found!", "danger")
    return redirect(url_for("joining.manage_files"))

# User: View + Download
@joining_bp.route("/user")
def user_view():
    upload_folder = current_app.config["JOINING_FOLDER"]
    files = os.listdir(upload_folder) if os.path.exists(upload_folder) else []
    return render_template("user/joining.html", files=files)

@joining_bp.route("/download/<filename>")
def download_file(filename):
    upload_folder = current_app.config["JOINING_FOLDER"]
    return send_from_directory(upload_folder, filename, as_attachment=True)

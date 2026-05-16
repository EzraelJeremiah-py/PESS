import os
from flask import Blueprint, render_template, current_app, send_from_directory
from models.guidelines import GuidelineFile

guidelines_bp = Blueprint("guidelines", __name__, url_prefix="/guidelines")

@guidelines_bp.route("/")
def list_files():
    files = GuidelineFile.query.all()
    return render_template("guidelines/list.html",
                           title="Guidelines",
                           files=files)

@guidelines_bp.route("/view/<int:file_id>")
def view_file(file_id):
    record = GuidelineFile.query.get_or_404(file_id)
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], record.filename)

@guidelines_bp.route("/download/<int:file_id>")
def download_file(file_id):
    record = GuidelineFile.query.get_or_404(file_id)
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], record.filename, as_attachment=True)

@guidelines_bp.route("/public")
def public_list():
    files = GuidelineFile.query.all()
    return render_template("guidelines/list.html",
                           title="Guidelines",
                           files=files)



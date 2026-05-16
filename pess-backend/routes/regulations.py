from flask import Blueprint, render_template, current_app, send_from_directory
from models.regulations import RegulationFile

regulations_bp = Blueprint("regulations", __name__, url_prefix="/regulations")

@regulations_bp.route("/")
def list_regulations():
    files = RegulationFile.query.all()
    return render_template("regulations/list.html", files=files)

@regulations_bp.route("/view/<int:file_id>")
def view_regulation(file_id):
    record = RegulationFile.query.get_or_404(file_id)
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], record.filename)

@regulations_bp.route("/download/<int:file_id>")
def download_regulation(file_id):
    record = RegulationFile.query.get_or_404(file_id)
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], record.filename, as_attachment=True)

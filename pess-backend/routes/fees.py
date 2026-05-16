from flask import Blueprint, render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
import os
from models.fee import db, FeeStructure, FeeStatus

# Blueprint
fees_bp = Blueprint("fees", __name__, url_prefix="/fees")

# Upload folder
UPLOAD_FOLDER = "uploads/fees"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Admin management
@fees_bp.route("/admin", methods=["GET", "POST"])
def manage_fees():
    if request.method == "POST":
        year = request.form["year_of_study"]
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            db.session.add(FeeStructure(year_of_study=year, filename=filename))
            db.session.commit()
            flash("Fee structure uploaded successfully!", "success")
    structures = FeeStructure.query.all()
    statuses = FeeStatus.query.all()
    return render_template("admin/fees.html", structures=structures, statuses=statuses)

# Public view
@fees_bp.route("/")
def list_fees():
    year_filter = request.args.get("year")
    student_filter = request.args.get("student", "").lower()

    structures = FeeStructure.query.all()
    statuses = FeeStatus.query.all()

    # Apply filters
    if year_filter:
        structures = [s for s in structures if s.year_of_study == year_filter]
        statuses = [st for st in statuses if st.year_of_study == year_filter]
    if student_filter:
        statuses = [st for st in statuses if student_filter in st.student_name.lower()]

    return render_template("fees.html", structures=structures, statuses=statuses)

# File view/download
@fees_bp.route("/view/<filename>")
def view_fee(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

@fees_bp.route("/download/<filename>")
def download_fee(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

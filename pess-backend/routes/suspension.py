import os
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from models import db
from models.suspension import Suspension
from flask_login import login_required, current_user
from datetime import datetime
from fpdf import FPDF

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

suspension_bp = Blueprint("suspension", __name__)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@suspension_bp.route("/suspensions", methods=["GET", "POST"])
@login_required
def manage_suspensions():
    if request.method == "POST":
        student_name = request.form["student_name"]
        reason = request.form["reason"]
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d")

        photo_url = None
        if "photo" in request.files:
            file = request.files["photo"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                photo_url = filepath

        suspension = Suspension(
            student_name=student_name,
            reason=reason,
            start_date=start_date,
            end_date=end_date,
            photo_url=photo_url,
            issued_by=current_user.id
        )
        db.session.add(suspension)
        db.session.commit()
        flash("Suspension recorded successfully!", "success")
        return redirect(url_for("suspension.manage_suspensions"))

    query = request.args.get("q", "")
    status_filter = request.args.get("status", "")
    page = request.args.get("page", 1, type=int)
    per_page = 5

    suspensions_query = Suspension.query
    if query:
        suspensions_query = suspensions_query.filter(
            (Suspension.student_name.ilike(f"%{query}%")) |
            (Suspension.reason.ilike(f"%{query}%"))
        )
    if status_filter:
        suspensions_query = suspensions_query.filter(Suspension.status == status_filter)

    suspensions = suspensions_query.paginate(page=page, per_page=per_page)

    for s in suspensions.items:
        if s.auto_status == "completed" and s.status != "completed":
            s.status = "completed"
            db.session.commit()

    return render_template("admin/dashboard.html", suspensions=suspensions, query=query, status_filter=status_filter)

# Export to Excel
@suspension_bp.route("/suspensions/export/excel")
@login_required
def export_excel():
    suspensions = Suspension.query.all()
    data = [{
        "Student": s.student_name,
        "Reason": s.reason,
        "Start": s.start_date,
        "End": s.end_date,
        "Status": s.auto_status
    } for s in suspensions]
    df = pd.DataFrame(data)
    filepath = "static/exports/suspensions.xlsx"
    df.to_excel(filepath, index=False)
    return send_file(filepath, as_attachment=True)

# Export to PDF
@suspension_bp.route("/suspensions/export/pdf")
@login_required
def export_pdf():
    suspensions = Suspension.query.all()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Suspensions Report", ln=True, align="C")
    pdf.ln(10)
    for s in suspensions:
        pdf.cell(200, 10, f"{s.student_name} - {s.reason} ({s.start_date} to {s.end_date}) - {s.auto_status}", ln=True)
    filepath = "static/exports/suspensions.pdf"
    pdf.output(filepath)
    return send_file(filepath, as_attachment=True)

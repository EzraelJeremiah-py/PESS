from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.meeting import Meeting
from datetime import datetime

meeting_bp = Blueprint("meeting_bp", __name__, url_prefix="/admin/meetings")

# Manage meetings page
@meeting_bp.route("/", methods=["GET"])
def manage_meetings():
    meetings = Meeting.query.all()
    return render_template("admin/manage_meetings.html", meetings=meetings)

# Add meeting
@meeting_bp.route("/add", methods=["POST"])
def add_meeting():
    title = request.form["title"]
    platform = request.form["platform"]
    url = request.form["url"]
    scheduled_at = datetime.strptime(request.form["scheduled_at"], "%Y-%m-%dT%H:%M")

    new_meeting = Meeting(
        title=title,
        platform=platform,
        url=url,
        scheduled_at=scheduled_at
    )
    db.session.add(new_meeting)
    db.session.commit()
    flash("Meeting added successfully!", "success")
    return redirect(url_for("meeting_bp.manage_meetings"))

# Delete meeting
@meeting_bp.route("/delete/<int:id>", methods=["POST"])
def delete_meeting(id):
    meeting = Meeting.query.get_or_404(id)
    db.session.delete(meeting)
    db.session.commit()
    flash("Meeting deleted successfully!", "success")
    return redirect(url_for("meeting_bp.manage_meetings"))

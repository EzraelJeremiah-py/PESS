from flask import Blueprint, render_template
from models.meeting import Meeting

# Define the blueprint object
public_meeting_bp = Blueprint("public_meeting_bp", __name__)

# Route for public meeting zone
@public_meeting_bp.route("/meetingzone")
def meetingzone():
    meetings = Meeting.query.all()
    return render_template("meetingzone.html", meetings=meetings)

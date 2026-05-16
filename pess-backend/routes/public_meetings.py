from flask import render_template
from models.meeting import Meeting

@app.route("/meetingzone")
def meetingzone():
    meetings = Meeting.query.all()
    return render_template("meetingzone.html", meetings=meetings)

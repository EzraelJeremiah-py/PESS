from models import db
from datetime import date

class Attendance(db.Model):
    __tablename__ = "attendancies"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    class_cohort_id = db.Column(db.Integer, db.ForeignKey("class_cohorts.id"), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    status = db.Column(db.String(15), nullable=False)  # Present/Absent/Sick/Permission

    # Relationships (optional, but useful)
    student = db.relationship("Student", backref="attendance_records", lazy=True)
    class_cohort = db.relationship("ClassCohort", backref="attendance_records", lazy=True)

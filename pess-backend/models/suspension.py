from . import db
from datetime import date

class Suspension(db.Model):
    __tablename__ = "suspensions"

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    photo_url = db.Column(db.String(255), nullable=True)
    issued_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(50), default="active")

    @property
    def auto_status(self):
        if date.today() > self.end_date:
            return "completed"
        return self.status

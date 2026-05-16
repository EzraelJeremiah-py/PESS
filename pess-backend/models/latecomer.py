from models import db
from datetime import datetime

class LateComer(db.Model):
    __tablename__ = "late_comers"
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(20), nullable=False)
    stream = db.Column(db.String(20), nullable=True)
    reason = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default="Pending")  # Pending / Excused / Penalized
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

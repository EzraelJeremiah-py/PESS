from models import db
from datetime import datetime

class FeeStructure(db.Model):
    __tablename__ = "fee_structures"
    id = db.Column(db.Integer, primary_key=True)
    year_of_study = db.Column(db.String(20), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class FeeStatus(db.Model):
    __tablename__ = "fee_statuses"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    year_of_study = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Paid / Not Paid / Incomplete
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

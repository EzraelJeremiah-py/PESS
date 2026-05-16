# models/guidelines.py
from . import db

class GuidelineFile(db.Model):
    __tablename__ = "guideline_files"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    filepath = db.Column(db.String(300), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

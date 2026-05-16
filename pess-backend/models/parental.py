from . import db

class ParentalSuggestion(db.Model):
    __tablename__ = "parental_suggestions"
    id = db.Column(db.Integer, primary_key=True)
    parent_name = db.Column(db.String(100), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    student_class = db.Column(db.String(50), nullable=False)
    student_stream = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    gmail = db.Column(db.String(120), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

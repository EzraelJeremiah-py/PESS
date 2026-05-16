from models import db

class ClassCohort(db.Model):
    __tablename__ = "class_cohorts"
    id = db.Column(db.Integer, primary_key=True)
    form = db.Column(db.Integer, nullable=False)   # e.g. 1, 2, 3, 4
    stream = db.Column(db.String(1), nullable=False)  # e.g. A, B, C
    year = db.Column(db.Integer, nullable=False)   # e.g. 2026

    # Relationships
    students = db.relationship("Student", backref="class_cohort", lazy=True)

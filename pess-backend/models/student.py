from models import db

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    cohort_id = db.Column(db.Integer, db.ForeignKey("class_cohorts.id"))

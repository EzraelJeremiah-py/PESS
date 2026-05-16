from app import db
from models.student import Student   # <-- add this import

class Parent(db.Model):
    __tablename__ = "parents"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))

    # direct relationship to Student
    students = db.relationship("Student", backref="parent", lazy=True)

    def __repr__(self):
        return f"<Parent {self.name}>"

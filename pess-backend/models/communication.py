from app import db

class Communication(db.Model):
    __tablename__ = "communications"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    parent_id = db.Column(db.Integer, db.ForeignKey("parents.id"))

    def __repr__(self):
        return f"<Communication {self.message[:30]}...>"

from flask import Blueprint, render_template
from models.student import Student   # ✅ import from models/student.py

student_bp = Blueprint("student", __name__)

@student_bp.route("/students")
def students():
    all_students = Student.query.all()
    return render_template("students.html", students=all_students)

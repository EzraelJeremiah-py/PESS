from flask import Blueprint, render_template
from models.library import Library   # ✅ correct import

library_bp = Blueprint("library", __name__)

@library_bp.route("/library")
def library():
    books = Library.query.all()
    return render_template("library.html", books=books)

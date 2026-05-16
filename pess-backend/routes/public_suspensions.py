from flask import Blueprint, render_template
from models.suspension import Suspension

public_suspensions_bp = Blueprint("public_suspensions", __name__, url_prefix="/suspensions")

@public_suspensions_bp.route("/")
def view_suspensions():
    suspensions = Suspension.query.all()
    return render_template("public/suspensions/list.html", suspensions=suspensions)

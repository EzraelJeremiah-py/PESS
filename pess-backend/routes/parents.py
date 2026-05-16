from flask import Blueprint, jsonify
from models import Parent

parents_bp = Blueprint("parents", __name__)

@parents_bp.route("/parents", methods=["GET"])
def get_parents():
    parents = Parent.query.all()
    return jsonify([
        {"id": p.id, "name": p.name, "phone": p.phone}
        for p in parents
    ])

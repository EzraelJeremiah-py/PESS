from flask import Blueprint, jsonify
from models import Communication

alerts_bp = Blueprint("alerts", __name__)

@alerts_bp.route("/alerts", methods=["GET"])
def get_alerts():
    alerts = Communication.query.all()
    return jsonify([{"id": a.id, "message": a.message, "date": a.date} for a in alerts])

from flask import Blueprint, jsonify
from models import Event

events_bp = Blueprint("events", __name__)

@events_bp.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    return jsonify([{"id": e.id, "title": e.title, "date": e.date} for e in events])

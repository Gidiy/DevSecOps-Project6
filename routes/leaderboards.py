from flask import Blueprint, jsonify, request
from utils.utils import L
from flask_jwt_extended import get_jwt_identity

leaderboards_bp = Blueprint('leaderboards_bp', __name__)

# ---------- HELPERS ----------
def _uid_or_anon() -> str:
    try:
        return get_jwt_identity() or "anonymous"
    except Exception:
        return "anonymous"


# ---------- ROUTES ----------
@leaderboards_bp.get("/global")
# GET http://127.0.0.1:5001/leaderboards/global
# Body: None
# Example cURL:
# curl -X GET http://127.0.0.1:5001/leaderboards/global
def leaderboard_global():
    data = [
        {"user": "alice", "points": 1200},
        {"user": "bob", "points": 1100},
        {"user": "charlie", "points": 900},
    ]
    L.log("Fetched global leaderboard")
    return jsonify({"leaderboard": data}), 200


@leaderboards_bp.get("/team")
# GET http://127.0.0.1:5001/leaderboards/team
# Headers: (optional) Authorization: Bearer <jwt_token>
# Body: None
# Example cURL:
# curl -X GET http://127.0.0.1:5001/leaderboards/team -H "Authorization: Bearer <jwt_token>"
def leaderboard_team():
    uid = _uid_or_anon()
    data = [
        {"user": uid, "points": 300},
        {"user": "teammate1", "points": 280},
        {"user": "teammate2", "points": 260},
    ]
    L.log(f"Fetched team leaderboard for {uid}")
    return jsonify({"leaderboard": data}), 200


@leaderboards_bp.get("/monthly")
# GET http://127.0.0.1:5001/leaderboards/monthly
# Body: None
# Example cURL:
# curl -X GET http://127.0.0.1:5001/leaderboards/monthly
def leaderboard_monthly():
    data = [
        {"month": "September", "top_user": "alice", "points": 500},
        {"month": "August", "top_user": "bob", "points": 450},
    ]
    L.log("Fetched monthly leaderboard")
    return jsonify({"leaderboard": data}), 200


@leaderboards_bp.get("/hall-of-fame")
# GET http://127.0.0.1:5001/leaderboards/hall-of-fame
# Body: None
# Example cURL:
# curl -X GET http://127.0.0.1:5001/leaderboards/hall-of-fame
def leaderboard_hall_of_fame():
    data = [
        {"user": "alice", "achievements": ["Top scorer Q1", "Best code quality"]},
        {"user": "bob", "achievements": ["Fitness champion", "Learning star"]},
    ]
    L.log("Fetched hall of fame")
    return jsonify({"hall_of_fame": data}), 200


@leaderboards_bp.post("/predictions")
# POST http://127.0.0.1:5001/leaderboards/predictions
# Headers: Content-Type: application/json
# Body:
# {
#   "prediction": "Alice will win the Code Quality Challenge"
# }
# Example cURL:
# curl -X POST http://127.0.0.1:5001/leaderboards/predictions \
#   -H "Content-Type: application/json" \
#   -d '{"prediction": "Alice will win the Code Quality Challenge"}'
def leaderboard_predictions():
    body = request.get_json(force=True)
    prediction = body.get("prediction", "No prediction provided")
    uid = _uid_or_anon()
    L.log(f"Prediction submitted by {uid}: {prediction}")
    return jsonify({"message": "Prediction received", "prediction": prediction}), 200

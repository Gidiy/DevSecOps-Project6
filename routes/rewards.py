from flask import Blueprint, jsonify, request
from utils.utils import L
from flask_jwt_extended import get_jwt_identity

rewards_bp = Blueprint('rewards_bp', __name__)

# ---------- HELPERS ----------
def _uid_or_anon() -> str:
    try:
        return get_jwt_identity() or "anonymous"
    except Exception:
        return "anonymous"


# ---------- ROUTES ----------
@rewards_bp.post("/teams/create")  # יצירת צוותי תחרות
# POST http://127.0.0.1:5001/rewards/teams/create
# Body:
# {
#   "team_name": "Winners",
#   "members": ["alice", "bob"]
# }
def rewards_teams_create():
    body = request.get_json(force=True)
    team_name = body.get("team_name")
    members = body.get("members", [])
    uid = _uid_or_anon()

    L.log(f"Team created by {uid}: {team_name} with {len(members)} members")
    return jsonify({
        "message": "Team created successfully",
        "team": {"name": team_name, "members": members}
    }), 201


@rewards_bp.get("/friends")  # צפייה בחברים/עמיתים מהמשרד
# GET http://127.0.0.1:5001/rewards/friends
def rewards_friends():
    data = ["alice", "bob", "charlie"]
    L.log("Fetched friends list")
    return jsonify({"friends": data}), 200


@rewards_bp.post("/challenges/send")  # שליחת אתגרים אישיים
# POST http://127.0.0.1:5001/rewards/challenges/send
# Body:
# {
#   "to": "alice",
#   "challenge": "Push-up contest"
# }
def rewards_challenges_send():
    body = request.get_json(force=True)
    target = body.get("to")
    challenge = body.get("challenge")
    uid = _uid_or_anon()

    L.log(f"Challenge sent by {uid} to {target}: {challenge}")
    return jsonify({
        "message": "Challenge sent",
        "from": uid,
        "to": target,
        "challenge": challenge
    }), 200


@rewards_bp.get("/activity-feed")  # פיד של פעילות חברתית
# GET http://127.0.0.1:5001/rewards/activity-feed
def rewards_activity_feed():
    data = [
        {"user": "alice", "action": "unlocked achievement Code Master"},
        {"user": "bob", "action": "joined the Fitness Challenge"},
    ]
    L.log("Fetched activity feed")
    return jsonify({"feed": data}), 200


@rewards_bp.post("/celebrations")  # חגיגת הישגים
# POST http://127.0.0.1:5001/rewards/celebrations
# Body:
# {
#   "achievement_id": 1,
#   "message": "Congrats Alice for winning!"
# }
def rewards_celebrations():
    body = request.get_json(force=True)
    achievement_id = body.get("achievement_id")
    message = body.get("message")
    uid = _uid_or_anon()

    L.log(f"Celebration posted by {uid} for achievement {achievement_id}: {message}")
    return jsonify({
        "message": "Celebration posted",
        "achievement_id": achievement_id,
        "celebration": message
    }), 201


@rewards_bp.get("/rivalries")  # יריבויות משרדיות מהנות
# GET http://127.0.0.1:5001/rewards/rivalries
def rewards_rivalries():
    data = [
        {"user1": "alice", "user2": "bob", "status": "friendly rivalry"},
        {"user1": "charlie", "user2": "dave", "status": "step challenge"}
    ]
    L.log("Fetched rivalries")
    return jsonify({"rivalries": data}), 200

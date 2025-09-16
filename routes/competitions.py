from flask import Blueprint, request, jsonify
from utils.utils import L
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db import db
from datetime import datetime
from routes.games import Competition  # 👈 use Competition from games.py

competitions_bp = Blueprint('competitions_bp', __name__)

# ---------- MODELS ----------
class UserCompetition(db.Model):
    __tablename__ = 'user_competitions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), nullable=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    competition = db.relationship('Competition')

# ---------- HELPERS ----------
def _uid_or_anon() -> str:
    try:
        return get_jwt_identity() or "anonymous"
    except Exception:
        return "anonymous"

def _ser(c: Competition):
    return {
        "id": c.id,
        "title": getattr(c, "title", None),  # since Competition in games.py uses 'title'
        "description": c.description,
        "start_at": c.start_at,
        "end_at": c.end_at,
        "is_active": c.is_active,
    }

def _join_competition(category: str, default_title: str, description: str):
    """Shared logic: ensure competition exists, join it for the current user."""
    comp = Competition.query.filter_by(title=default_title).first()
    if not comp:
        comp = Competition(
            title=default_title,
            description=description,
            start_at=None,
            end_at=None,
            is_active=True
        )
        db.session.add(comp)
        db.session.commit()

    user_id = _uid_or_anon()
    existing = UserCompetition.query.filter_by(user_id=user_id, competition_id=comp.id).first()
    if existing:
        return jsonify({"message": "already joined", "competition": _ser(comp)}), 200

    uc = UserCompetition(user_id=user_id, competition_id=comp.id)
    db.session.add(uc)
    db.session.commit()
    L.log(f"Competition joined by {user_id}: {comp.title}")
    return jsonify({"message": "joined", "competition": _ser(comp)}), 200

# ---------- ROUTES ----------
@competitions_bp.post("/code-quality")
# POST http://127.0.0.1:5001/competitions/code-quality
# Body: {}
# @jwt_required(optional=True)
def competitions_code_quality():
    return _join_competition("code-quality", "Code Quality Challenge", "Improve code readability and maintainability")

@competitions_bp.post("/learning")
# POST http://127.0.0.1:5001/competitions/learning
# Body: {}
# @jwt_required(optional=True)
def competitions_learning():
    return _join_competition("learning", "Learning Challenge", "Upskill and share knowledge")

@competitions_bp.post("/fitness")
# POST http://127.0.0.1:5001/competitions/fitness
# Body: {}
# @jwt_required(optional=True)
def competitions_fitness():
    return _join_competition("fitness", "Office Fitness Challenge", "Stay active at work")

@competitions_bp.post("/sustainability")
# POST http://127.0.0.1:5001/competitions/sustainability
# Body: {}
# @jwt_required(optional=True)
def competitions_sustainability():
    return _join_competition("sustainability", "Green Office Challenge", "Promote eco-friendly practices")

@competitions_bp.post("/creativity")
# POST http://127.0.0.1:5001/competitions/creativity
# Body: {}
# @jwt_required(optional=True)
def competitions_creativity():
    return _join_competition("creativity", "Creativity Challenge", "Express and innovate")

@competitions_bp.post("/team-building")
# POST http://127.0.0.1:5001/competitions/team-building
# Body: {}
# @jwt_required(optional=True)
def competitions_team_building():
    return _join_competition("team-building", "Team Building Activity", "Strengthen collaboration")

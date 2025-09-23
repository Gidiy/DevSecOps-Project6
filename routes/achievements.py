from flask import Blueprint, request, jsonify
from utils.utils import users, L
#from werkzeug.security import generate_password_hash, check_password_hash, jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from classes.user import User
from utils.db import db
from datetime import datetime

achievements_bp = Blueprint('achievements_bp', __name__)

class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    rarity = db.Column(db.String(50), default='common')  # common/rare/epic/legendary
    points = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)
    achievement = db.relationship('Achievement')

# -----Helpers-----

def _uid_or_anon() -> str:
    user = get_jwt_identity()
    return user if user else 'anonymous'

def _ser(a: Achievement):
    return {
        'id': a.id,
        'name': a.name,
        'description': a.description,
        'rarity': a.rarity,
        'points': a.points
    }

@achievements_bp.get('/available')  # view available achievements # GET http://127.0.0.1:5001/achievements/available
def achievements_available():
    rarity = request.args.get('rarity')
    q = Achievement.query
    if rarity:
        q = q.filter_by(rarity=rarity)
    items = q.order_by(Achievement.points.desc(), Achievement.name.asc()).all()
    return jsonify([_ser(a) for a in items]), 200

@achievements_bp.post('/unlock')  # unlock achievements # POST http://127.0.0.1:5001/achievements/unlock - {"achievement_id":1}
#@jwt_required(optional=True)
def achievements_unlock():
    data = request.get_json(silent=True) or {}
    achievement_id = data.get('achievement_id')
    if not achievement_id:
        return jsonify({'error': 'achievement_id is required'}), 400

    a = Achievement.query.get(achievement_id)
    if not a:
        return jsonify({'error': 'achievement not found'}), 404

    user_id = _uid_or_anon()
    ua = UserAchievement(user_id=user_id, achievement_id=a.id)
    db.session.add(ua)
    db.session.commit()
    L.log(f'Achievement unlocked by {user_id}: {a.name}')
    return jsonify({'message': 'unlocked', 'achievement': _ser(a)}), 200

@achievements_bp.get('/my-progress')  # view achievements progress # GET http://127.0.0.1:5001/achievements/my-progress
#@jwt_required(optional=True)
def achievements_my_progress():
    user_id = _uid_or_anon()
    unlocked = UserAchievement.query.filter_by(user_id=user_id).all()
    unlocked_ids = {u.achievement_id for u in unlocked}
    all_ach = Achievement.query.all()
    return jsonify({
        'user_id': user_id,
        'unlocked': [_ser(a) for a in all_ach if a.id in unlocked_ids],
        'locked':   [_ser(a) for a in all_ach if a.id not in unlocked_ids]
    }), 200

@achievements_bp.post('/create-custom')  # create custom achievements # POST http://127.0.0.1:5001/achievements/create-custom - {"name":"My Custom Achievement", "description": "ok?" }
#@jwt_required(optional=True)
def achievements_create_custom():
    data = request.get_json(silent=True) or {}
    name = data.get('name')
    if not name:
        return jsonify({'error': 'name is required'}), 400
    a = Achievement(
        name=name,
        description=data.get('description'),
        rarity=data.get('rarity', 'common'),
        points=int(data.get('points', 10))
    )
    db.session.add(a)
    db.session.commit()
    return jsonify(_ser(a)), 201

@achievements_bp.get('/rare')  # view rare achievements # GET http://127.0.0.1:5001/achievements/rare
def achievements_rare():
    rare_set = ['rare', 'epic', 'legendary']
    items = Achievement.query.filter(Achievement.rarity.in_(rare_set)).all()
    return jsonify([_ser(a) for a in items]), 200

@achievements_bp.post('/share')  # share achievements # POST http://127.0.0.1:5001/achievements/share - {"achievement_id":1}
#@jwt_required(optional=True)
def achievements_share():
    data = request.get_json(silent=True) or {}
    achievement_id = data.get('achievement_id')
    if not achievement_id:
        return jsonify({'error': 'achievement_id is required'}), 400
    # In a real app this would publish to a social feed; for now return success.
    return jsonify({'message': 'shared', 'achievement_id': achievement_id}), 200

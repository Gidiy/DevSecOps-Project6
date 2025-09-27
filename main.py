import datetime
from flask import Flask, request, g, jsonify, redirect, url_for ,render_template
from routes.login import login_bp
from routes.achievements import achievements_bp
from routes.competitions import competitions_bp
from routes.games import games_bp
from routes.rewards import rewards_bp, Reward, Redemption
from routes.social import UserTeam
from routes.leaderboards import leaderboards_bp
from routes.social import social_bp
from classes.user import User
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from utils.utils import L, get_achievement_points
from utils.db import db  # Import from the new file
import os
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import timedelta
from classes.user import *
from routes.games import Competition, Participation, Game, UserCompetition
from routes.achievements import Achievement, UserAchievement

load_dotenv()

# Ensure Flask can resolve templates/static correctly
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
# Ensure a JWT secret exists (fallback for local dev)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY') or 'dev-secret-change-me'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
jwt = JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or 'sqlite:///instance/games.db'
db.init_app(app)


@app.before_request
def before_rq():
    L.log(f'{request.host} {request.date} -> {request.base_url}')
    g.start_time = datetime.datetime.now()


@app.after_request
def after_rg(response):
    end_time = datetime.datetime.now()
    duration = end_time - g.start_time
    L.log(f'duration [{duration.total_seconds()}] ')
    return response

app.register_blueprint(login_bp)
app.register_blueprint(games_bp, url_prefix='/games')
app.register_blueprint(achievements_bp, url_prefix='/achievements')
app.register_blueprint(competitions_bp, url_prefix='/competitions')
app.register_blueprint(rewards_bp, url_prefix='/rewards')
app.register_blueprint(leaderboards_bp, url_prefix='/leaderboards')
app.register_blueprint(social_bp, url_prefix='/social')

@app.route("/")
def homepage():
    # players + points + competition
    players = (
        db.session.query(
            User.username,
            Participation.competition_id,
            Competition.title,
            Participation.progress,
        )
        .join(Participation, User.username == Participation.user_id)
        .join(Competition, Competition.id == Participation.competition_id)
        .all()
    )

    # group competitions and total points by user
    from collections import defaultdict
    grouped = defaultdict(lambda: {"competitions": [], "total_progress": 0, "achievement_points": 0})
    for username, _competition_id, competition_title, progress in players:
        grouped[username]["competitions"].append(competition_title)
        try:
            grouped[username]["total_progress"] += int(progress or 0)
        except Exception:
            # if progress is not numeric, ignore in total
            pass

    # Calculate achievement points for each user

    def _calculate_user_achievement_points(user_id: str) -> int:
        """Calculate total achievement points for a user based on rarity"""
        unlocked = UserAchievement.query.filter_by(user_id=user_id).all()
        total_points = 0
        for ua in unlocked:
            achievement = Achievement.query.get(ua.achievement_id)
            if achievement:
                total_points += get_achievement_points(achievement.rarity)
        return total_points

    # Add achievement points, manual points, and spent points to each user
    for username in grouped:
        grouped[username]["achievement_points"] = _calculate_user_achievement_points(username)
        # Calculate spent points from redemptions
        spent = db.session.query(db.func.coalesce(db.func.sum(Redemption.points), 0)).filter_by(user_id=username).scalar() or 0
        grouped[username]["spent_points"] = int(spent)
        # Calculate manual leaderboard points (donations)
        from routes.leaderboards import ManualLeaderboardEntry
        manual_entry = ManualLeaderboardEntry.query.filter_by(user=username, board='global').first()
        grouped[username]["manual_points"] = manual_entry.points if manual_entry else 0

    players_grouped = [
        {
            "username": username,
            "competitions": sorted(set(data["competitions"])),
            "total_progress": data["total_progress"],
            "achievement_points": data["achievement_points"],
            "spent_points": data["spent_points"],
            "total_points": data["total_progress"] + data["achievement_points"] + data["manual_points"] - data["spent_points"],
        }
        for username, data in grouped.items()
    ]

    # competitions
    competitions = Competition.query.all()

    # All games with rules_json
    games = Game.query.all()

    return render_template(
        "homepage.html", 
        players=players,
        players_grouped=players_grouped,
        competitions=competitions,
        games=games
    )


@app.route("/api/players_grouped")
def api_players_grouped():
    players = (
        db.session.query(
            User.username,
            Participation.competition_id,
            Competition.title,
            Participation.progress,
        )
        .join(Participation, User.username == Participation.user_id)
        .join(Competition, Competition.id == Participation.competition_id)
        .all()
    )
    

    from collections import defaultdict
    grouped = defaultdict(lambda: {"competitions": [], "total_progress": 0, "achievement_points": 0})
    for username, _competition_id, competition_title, progress in players:
        grouped[username]["competitions"].append(competition_title)
        try:
            grouped[username]["total_progress"] += int(progress or 0)
        except Exception:
            pass

    # Calculate achievement points for each user

    def _calculate_user_achievement_points(user_id: str) -> int:
        """Calculate total achievement points for a user based on rarity"""
        unlocked = UserAchievement.query.filter_by(user_id=user_id).all()
        total_points = 0
        for ua in unlocked:
            achievement = Achievement.query.get(ua.achievement_id)
            if achievement:
                total_points += get_achievement_points(achievement.rarity)
        return total_points

    # Add achievement points, manual points, and spent points to each user
    for username in grouped:
        grouped[username]["achievement_points"] = _calculate_user_achievement_points(username)
        # Calculate spent points from redemptions
        spent = db.session.query(db.func.coalesce(db.func.sum(Redemption.points), 0)).filter_by(user_id=username).scalar() or 0
        grouped[username]["spent_points"] = int(spent)
        # Calculate manual leaderboard points (donations)
        from routes.leaderboards import ManualLeaderboardEntry
        manual_entry = ManualLeaderboardEntry.query.filter_by(user=username, board='global').first()
        grouped[username]["manual_points"] = manual_entry.points if manual_entry else 0

    players_grouped = [
        {
            "username": username,
            "competitions": sorted(set(data["competitions"])),
            "total_progress": data["total_progress"],
            "achievement_points": data["achievement_points"],
            "spent_points": data["spent_points"],
            "total_points": data["total_progress"] + data["achievement_points"] + data["manual_points"] - data["spent_points"],
        }
        for username, data in grouped.items()
    ]

    return jsonify(players_grouped)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Disable reloader so only one process listens and doesn't respawn
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
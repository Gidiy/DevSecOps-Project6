"""
Gamification Platform - Main Flask Application
=============================================

This is the main entry point for the gamification platform.
It handles user authentication, competition management, achievements,
rewards, leaderboards, and social features.

Key Features:
- User registration and JWT authentication
- Competition and game management
- Achievement system with rarity-based points
- Reward redemption and point donations
- Leaderboards and social features
- Real-time homepage with user statistics
"""

import datetime
import os
from collections import defaultdict
from datetime import timedelta

# Flask and web framework imports
from flask import Flask, request, g, jsonify, redirect, url_for, render_template
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from dotenv import load_dotenv

# Database and utility imports
from utils.db import db
from utils.utils import L, get_achievement_points

# Route blueprints (modular API endpoints)
from routes.login import login_bp
from routes.achievements import achievements_bp
from routes.competitions import competitions_bp
from routes.games import games_bp
from routes.rewards import rewards_bp, Reward, Redemption
from routes.leaderboards import leaderboards_bp
from routes.social import social_bp, UserTeam

# Database models
from classes.user import User
from routes.games import Competition, Participation, Game, UserCompetition
from routes.achievements import Achievement, UserAchievement

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# FLASK APPLICATION SETUP
# =============================================================================

# Create Flask application with custom static and template folders
app = Flask(__name__, static_folder='static', template_folder='templates')

# Enable CORS (Cross-Origin Resource Sharing) for web requests
CORS(app)

# JWT (JSON Web Token) configuration for user authentication
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY') or 'dev-secret-change-me'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Token expires in 1 hour
jwt = JWTManager(app)

# Development settings for auto-reloading templates and static files
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Database configuration - SQLite for development, can be changed to PostgreSQL for production
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or 'sqlite:///instance/games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# =============================================================================
# REQUEST LOGGING AND MONITORING
# =============================================================================

@app.before_request
def before_request():
    """Log incoming requests and start timing"""
    L.log(f'{request.host} {request.date} -> {request.base_url}')
    g.start_time = datetime.datetime.now()


@app.after_request
def after_request(response):
    """Log request duration after processing"""
    end_time = datetime.datetime.now()
    duration = end_time - g.start_time
    L.log(f'duration [{duration.total_seconds()}] ')
    return response

# =============================================================================
# BLUEPRINT REGISTRATION (MODULAR API ENDPOINTS)
# =============================================================================

# Register all route blueprints with URL prefixes
app.register_blueprint(login_bp)                                    # User authentication
app.register_blueprint(games_bp, url_prefix='/games')              # Game competitions
app.register_blueprint(achievements_bp, url_prefix='/achievements') # Achievement system
app.register_blueprint(competitions_bp, url_prefix='/competitions') # Competition management
app.register_blueprint(rewards_bp, url_prefix='/rewards')          # Rewards and donations
app.register_blueprint(leaderboards_bp, url_prefix='/leaderboards') # Leaderboards
app.register_blueprint(social_bp, url_prefix='/social')            # Social features

# =============================================================================
# MAIN ROUTES
# =============================================================================

@app.route("/")
def homepage():
    """
    Main homepage route that displays the gamification dashboard.
    
    This route aggregates data from multiple sources to show:
    - All users who have participated in any activity
    - Their competition participations (from both games and competitions routes)
    - Achievement points earned
    - Manual points (from donations)
    - Spent points (from redemptions)
    - Total calculated points
    
    Returns:
        Rendered homepage.html template with all user data
    """
    
    # =============================================================================
    # COLLECT ALL USERS FROM DIFFERENT ACTIVITY SOURCES
    # =============================================================================
    
    # Get all users who have participated in competitions (from both routes)
    all_users = set()
    
    # Get users from games route (Participation table) - tracks progress points
    games_users = db.session.query(Participation.user_id).distinct().all()
    for (user_id,) in games_users:
        all_users.add(user_id)
    
    # Get users from competitions route (UserCompetition table) - tracks membership only
    competitions_users = db.session.query(UserCompetition.user_id).distinct().all()
    for (user_id,) in competitions_users:
        all_users.add(user_id)
    
    # Get users who have unlocked achievements
    achievement_users = db.session.query(UserAchievement.user_id).distinct().all()
    for (user_id,) in achievement_users:
        all_users.add(user_id)
    
    # Get users who have manual leaderboard entries (from donations)
    from routes.leaderboards import ManualLeaderboardEntry
    manual_users = db.session.query(ManualLeaderboardEntry.user).distinct().all()
    for (user,) in manual_users:
        all_users.add(user)
    
    # Initialize grouped data for all users
    grouped = defaultdict(lambda: {"competitions": [], "total_progress": 0, "achievement_points": 0})
    
    # Add competitions from games route (Participation table)
    games_participations = (
        db.session.query(
            Participation.user_id,
            Competition.title,
            Participation.progress,
        )
        .join(Competition, Competition.id == Participation.competition_id)
        .all()
    )
    
    for user_id, competition_title, progress in games_participations:
        grouped[user_id]["competitions"].append(competition_title)
        try:
            grouped[user_id]["total_progress"] += int(progress or 0)
        except Exception:
            # if progress is not numeric, ignore in total
            pass
    
    # Add competitions from competitions route (UserCompetition table)
    competitions_participations = (
        db.session.query(
            UserCompetition.user_id,
            Competition.title,
        )
        .join(Competition, Competition.id == UserCompetition.competition_id)
        .all()
    )
    
    for user_id, competition_title in competitions_participations:
        grouped[user_id]["competitions"].append(competition_title)

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
    for username in all_users:
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
            "total_points": max(0, data["total_progress"] + data["achievement_points"] + data["manual_points"] - data["spent_points"]),
        }
        for username, data in grouped.items()
    ]

    # competitions
    competitions = Competition.query.all()

    # All games with rules_json
    games = Game.query.all()

    return render_template(
        "homepage.html", 
        players_grouped=players_grouped,
        competitions=competitions,
        games=games
    )


@app.route("/api/players_grouped")
def api_players_grouped():
    # Get all users who have participated in competitions (from both routes)
    from collections import defaultdict
    
    # Get all users from both Participation (games route) and UserCompetition (competitions route)
    all_users = set()
    
    # Get users from games route (Participation table)
    games_users = db.session.query(Participation.user_id).distinct().all()
    for (user_id,) in games_users:
        all_users.add(user_id)
    
    # Get users from competitions route (UserCompetition table)
    competitions_users = db.session.query(UserCompetition.user_id).distinct().all()
    for (user_id,) in competitions_users:
        all_users.add(user_id)
    
    # Get users from achievements
    achievement_users = db.session.query(UserAchievement.user_id).distinct().all()
    for (user_id,) in achievement_users:
        all_users.add(user_id)
    
    # Get users from manual leaderboard entries
    from routes.leaderboards import ManualLeaderboardEntry
    manual_users = db.session.query(ManualLeaderboardEntry.user).distinct().all()
    for (user,) in manual_users:
        all_users.add(user)
    
    # Initialize grouped data for all users
    grouped = defaultdict(lambda: {"competitions": [], "total_progress": 0, "achievement_points": 0})
    
    # Add competitions from games route (Participation table)
    games_participations = (
        db.session.query(
            Participation.user_id,
            Competition.title,
            Participation.progress,
        )
        .join(Competition, Competition.id == Participation.competition_id)
        .all()
    )
    
    for user_id, competition_title, progress in games_participations:
        grouped[user_id]["competitions"].append(competition_title)
        try:
            grouped[user_id]["total_progress"] += int(progress or 0)
        except Exception:
            # if progress is not numeric, ignore in total
            pass
    
    # Add competitions from competitions route (UserCompetition table)
    competitions_participations = (
        db.session.query(
            UserCompetition.user_id,
            Competition.title,
        )
        .join(Competition, Competition.id == UserCompetition.competition_id)
        .all()
    )
    
    for user_id, competition_title in competitions_participations:
        grouped[user_id]["competitions"].append(competition_title)

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
    for username in all_users:
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
            "total_points": max(0, data["total_progress"] + data["achievement_points"] + data["manual_points"] - data["spent_points"]),
        }
        for username, data in grouped.items()
    ]

    return jsonify(players_grouped)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Disable reloader so only one process listens and doesn't respawn
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
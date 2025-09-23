import datetime
from flask import Flask, request, g, jsonify, redirect, url_for ,render_template
from routes.login import login_bp
from routes.achievements import achievements_bp
from routes.competitions import competitions_bp
from routes.games import games_bp
from routes.leaderboards import leaderboards_bp
from routes.rewards import rewards_bp
from routes.social import social_bp
from classes.user import User
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from utils.utils import L
from utils.db import db  # Import from the new file
import os
from dotenv import load_dotenv
from datetime import timedelta
from classes.user import *
from routes.games import Competition, Participation,Game
from routes.achievements import Achievement, UserAchievement

load_dotenv()

app = Flask('Project6')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
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
app.register_blueprint(leaderboards_bp, url_prefix='/leaderboards')
app.register_blueprint(rewards_bp, url_prefix='/rewards')
app.register_blueprint(social_bp, url_prefix='/social')

@app.route("/")
def homepage():
    # players + points + competition
    players = (
        db.session.query(
            User.username, 
            Participation.competition_id,
            Competition.title, 
            Participation.progress
        )
        .join(Participation, User.username == Participation.user_id)
        .join(Competition, Competition.id == Participation.competition_id)
        .all()
    )

    # competitions
    competitions = Competition.query.all()

    # כל ה-games עם rules_json
    games = Game.query.all()

    return render_template(
        "homepage.html", 
        players=players, 
        competitions=competitions,
        games=games
    )



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001)
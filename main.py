import datetime

from flask import Flask, request, g, jsonify
from routes.achievements import achievements_bp
from routes.competitions import competitions_bp
from routes.games import games_bp
from routes.leaderboards import leaderboards_bp
from routes.rewards import rewards_bp
from routes.social import social_bp
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from utils.utils import L
from utils.db import db  # Import from the new file
import os
from dotenv import load_dotenv
from datetime import timedelta

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


app.register_blueprint(games_bp, url_prefix='/games')
app.register_blueprint(achievements_bp, url_prefix='/achievements')
app.register_blueprint(competitions_bp, url_prefix='/competitions')
app.register_blueprint(leaderboards_bp, url_prefix='/leaderboards')
app.register_blueprint(rewards_bp, url_prefix='/rewards')
app.register_blueprint(social_bp, url_prefix='/social')


@app.route('/') #postman - http://127.0.0.1:5001/
def homepage():
    return 'Welcome to Project6!'

#try jwt
users_db = {} 

@app.post('/register') #postman - http://127.0.0.1:5001/register - {"username":"gilad","password":123}
def register_user():
    """Endpoint to register a new user."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    if username in users_db:
        return jsonify({"msg": "User already exists"}), 409
    
    # In a real application, you should hash the password before saving it
    users_db[username] = password
    
    return jsonify({"msg": f"User {username} registered successfully"}), 201

@app.post('/login')#postman - http://127.0.0.1:5001/login - {"username":"gilad","password":123}
def login_user():
    """Endpoint for user login."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    if username in users_db and users_db[username] == password:
        # Create a JWT token for the user
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200 # got token - {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1Njg5MDI1MCwianRpIjoiYzZiYWY2MDYtNzdiYy00ODdkLWI4ZTUtYWFhZDQ3ZjJiYjgwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImdpbGFkIiwibmJmIjoxNzU2ODkwMjUwLCJjc3JmIjoiYTAyNmNmZDEtMTE0OC00ODkzLTkzMTQtOWNjMjlmZWUyNzg4IiwiZXhwIjoxNzU2ODkxMTUwfQ.Pl_utwhlMHhE3VelPXHs71h3z8mEug0ewXWGhiu2IX8"}
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@app.get('/protected')# postman - auth - bearer Token - Token - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1Njg5NTUxMywianRpIjoiZmU2ODdkMjUtOTcwNS00OWQ2LThkNWQtMzA5MGEyNmQ2ZTcyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImdpbGFkIiwibmJmIjoxNzU2ODk1NTEzLCJjc3JmIjoiYzU4NjIyNjgtZDdkZC00OTAxLWE2YzUtNWViYTYxZGVlOGUyIiwiZXhwIjoxNzU2ODk2NDEzfQ.S8_eh7zr2chmYrsMahVdpDYWltKY-JqLC2ck5JsEDpI
@jwt_required() #expire in 15 minutes
def protected_route():
    """A protected endpoint that requires a valid JWT."""
    # Access the user identity from the JWT
    current_user_username = get_jwt_identity()
    return jsonify(logged_in_as=current_user_username), 200
#end try jwt

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001)
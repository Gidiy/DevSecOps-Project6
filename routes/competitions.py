from flask import Blueprint, request, jsonify
from utils.utils import users, L
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from dao.user import User
from utils.db import db

competitions_bp = Blueprint('competitions_bp', __name__)

@competitions_bp.post("/code-quality")  # תחרויות איכות קוד
def competitions_code_quality():
    # TODO: implement logic
    return 200

@competitions_bp.post("/learning") #אתגרי למידה
def competitions_learning():
    # TODO: implement logic
    return 200

@competitions_bp.post("/fitness")  # אתגרי כושר במשרד
def competitions_fitness():
    # TODO: implement logic
    return 200

@competitions_bp.post("/sustainability")  # תחרויות משרד ירוק
def competitions_sustainability():
    # TODO: implement logic
    return 200

@competitions_bp.post("/creativity")  #  אתגרים יצירתיים
def competitions_creativity():
    # TODO: implement logic
    return 200

@competitions_bp.post("/team-building")  #  פעילויות בניית צוות
def competitions_team_building():
    # TODO: implement logic
    return 200


'''
@competitions_bp.post('/signup') #postman - http://127.0.0.1:5001/user/signup body(raw) - { "username": "gilad", "password": "123" }
def signup():
    try:
        data = request.json
        if 'password' not in request.json.keys() or 'username' not in request.json.keys():
            return 'name and password are required ', 403
        data['password'] = generate_password_hash(data['password'])
        print(data)
        for user in users:
            if user['username'] == data['username']:
                return 'already exists', 403

        # users.append(data)
        user1 = User(username=data['username'], password=data['password'])
        db.session.add(user1)
        db.session.commit()
        L.log(f'user added [{data["username"]}]')
        return 'got it', 201
    except Exception as e:
        return str(e), 200


@competitions_bp.post('/login')
def login():
    username = request.json['username']
    password = request.json['password']

    # Query the database instead of "users" list
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return {'msg': "username or password incorrect"}, 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@competitions_bp.get('/')  # Postman - GET http://127.0.0.1:5001/user
def get_all_users():
    # Query all users from the DB
    users = User.query.all()

    # Convert SQLAlchemy objects to plain dicts so they can be JSONified
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "username": u.username,
            "password": u.password
            # Do NOT return password hashes in a real app!
        })

    return jsonify(result), 200
'''
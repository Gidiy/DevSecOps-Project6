from flask import Blueprint, request, jsonify
from utils.utils import users, L
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from dao.user import User
from utils.db import db

achievements_bp = Blueprint('achievements_bp', __name__)


@achievements_bp.get('/available')  # צפייה בהישגים זמינים
def achievements_available():
    # TODO: implement logic
    return 200


@achievements_bp.post('/unlock')  #  פתיחת הישגים
def achievements_unlock():
    # TODO: implement logic
    return 200

@achievements_bp.get('/my-progress')  #  התקדמות אישית בהישגים
def achievements_my_progress():
    # TODO: implement logic
    return 200

@achievements_bp.post('/create-custom')  #  צירת הישגים מותאמים אישית
def achievements_create_custom():
    # TODO: implement logic
    return 200

@achievements_bp.get('/rare')  # צפייה בהישגים נדירים
def achievements_rare():
    # TODO: implement logic
    return 200

@achievements_bp.post('/share')  #  שיתוף הישגים קטגוריות תחרות
def achievements_share():
    # TODO: implement logic
    return 200
    
'''
@achievements_bp.post('/signup') #postman - http://127.0.0.1:5001/user/signup body(raw) - { "username": "gilad", "password": "123" }
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


@achievements_bp.post('/login')
def login():
    username = request.json['username']
    password = request.json['password']

    # Query the database instead of "users" list
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return {'msg': "username or password incorrect"}, 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@achievements_bp.get('/')  # Postman - GET http://127.0.0.1:5001/user
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
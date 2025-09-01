from flask import Blueprint, jsonify, request
from utils.utils import movies, L
from flask_jwt_extended import jwt_required, get_jwt_identity

games_bp = Blueprint('games_bp', __name__)


@games_bp.post('/create') #יצירת תחרות חדשה
def create_game():
    return 200

@games_bp.get('/active') #צפייה בתחרויות פעילות
def active_game():
    return jsonify({'status': 'success'}), 200

@games_bp.post('/join') #הצטרפות לתחרות
def join_game():
    return 200

@games_bp.put('/progress/update') #עדכון התקדמות התחרות
def update_progress_game():
    return 200

@games_bp.get('/rules/update') #קבלת כללי תחרות
def update_rules_game():
    return jsonify({'status': 'success'}), 200

@games_bp.post('/custom/create') #  אישית יצירת כללי משחק מותאמים 
def create_custom_rules_game():
    return 200


'''
@games_bp.get('/') #postman - http://127.0.0.1:5001/games/
def get_all():
    return jsonify(movies)


@games_bp.get('/<int:id>')#postman - http://127.0.0.1:5001/games/1
@jwt_required()
def get_by_id(id):
    for movie in movies:
        if movie.get('id') == id:
            print(get_jwt_identity())
            return jsonify(movie)
    return jsonify({'status': 'not found'}), 404


@games_bp.post('/') #postman - http://127.0.0.1:5001/games/ body(raw) - {"name": "spiderman11", "rate": 3.9 }-only if has "name"
#@jwt_required()
def add_game():
    new_game = request.json
    if not new_game or 'name' not in new_game:
        return jsonify({'status': 'bad request', 'message': 'name is required'}), 400
    new_id = max([game['id'] for game in games], default=0) + 1
    new_game['id'] = new_id
    games.append(new_game)
    L.log(f'Game added {new_game["name"]}')
    return jsonify(new_game), 201


@games_bp.put('/<int:id>')#postman - http://127.0.0.1:5001/games/1 body(raw) - {  "name": "bax", "rate": 3.0 }
def update_game(id):
    update_data = request.json

    if not update_data:
        return jsonify({'status': 'bad request', 'message': 'no data provided'}), 400

    for movie in movies:
        if game.get('id') == id:
            if 'name' in update_data:
                movie['name'] = update_data['name']
            if 'rate' in update_data:
                movie['rate'] = update_data['rate']
            return jsonify(movie)

    return jsonify({'status': 'not found'}), 404


@games_bp.delete('/<int:id>')#postman - http://127.0.0.1:5001/movies/1 
def delete_by_id(id):
    for i, movie in enumerate(movies):
        if movie.get('id') == id:
            deleted_movie = movies.pop(i)
            return jsonify({'status': 'deleted', 'movie': deleted_movie})

    return jsonify({'status': 'not found'}), 404


@games_bp.delete('/')#postman - http://127.0.0.1:5001/movies
def delete_all():
    deleted_count = len(movies)
    movies.clear()#return []
    return jsonify({'status': 'deleted', 'count': deleted_count})
'''
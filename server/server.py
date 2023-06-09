import requests
import json
import datetime

from flask import Flask, request, jsonify

from mongoConnection import MongoConnection
from app.Enums.modeEnum import *

app = Flask(__name__)
port = 8080

@app.route('/')
def hello():
    return 'Server for chess application'

@app.route('/register', methods=['POST'])
def register():
    try:
        data = json.loads(request.data)
        username = data.get('username')

        existing_user = mongo.users.find_one({'username': username})
        if existing_user:
            response = {'error': 'User with the same username already exists.'}
            return jsonify(response), 409

        mongo.users.insert_one(data)

        response = {'message': 'User registered successfully!'}
        return jsonify(response), 200

    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", str(e))
        return jsonify({'message': 'An error occurred during the request.'}), 500

@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    # print(data)

    username = data.get('username')
    password = data.get('password')

    try:

        existing_user = mongo.users.find_one({'username': username})

        if not existing_user:
            response = {'message': 'Invalid username or password'}
            return jsonify(response), 401

        if existing_user['password'] != password:
            response = {'message': 'Invalid username or password'}
            return jsonify(response), 401

        response = {'message': 'User registered successfully!'}
        return jsonify(response), 200

    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", str(e))
        return jsonify({'message': 'An error occurred during the request.'}), 500

@app.route('/stats', methods=['POST'])
def get_statistics():

    data = request.get_json()

    username = data['username']

    try:

        pipeline = [
            {"$match": {"username": username}},
            {"$unwind": "$PLAYER_VS_COMPUTER.games"},
            {"$group": {
                "_id": "$username",
                "wins": {"$sum": {"$cond": [{"$eq": ["$PLAYER_VS_COMPUTER.games.res", 1]}, 1, 0]}},
                "losses": {"$sum": {"$cond": [{"$eq": ["$PLAYER_VS_COMPUTER.games.res", -1]}, 1, 0]}}
            }}
        ]

        result = mongo.users.aggregate(pipeline)

        if result:
            stats = result.next()
            response = {
                'message': 'User statistics fetched successfully!',
                'wins': stats['wins'],
                'losses': stats['losses']
            }
            return jsonify(response), 200
        else:
            response = {'message': 'No user found'}
            return jsonify(response), 401



    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", str(e))
        return jsonify({'message': 'An error occurred during the request.'}), 500

@app.route('/score', methods=['PUT'])
def update_score():

    data = request.get_json()
    username = data['username']
    res = data['res']
    game_state = data['game_state']
    difficulty = data['difficulty']

    try:
        existing_user = mongo.users.find_one({"username": username})

        if not existing_user:
            response = {'message': 'No user found'}
            return jsonify(response), 401


        game_info = {
            "game_state": game_state,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "difficulty": difficulty,
            "res": res
        }
        mongo.users.update_one(
            {"username": username},
            {"$push": {"PLAYER_VS_COMPUTER.games": game_info}}
        )

        response = {
            'message': 'Score updated successfully!',
        }

        return jsonify(response), 200

    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", str(e))
        return jsonify({'message': 'An error occurred during the request.'}), 500

@app.route('/top_players', methods=['GET'])
def get_top_players():
    try:
        pipeline = [
            {
                '$project': {
                    'username': 1,
                    'ranking': {
                        '$sum': {
                            '$map': {
                                'input': '$PLAYER_VS_COMPUTER.games',
                                'as': 'game',
                                'in': {
                                    '$multiply': [
                                        5,
                                        '$$game.difficulty',
                                        '$$game.res'
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            {
                '$addFields': {
                    'ranking': {
                        '$add': [1000, '$ranking']
                    }
                }
            },
            {
                '$sort': {'ranking': -1}
            },
            {
                '$limit': 10
            }
        ]

        result = mongo.users.aggregate(pipeline)

        top_10 = []
        for player in result:
            username = player['username']
            ranking = player['ranking']
            top_10.append({'playername': username, 'ranking': ranking})

        response = {
            'top_10': top_10,
            'message': "Top 10 players fetched successfully from the database"
        }

        return jsonify(response)

    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", str(e))
        return jsonify({'message': 'An error occurred during the request.'}), 500

@app.route('/save_game', methods=['PUT'])
def save_game():

    data = request.get_json()
    username = data['username']
    game_state = data['game_state']
    difficulty = data['difficulty']

    try:
        existing_user = mongo.users.find_one({"username": username})

        if not existing_user:
            response = {'message': 'No user found'}
            return jsonify(response), 401


        game_info = {
            "game_state": game_state,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "difficulty": difficulty,
        }

        mongo.users.update_one(
            {"username": username},
            {"$set": {"PLAYER_VS_COMPUTER.last_save": game_info}}
        )

        response = {
            'message': 'Game state saved successfully!',
        }

        return jsonify(response), 200

    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", str(e))
        return jsonify({'message': 'An error occurred during the request.'}), 500

    # {"username": username},
    # {"$push": {"PLAYER_VS_COMPUTER.games": game_info}}



# @app.route('/delete_users', methods=['DELETE'])
# def delete_users():
#     try:
#         result = mongo.users.delete_many({})
#
#         deleted_count = result.deleted_count
#
#         response = {'message': f'{deleted_count} users deleted successfully!'}
#         return jsonify(response), 200
#
#     except requests.exceptions.RequestException as e:
#         print("Error occurred during the request:", str(e))
#         return jsonify({'message': 'An error occurred during the request.'}), 500



if __name__ == '__main__':
    mongo = MongoConnection()
    mongo.initMongoConnection()
    app.run(host='localhost', port=port)

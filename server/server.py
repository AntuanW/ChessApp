import requests
import json

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
    req_enum_val = data['mode']

    try:

        existing_user = mongo.users.find_one({"username": username})

        enum_val = get_key_by_value(req_enum_val)

        wins = existing_user[enum_val]['wins']
        losses = existing_user[enum_val]['loses']

        response = {
            'message': 'User statistics fetched successfully!',
            'wins': wins,
            'loses': losses
        }
        return jsonify(response), 200

    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", str(e))
        return jsonify({'message': 'An error occurred during the request.'}), 500


import datetime

@app.route('/score', methods=['PUT'])
def update_score():

    data = request.get_json()
    username = data['username']
    score = data['score']
    game_state = data['game_state']

    try:
        existing_user = mongo.users.find_one({"username": username})

        if not existing_user:
            response = {'message': 'No user found'}
            return jsonify(response), 401

        if score == 0:
            mongo.users.update_one(
                {"username": username},
                {"$inc": {"PLAYER_VS_COMPUTER.loses": 1}}
            )
        elif score == 1:
            mongo.users.update_one(
                {"username": username},
                {"$inc": {"PLAYER_VS_COMPUTER.wins": 1}}
            )
        else:
            response = {'message': 'Invalid score value'}
            return jsonify(response), 400

        game_info = {
            "game_state": game_state,
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
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

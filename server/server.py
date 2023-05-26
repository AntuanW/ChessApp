import requests
import json

from flask import Flask, request, jsonify
from mongoConnection import MongoConnection


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


if __name__ == '__main__':
    mongo = MongoConnection()
    mongo.initMongoConnection()
    app.run(host='localhost', port=port)



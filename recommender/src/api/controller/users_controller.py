from flask import request
from flask import jsonify

from src.service.persistency import persistence_service

def init(app):
    @app.route('/users/create_user_with_text/', methods=['POST'])
    def create_user_with_text():
        body = request.json
        text = body['text']

        user_id = persistence_service.create_user()
        persistence_service.insert_user_input(user_id, text, None)

        # for simplicity reasons the cookie is set manually
        cookie = { "user_id": user_id }
        response = { "cookie": cookie }

        return jsonify(response)

    @app.route('/users/create_user_with_twitter_name/', methods=['POST'])
    def create_users_with_twitter_name():
        body = request.json
        twitter_name = body['twitter_name']

        print(twitter_name)

        user_id = persistence_service.create_user()
        persistence_service.insert_user_input(user_id, None, twitter_name)

        # for simplicity reasons the cookie is set manually
        cookie = { "user_id": user_id }
        response = { "cookie": cookie }

        return jsonify(response)

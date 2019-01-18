from flask import request
from flask import jsonify
import json

# from src.service import classifier_service

from src.service.persistency import pandas_persistence_service

def init(app):

    @app.route("/classify", methods = ['POST'])
    def classify():
        body = request.json

        similarArticle = classifier_service.classify(body['query'])

        return similarArticle.reset_index().to_json(orient='records')

    @app.route('/points_of_interests/<id>')
    def get(id):
        assert id == request.view_args['id']
        result = pandas_persistence_service.get_points_of_interests_by_id_as_df(id)

        return result.reset_index().to_json(orient='records')

    @app.route('/points_of_interests/')
    def get_all():
        result = pandas_persistence_service.get_all_points_of_interests_as_df()

        return result.reset_index().to_json(orient='records')

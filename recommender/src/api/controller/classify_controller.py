from flask import request
from flask import jsonify
import json

# from src.service import classifier_service

from src.service.persistency import pandas_persistence_service
from src.service.persistency import persistence_service

def init(app):
    @app.route("/classify", methods = ['POST'])
    def classify():
        body = request.json

        similarArticle = classifier_service.classify(body['query'])

        return similarArticle.reset_index().to_json(orient='records')

    @app.route('/points_of_interests/<id>')
    def get(id):
        assert id == request.view_args['id']
        poi_data_frame = pandas_persistence_service.get_points_of_interests_by_id_as_df(id)

        poi_data_frame['text'] = poi_data_frame.apply(lambda row: persistence_service.get_text_for_poi(row.id)[1], axis=1)

        return poi_data_frame.reset_index().to_json(orient='records')

    @app.route('/points_of_interests/')
    def get_all():
        poi_data_frame = pandas_persistence_service.get_all_points_of_interests_as_df()

        return result.reset_index().to_json(orient='records')

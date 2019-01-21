from flask import request
from flask import jsonify
import json

from src.service import classifier_service

from src.service.persistency import pandas_persistence_service
from src.service.persistency import persistence_service

def add_source_column_to_data_frame(poi_data_frame):
    poi_data_frame['source'] = poi_data_frame.apply(lambda row: persistence_service.get_text_for_poi(row.id), axis=1)

    return poi_data_frame

def init(app):
    @app.route("/classify", methods = ['POST'])
    def classify():
        body = request.json

        poi_data_frame = classifier_service.classify(body['query']).reset_index()
        poi_data_frame = add_source_column_to_data_frame(poi_data_frame)

        return poi_data_frame.reset_index().to_json(orient='records')

    @app.route('/points_of_interests/<id>')
    def get(id):
        assert id == request.view_args['id']

        poi_data_frame = pandas_persistence_service.get_points_of_interests_by_id_as_df(id).reset_index()
        poi_data_frame = add_source_column_to_data_frame(poi_data_frame)

        return poi_data_frame.to_json(orient='records')

    @app.route('/points_of_interests/')
    def get_all():
        poi_data_frame = pandas_persistence_service.get_all_points_of_interests_as_df().reset_index()[10:100]
        poi_data_frame = add_source_column_to_data_frame(poi_data_frame)

        return poi_data_frame.to_json(orient='records')

    @app.route('/insertRating/<u_id>/<poi_id>/<rating>')
    def insertRating():
        assert u_id == request.view_args['u_id']
        assert poi_id == request.view_args['poi_id']
        assert rating == request.view_args['rating']

        persistence_service.insert_rating(u_id, poi_id, rating)

        
    # @app.route('/points_of_interests_for_user/<userId>')
    # def get_recommendations_for_user(user_id):
    #     print('get_recommendations_for_user')

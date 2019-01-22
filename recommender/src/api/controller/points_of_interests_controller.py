from flask import request
from flask import jsonify
import json

import pandas as pd

from src.service.persistency import pandas_persistence_service
from src.service.persistency import persistence_service

from src.service.collaborative_filtering import user2user_recommender
from src.service.collaborative_filtering import filterWeather, filterLocation

from src.service import classifier_service

def append_source_column_to_data_frame(poi_data_frame):
    poi_data_frame['source'] = poi_data_frame.apply(lambda row: persistence_service.get_text_for_poi(row.id), axis=1)

def append_current_poi_rating_to_dataframe(user_id, poi_data_frame):
    poi_data_frame['liked'] = None
    if user_id:
        for index, row in poi_data_frame.iterrows():
            liked = persistence_service.get_poi_rating_for_user(row.id, user_id)
            poi_data_frame.at[index, 'liked'] = liked

def init(app):
    @app.route('/points_of_interests/<id>/')
    @app.route('/points_of_interests/<id>/<user_id>')
    def get(id, user_id = None):
        assert id == request.view_args['id']

        poi_data_frame = pandas_persistence_service.get_points_of_interests_by_id_as_df(id).reset_index()

        append_source_column_to_data_frame(poi_data_frame)
        append_current_poi_rating_to_dataframe(user_id, poi_data_frame)

        return poi_data_frame.to_json(orient='records')

    @app.route('/points_of_interests/')
    def get_all():
        poi_data_frame = pandas_persistence_service.get_all_points_of_interests_as_df().reset_index()[10:100]
        poi_data_frame = append_source_column_to_data_frame(poi_data_frame)

        return poi_data_frame.to_json(orient='records')

    @app.route("/points_of_interests/personal_recommendations/<user_id>/<user_lat>/<user_long>/<radius>/")
    @app.route("/points_of_interests/personal_recommendations/<user_id>/<user_lat>/<user_long>/<radius>/<consider_weather>/<force_bad_weather>")
    def classify_content_based_collaborative_filtering(user_id, user_lat, user_long, radius, consider_weather = False, force_bad_weather = False):
        if persistence_service.get_recommenderType(user_id) == "collaborativeFiltering" and user2user_recommender.eval(user_id) < 0.001:
            # COLLABORATIVE FILTERING
            recommendations = user2user_recommender.getRecommendationsForUser(user_id)
            usersCurrentLocation = {'lat':user_lat, 'lng':user_long} #some place in berlin

            # apply filter: weather
            recommendations = filterWeather.filterOnWeather(usersCurrentLocation, recommendations, weatherApi_bool, forceBadWeather_bool)

            # applyfilter: location
            recommendations = filterLocation.filterOnLocation(usersCurrentLocation, recommendations, radius)

            # return results
            return recommendations.reset_index().to_json(orient='records')

        else:
            #CONTENT-BASED RECOMMENDATION
            poi_data_frame = classifier_service.do_classification_for_user(user_id).reset_index()

            append_source_column_to_data_frame(poi_data_frame)

            return poi_data_frame.to_json(orient='records')

from flask import request
from flask import jsonify

from src.service.persistency import persistence_service

from src.service.persistency import pandas_persistence_service
from src.service.persistency import persistence_service
from src.service.collaborative_filtering import user2user_recommender
from src.service.collaborative_filtering import filterWeather, filterLocation

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

    @app.route('/users/rate_poi/<u_id>/<poi_id>/<rating>')
    def insertRating():
        assert u_id == request.view_args['u_id']
        assert poi_id == request.view_args['poi_id']
        assert rating == request.view_args['rating']

        persistence_service.insert_rating(u_id, poi_id, rating)

    @app.route("/users/get_personal_recommendations", methods = ['POST'])
    def classify_content_based_collaborative_filtering():
        body = request.json

        # Step 1: Copy parameters to local variables
        user_id = body['user_id']
        weather_api_bool = body['weatherAPI']
        force_bad_weather_bool = body['forceBadWeather']
        user_lat = body['lat']
        user_lng = body['long']
        radius = body['radius']

        # Step 2: Decide wether recommendation is content-based or collaborative filtering
        if persistence_service.get_recommenderType(currentUserId) == "collaborativeFiltering" and user2user_recommender.eval(currentUserId) < 0.001:
                # COLLABORATIVE FILTERING
                recommendations = user2user_recommender.getRecommendationsForUser(currentUserId)
                usersCurrentLocation = {'lat':user_lat, 'lng':user_lng} #some place in berlin

                # apply filter: weather
                recommendations = filterWeather.filterOnWeather(usersCurrentLocation, recommendations, weatherApi_bool, forceBadWeather_bool)

                # applyfilter: location
                recommendations = filterLocation.filterOnLocation(usersCurrentLocation, recommendations, radius)

                # return results
                return recommendations.reset_index().to_json(orient='records')

        else:
            #CONTENT-BASED RECOMMENDATION
            poi_data_frame = classifier_service.classify(body['query']).reset_index()
            poi_data_frame = add_source_column_to_data_frame(poi_data_frame)
            return poi_data_frame.reset_index().to_json(orient='records')

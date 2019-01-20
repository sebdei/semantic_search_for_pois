from src.service.embedding_preprocess import embedding_preprocess
from src.service.embedding_preprocess import visitBerlin_search
from src.service.acquisition.open_street_map import import_osm_points_of_interest
from src.service.acquisition.open_data_berlin import import_odb_points_of_interest
from src.service.schema_fusion import import_into_poi_table
from src.service.restore_default import restore_default_database
from src.service.collaborative_filtering import user2user_recommender
from src.service.collaborative_filtering import filterWeather, filterLocation
from src.service.persistency.persistence_service import get_text_for_poi, create_schemata

# import pandas as pd

# from src.api import flask

def run():
    # flask.bindRoutes()


    # do a manual import of from source (ODB/OSM/Wikipedia/VisitBerlin)
    # create_schemata()
    # import_odb_points_of_interest()
    # import_osm_points_of_interest()
    # import_into_poi_table()


    # drop all tables and import default data
    restore_default_database()

    ### Tests ###

    # test text retrieval for POI ID
    # result_dict = get_text_for_poi(83)
    # print(result_dict)

    # test collaborative filtering
    recommendations = user2user_recommender.getRecommendationsForUser(1)
    usersCurrentLocation = {'lat':52.520008, 'lng':13.404954} #some place in berlin
    filterWeather.filterOnWeather(usersCurrentLocation, recommendations)
    #filterLocation.filterOnLocation(usersCurrentLocation, recommendations, 6)
    print("stopper")


    # (re-) calculate the word embedding feature vector
    # embedding_preprocess.init_word_embeddings_calculation_for_articles()

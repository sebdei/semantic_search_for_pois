# from src.service import wikipedia_search
# from src.service import embedding_preprocess
#
# from src.service import model_provider
# from src.service import similarity_service
# from src.service import word_embedding_service

# from src.service.persistency import pandas_persistence_service
from src.service.embedding_preprocess import embedding_preprocess
from src.service.embedding_preprocess import visitBerlin_search
from src.service.acquisition.open_street_map import import_osm_points_of_interest
from src.service.acquisition.open_data_berlin import import_odb_points_of_interest
from src.service.schema_fusion import import_into_poi_table
from src.service.restore_default import restore_default_database

# import pandas as pd

# from src.api import flask

def run():
    # flask.bindRoutes()


    # do a manual import of from source (ODB/OSM/Wikipedia/VisitBerlin)
    # import_odb_points_of_interest()
    # import_osm_points_of_interest()
    # import_into_poi_table()


    # drop all tables and import default data
    restore_default_database()
    

    # (re-) calculate the word embedding feature vector
    # embedding_preprocess.init_word_embeddings_calculation_for_articles()




    # -- similarity --

    #
    # model = model_provider.provide_glove_model()
    #
    #
    # userinput = 'art museum'
    # cleanedinput = embedding_preprocess.clean_article(userinput, model)
    #
    # print(cleanedinput)
    #
    # userinputarray = word_embedding_service.calculate_mean_vector_of_word_embeddings_for_text(cleanedinput, model)
    #
    # result = similarity_service.determine_similar_items_with_cosine_similarity(userinputarray, dataframe)
    #
    # print(result)

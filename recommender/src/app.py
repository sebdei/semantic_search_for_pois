from . import acquisition

# from src.service import wikipedia_search
# from src.service import embedding_preprocess
#
# from src.service import model_provider
# from src.service import similarity_service
# from src.service import word_embedding_service

# from src.service.persistency import pandas_persistence_service
from src.service.embedding_preprocess import embedding_preprocess
from src.service.embedding_preprocess import visitBerlin_search
from src.service.open_street_map import import_osm_points_of_interest
from src.service.schema_fusion import import_into_poi_table

# import pandas as pd

# from src.api import flask

def run():
    # flask.bindRoutes()
    # acquisition.init_acqusition()
    # import_osm_points_of_interest()
    # import_into_poi_table()
    
    visitBerlin = visitBerlin_search.VisitBerlin()
    visitBerlin.initializeArticles()
    print(visitBerlin.find('Maxim Gorki Theater'))
    dataframe = visitBerlin.perform_visitBerlin_lookup()

    #embedding_preprocess.init_word_embeddings_calculation_for_articles()

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

# from .api import flask
from .acquisition import perform_acqusition

from src.service import wikipedia_search
from src.service import persistence_service
from src.service import word2vec_preprocess

from src.service import model_provider
from src.service import similarity_service
from src.service import word_embedding_service


import pandas as pd

def run():
    # persistence_service.create_initial_schema()
    # perform_acqusition()

    dataframe = wikipedia_search.perform_wikipedia_lookup()
    weighted_word_matrix = word2vec_preprocess.determine_weighted_word_embeddings_for_articles(dataframe)

    for index, row in weighted_word_matrix.iterrows():
        persistence_service.update_weighted_word2vec_by_id(index, row.get_values().tolist())


    # -- similarity --
    # columns = ['id', 'name', 'street_name', 'street_number', 'zip_code', 'long', 'lat', 'opening_hours', 'weighted_word2vec']
    # dataframe = pd.DataFrame(persistence_service.get_all_points_of_interests(), columns = columns)[['id', 'name', 'weighted_word2vec']]
    #
    # model = model_provider.provide_glove_model()
    # userinputarray = word_embedding_service.calculate_mean_vector_of_word_embeddings_for_text('Donald trump has stated to visit Berlin and its favourit places. He likes Jewish art and german history museums.', model)
    #
    # result = similarity_service.determine_similar_items_with_cosine_similarity(userinputarray, dataframe)
    #
    # print(result)

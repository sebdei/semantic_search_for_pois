from . import acquisition

# from src.service import wikipedia_search
# from src.service import word2vec_preprocess
#
# from src.service import model_provider
# from src.service import similarity_service
from src.service import word_embedding_service

from src.service.persistency import pandas_persistency_service
from src.service.word2vec_preprocess import word2vec_preprocess

import pandas as pd

def run():
    # acquisition.init_acqusition()
    word2vec_preprocess.init_word_embeddings_calculation_for_articles()

    # -- similarity --

    #
    # model = model_provider.provide_glove_model()
    #
    #
    # userinput = 'art museum'
    # cleanedinput = word2vec_preprocess.clean_article(userinput, model)
    #
    # print(cleanedinput)
    #
    # userinputarray = word_embedding_service.calculate_mean_vector_of_word_embeddings_for_text(cleanedinput, model)
    #
    # result = similarity_service.determine_similar_items_with_cosine_similarity(userinputarray, dataframe)
    #
    # print(result)

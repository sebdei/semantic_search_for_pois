# from .api import flask
from .acquisition import perform_acqusition

from src.service import wikipedia_search
from src.service import persistence_service
from src.service import word2vec_preprocess


def run():
    # persistence_service.create_initial_schema()
    # perform_acqusition()

    dataframe = wikipedia_search.perform_wikipedia_loopup()
    weighted_word_matrix = word2vec_preprocess.determine_weighted_word_embeddings_for_articles(dataframe)

    for index, row in weighted_word_matrix.iterrows():
        persistence_service.update_weighted_word2vec_by_id(index, row.get_values().tolist())

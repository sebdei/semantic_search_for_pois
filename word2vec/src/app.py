# from .api import flask
# from .acquisition import perform_acqusition

from src.service import wikipedia_search
from src.service import visitBerlin_search
from src.service import persistence_service
from src.service import word2vec_preprocess

from src.service import model_provider
from src.service import similarity_service
from src.service import word_embedding_service

import pandas as pd

def run():
    #persistence_service.create_initial_schema()
    #perform_acqusition()

    visitBerlinApi = visitBerlin_search.VisitBerlin()
    print(visitBerlinApi.find('Maxim Gorki Theater'))
    dataframe = visitBerlinApi.perform_visitBerlin_lookup()
    dataframe = dataframe[dataframe['text']!=NaN]
    print("yoo")

    #dataframe = wikipedia_search.perform_wikipedia_lookup()
    weighted_word_matrix = d.determine_weighted_word_embeddings_for_articles(dataframe)

    for index, row in weighted_word_matrix.iterrows():
        
        persistence_service.update_weighted_word2vec_by_id(index, row.get_values().tolist())

    # -- similarity --
    columns = ['id', 'name', 'street_name', 'street_number', 'zip_code', 'long', 'lat', 'opening_hours', 'weighted_word2vec']
    dataframe = pd.DataFrame(persistence_service.get_all_points_of_interests(), columns = columns)[['id', 'name', 'weighted_word2vec']]
    
    model = model_provider.provide_glove_model()
    
    
    userinput = 'art museum'
    cleanedinput = word2vec_preprocess.clean_article(userinput, model)
    
    print(cleanedinput)
    
    userinputarray = word_embedding_service.calculate_mean_vector_of_word_embeddings_for_text(cleanedinput, model)
    
    result = similarity_service.determine_similar_items_with_cosine_similarity(userinputarray, dataframe)
    
    print(result)

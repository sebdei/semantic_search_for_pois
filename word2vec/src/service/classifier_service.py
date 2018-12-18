from .similarity_service import determine_similar_items_with_cosine_similarity
from .word_embedding_service import calculate_mean_vector_of_word_embeddings_for_text

from .persistency import pandas_persistency_service

def classify(userinput):
    userInputMeanWordEmbeddings = calculate_mean_vector_of_word_embeddings_for_text(userinput)
    articles = pandas_persistency_service.get_all_points_of_interests_as_df()
    articles = articles[articles.weighted_word2vec.notnull()]

    cosineSimilarities = determine_similar_items_with_cosine_similarity(userInputMeanWordEmbeddings, articles)

    return cosineSimilarities[:5]

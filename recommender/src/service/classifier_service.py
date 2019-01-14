from .similarity_service import determine_similar_items_with_cosine_similarity
from .word_embedding_service import calculate_mean_vector_of_word_embeddings_for_text

from .persistency import pandas_persistence_service

def classify(userinput):
    userInputMeanWordEmbeddings = calculate_mean_vector_of_word_embeddings_for_text(userinput)
    articles = pandas_persistence_service.get_all_points_of_interests_as_df()
    articles = articles[articles.feature_vector.notnull()]

    cosineSimilarities = determine_similar_items_with_cosine_similarity(userInputMeanWordEmbeddings, articles)

    return cosineSimilarities[:5]
from .model_provider import provide_glove_model
from .similarity_service import determine_similar_items_with_cosine_similarity
from .word_embedding_service import calculate_mean_vector_of_word_embeddings_for_text

from .persistency import pandas_persistency_service

model = provide_glove_model()

def classify(userinput):
    userInputMeanWordEmbeddings = calculate_mean_vector_of_word_embeddings_for_text(userinput, model)
    articles = pandas_persistency_service.get_all_points_of_interests_as_dataframe()
    cosineSimilarities = determine_similar_items_with_cosine_similarity(userInputMeanWordEmbeddings, articles )

    return cosineSimilarities[:5]

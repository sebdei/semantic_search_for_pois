from .model_provider import provide_glove_model
from .similarity_service import determine_similar_items_with_cosine_similarity
from .word_embedding_service import calculate_mean_vector_of_word_embeddings_for_array
from .word_embedding_service import calculate_mean_vector_of_word_embeddings_for_text

model = provide_glove_model()

def classify(userinput):
    userInputMeanWordEmbeddings = calculate_mean_vector_of_word_embeddings_for_array(userinput, model)
    cosineSimilarities = determine_similar_items_with_cosine_similarity(userInputMeanWordEmbeddings, articles)

    return cosineSimilarities

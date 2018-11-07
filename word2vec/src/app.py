from .model_provider import load_model
from .embedding_calculator import calculate_mean_vector_of_word_embeddings_for_text

def run():
    article_string = 'suck it down dude'

    model = load_model()
    mean_vector_of_article = calculate_mean_vector_of_word_embeddings_for_text(article_string, model)

    print(mean_vector_of_article)

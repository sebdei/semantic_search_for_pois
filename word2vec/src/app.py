# from .api import flask

from src.service import word2vec_preprocess
from src.service.word_embedding_service import calculate_mean_vector_of_word_embeddings_for_array
from src.service.model_provider import load_model

def run():
    article1 = {'id': 1, 'text': "adsd sda sdahjbsg churches church In mathematics, matrix multiplication or matrix product is a binary operation that produces a matrix from two matrices with entries in a field, or, more generally, in a ring or even a semiring. The matrix product is designed for representing the composition of linear maps that are represented by matrices. Matrix multiplication is thus a basic tool of linear algebra, and as such has numerous applications in many areas of mathematics, as well as in applied mathematics, statistics, physics, economics, and engineering.[1][2] In more detail, if A is an n × m matrix and B is an m × p matrix, their matrix product AB is an n × p matrix, in which the m entries across a row of A are multiplied with the m entries down a column of B and summed to produce an entry of AB. When two linear maps are represented by matrices, then the matrix product represents the composition of the two maps."}
    article2 = {'id': 3, 'text': "test hello"}
    article3 = {'id': 2, 'text': "fuck you penis"}

    articles = [article1, article2, article3]

    word_embeddings = word2vec_preprocess.determine_weighted_word_embeddings_for_articles(articles)

    print(word_embeddings)
    # print(word_embeddings.loc[3])
    # print(word_embeddings.loc[2])

    # calculate_mean_vector_of_word_embeddings_for_array(features_names, model)
    # flask.bindRoutes()


    # perform_acqusition()
    #
    # article_string = 'The Berlin Wall (German: Berliner Mauer, pronounced [b\u025b\u0281\u02c8li\u02d0n\u0250 \u02c8ma\u028a\u032f\u0250] (listen)) was a guarded concrete barrier that physically and ideologically divided Berlin from 1961 to 1989. Constructed by the German Democratic Republic (GDR, East Germany), starting on 13 August 1961, the Wall cut off (by land) West Berlin from virtually all of surrounding East Germany and East Berlin until government officials opened it in November 1989. Its demolition officially began on 13 June 1990 and finished in 1992. The barrier included guard towers placed along large concrete walls, accompanied by a wide area (later known as the \"death strip\") that contained anti-vehicle trenches, \"fakir beds\" and other defenses.'
    # mean_vector_of_article = calculate_mean_vector_of_word_embeddings_for_text(article_string, model)
    #
    # article_similarity = determine_similar_items_with_cosine_similarity(mean_vector_of_article, articles)
    # print(article_similarity)

import numpy as np
from scipy.spatial import distance
import random

SIMILARITY = 'similarity'

def calculate_cosine_similarity_for_article(compare_vector, article_vector):
    cosine_distance = distance.cosine(compare_vector, article_vector)
    return 1 - cosine_distance

def determine_similar_items_with_cosine_similarity(compare_vector, articles_data_frame):
    articles_data_frame['similarity'] = articles_data_frame.apply(lambda row: calculate_cosine_similarity_for_article(compare_vector, row['weighted_word2vec']), axis = 1)

    return articles_data_frame.sort_values(by=['similarity'], ascending=False)

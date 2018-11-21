from scipy.spatial import distance

SIMILARITY = 'similarity'

def calculate_cosine_similarity_for_article(article, compare_vector):
    cosine_distance = distance.cosine(compare_vector, article['word2vec_vector'])
    result = {
        'id': article['id'],
        SIMILARITY: 1 - cosine_distance
    }

    return result

def determine_similar_items_with_cosine_similarity(compare_vector, articles):
    unsorted_list_of_articles_with_similarity = [calculate_cosine_similarity_for_article(article, compare_vector) for article in articles]
    result = sorted(unsorted_list_of_articles_with_similarity, key=lambda key: key[SIMILARITY], reverse=True)

    return result

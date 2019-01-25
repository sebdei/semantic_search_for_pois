from .similarity_service import determine_similar_items_with_cosine_similarity
from .word_embedding_service import calculate_mean_vector_of_word_embeddings_for_text
from src.service.collaborative_filtering import filter_weather, filter_location

from src.service.persistency import pandas_persistence_service
from src.service.persistency import persistence_service


def do_content_based_recommendation(user_id):
    user_input_record = persistence_service.get_user_input_for_id(user_id)
    if not user_input_record:
        return pandas_persistence_service.get_all_points_of_interests_as_df().sample(10)
    else:
        user_input = user_input_record[1]

        user_input_mean_word_embeddings = calculate_mean_vector_of_word_embeddings_for_text(userinput)
        articles = pandas_persistence_service.get_all_points_of_interests_as_df()
        articles = articles[articles.feature_vector.notnull()]

        cosineSimilarities_df = determine_similar_items_with_cosine_similarity(user_input_mean_word_embeddings, articles)

        return cosineSimilarities_df[:10]

def do_collaborative_filter_recommendation(user_id, user_lat, user_long, radius, consider_weather, force_bad_weather):
    recommendations = user2user_recommender.getRecommendationsForUser(user_id)

    users_currentLocation = {'lat':user_lat, 'lng':user_long}
    recommendations = filter_weather.filterOnWeather(users_currentLocation, recommendations, consider_weather, force_bad_weather)
    recommendations = filter_location.filterOnLocation(users_currentLocation, recommendations, radius)

    return recommendations.to_json(orient='records')

def do_recommendation_for_user(user_id, user_lat, user_long, radius, consider_weather, force_bad_weather):
    ratings_count = count_recommendations_by_user(user_id)

    if ratings_count > 3 and user2user_recommender.eval(user_id) < 0.001:
        return do_collaborative_filter_recommendation(user_id, user_lat, user_long, radius, consider_weather, force_bad_weather)
    else:
        return do_content_based_recommendation(user_id)

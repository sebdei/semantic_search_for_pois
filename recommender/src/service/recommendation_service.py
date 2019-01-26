from .similarity_service import determine_similar_items_with_cosine_similarity
from .word_embedding_service import calculate_mean_vector_of_word_embeddings_for_text
from src.service.collaborative_filtering import filter_weather, filter_location, user2user_recommender

from src.service.persistency import pandas_persistence_service
from src.service.persistency import persistence_service

def content_based_recommendation(user_id):
    user_input_record = persistence_service.get_user_input_for_id(user_id)
    if not user_input_record:
        # random recommendation to display at least something
        print('Did not find user input! Returning random POIs.')
        return pandas_persistence_service.get_all_points_of_interests_as_df().sample(10)
    else:
        user_input = user_input_record[1]

        user_input_mean_word_embeddings = calculate_mean_vector_of_word_embeddings_for_text(user_input)
        articles = pandas_persistence_service.get_all_points_of_interests_as_df()
        articles = articles[articles.feature_vector.notnull()]

        cos_similarities_df = determine_similar_items_with_cosine_similarity(user_input_mean_word_embeddings, articles)

        print(cos_similarities_df)
        return cos_similarities_df[:10]

def collaborative_filter_recommendation(user_id, user_lat, user_long, radius, consider_weather, force_bad_weather):
    recommendations = user2user_recommender.get_recommendations_for_user(int(user_id))

    user_location = {'lat':float(user_lat), 'lng':float(user_long)}
    recommendations = filter_weather.filter_by_weather(user_location, recommendations, consider_weather, force_bad_weather)
    recommendations = filter_location.filter_by_location(user_location, recommendations, float(radius))

    print(recommendations)
    return recommendations

def recommendation_for_user(user_id, user_lat, user_long, radius, consider_weather, force_bad_weather):
    ratings_count = persistence_service.count_recommendations_by_user(user_id)

    # only calculate rmse when required
    if ratings_count > 3:
        print('Calculating RMSE for collaborative filtering recommendations')
        rmse = user2user_recommender.eval(int(user_id))
        print('RMSE is %f' % (rmse))

    if ratings_count > 3 and rmse < 0.01:
        print('Collaborative filtering for user with ID %s with RMSE %f and %d ratings' % (user_id, rmse, ratings_count))
        return collaborative_filter_recommendation(user_id, user_lat, user_long, radius, consider_weather, force_bad_weather)
    else:
        print('Content based filtering for user with ID %s' % (user_id))
        return content_based_recommendation(user_id)

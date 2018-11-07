import numpy as np

def get_init_sum_vector(model):
    first_element_value_in_model = next(iter(model.values()))
    number_of_dimensions = len(first_element_value_in_model)

    return np.zeros(number_of_dimensions)

# assumes, that text is already cleaned
def calculate_mean_vector_of_word_embeddings_for_text(article_string, model):
    words_array = article_string.split()
    return calculate_mean_vector_of_word_embeddings_for_array(words_array, model)

def calculate_mean_vector_of_word_embeddings_for_array(words_array, model):
    sum_vector = get_init_sum_vector(model)
    number_of_words = len(words_array)
    words_not_found_in_model = []

    if (number_of_words > 0 ):
        for word in words_array:
            lower_case_word = word.lower()

            try:
                word_vector = model[lower_case_word]
                sum_vector = np.add(sum_vector, word_vector)
            except KeyError:
                words_not_found_in_model.append(lower_case_word)
                number_of_words -= 1

        if (len(words_not_found_in_model) > 0):
            print('The following words were not found in model:')
            print(words_not_found_in_model)

        mean_vector = np.divide(sum_vector, number_of_words)

        return mean_vector

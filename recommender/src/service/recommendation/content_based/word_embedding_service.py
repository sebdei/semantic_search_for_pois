import numpy as np
import re
import nltk

nltk.download('stopwords')
nltk.download('wordnet') # lemmatization

from src.service import model_provider

glove_model = model_provider.provide_glove_model()

def clean_userinput(userinput):
    stripped_userinput = re.sub('[-!$%^&*()_+|~=`{}\[\]:\";\'<>?,.\/\d]', ' ', userinput)
    word_list = stripped_userinput.split()
    word_list_lowercase = [ word.lower() for word in word_list ]

    wn = nltk.WordNetLemmatizer()
    stopwords = nltk.corpus.stopwords.words('english')

    valid_words = []
    invalid_words = []
    for word in word_list_lowercase:
        if word not in stopwords:
            lemmatized_word = wn.lemmatize(word)

            if lemmatized_word in glove_model:
                valid_words.append(lemmatized_word)
            else:
                invalid_words.append(lemmatized_word)

    if (len(invalid_words) > 0 ):
        print('the following words were not found in model:')
        print(invalid_words)

    return valid_words

def get_init_sum_vector():
    first_element_value_in_model = next(iter(glove_model.values()))
    number_of_dimensions = len(first_element_value_in_model)

    return np.zeros(number_of_dimensions)

def calculate_mean_vector_of_word_embeddings_for_array(words_array):
    sum_vector = get_init_sum_vector()
    number_of_words = len(words_array)
    words_not_found_in_model = []

    if (number_of_words > 0 ):
        for word in words_array:
            word_vector = glove_model.get(word)
            sum_vector = np.add(sum_vector, word_vector)

        mean_vector = np.divide(sum_vector, number_of_words)

        return mean_vector

def calculate_mean_vector_of_word_embeddings_for_text(userinput):
    valid_words = clean_userinput(userinput)

    mean_vector = calculate_mean_vector_of_word_embeddings_for_array(valid_words)

    return mean_vector

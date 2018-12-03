import re
import pandas as pd
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from .model_provider import provide_glove_model

nltk.download('wordnet') #lemmatizer

def clean_article(article, glove_model):
    stripped_article = re.sub('[-!$%^&*()_+|~=`{}\[\]:\";\'<>?,.\/\d]', ' ', article)
    word_list = stripped_article.split()
    word_list_lowercase = [word.lower() for word in word_list]

    wn = nltk.WordNetLemmatizer()
    stopwords = nltk.corpus.stopwords.words('english')

    valid_words = []
    for word in word_list_lowercase:
        if word not in stopwords:
            lemmatized_word = wn.lemmatize(word)

            if glove_model.get(lemmatized_word) is not None:
                valid_words.append(lemmatized_word)

    return ' '.join(valid_words)

def determine_tf_idfs_for_list_of_articles(articles, glove_model):
    cleaned_articles = [clean_article(article['text'], glove_model) for article in articles]

    tf_idf_vectorizer = TfidfVectorizer()
    tf_idf_vector = tf_idf_vectorizer.fit_transform(cleaned_articles)

    result = pd.DataFrame(tf_idf_vector.toarray(), index = [article['id'] for article in articles])
    result.columns = tf_idf_vectorizer.get_feature_names()

    return result

def determine_word_embeddings_for_feature_vector(feature_vector, glove_model):
    return pd.DataFrame([glove_model[word] for word in feature_vector], index = feature_vector)

def determine_weighted_word_embeddings_for_articles(articles):
    glove_model = provide_glove_model()

    tf_idf_matrix = determine_tf_idfs_for_list_of_articles(articles, glove_model)

    feature_vector = tf_idf_matrix.columns.values
    word_embedding_matrix =  determine_word_embeddings_for_feature_vector(feature_vector, glove_model)

    return tf_idf_matrix.dot(word_embedding_matrix)

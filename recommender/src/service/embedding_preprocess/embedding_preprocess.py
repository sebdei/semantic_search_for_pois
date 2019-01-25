import re
import pandas as pd
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from src.service.persistency import pandas_persistence_service as pps
from src.service.persistency import persistence_service as ps
from src.service.model_provider import provide_glove_model
from src.service.persistency.data_model import *

from .wikipedia_search import execute_wikipedia_query
from .visit_berlin_search import execute_visitberlin_query

nltk.download('stopwords')
nltk.download('wordnet') # lemmatization

def clean_article(article, glove_model):
    stripped_article = re.sub(r'[-!$%^&*()_+|~=`{}\[\]:\";\'<>?,.\/\d]', ' ', article)
    word_list = stripped_article.split()
    word_list_lowercase = [ word.lower() for word in word_list ]

    wn = nltk.WordNetLemmatizer()
    stopwords = nltk.corpus.stopwords.words('english')

    valid_words = []
    for word in word_list_lowercase:
        if word not in stopwords:
            lemmatized_word = wn.lemmatize(word)

            if lemmatized_word in glove_model:
                valid_words.append(lemmatized_word)

    return ' '.join(valid_words)

def determine_tf_idfs_for_list_of_articles(articles, glove_model):
    cleaned_articles = articles.apply(lambda row: clean_article(row['text'], glove_model), axis = 1).values

    tf_idf_vectorizer = TfidfVectorizer()
    tf_idf_vector = tf_idf_vectorizer.fit_transform(cleaned_articles)

    result = pd.DataFrame(tf_idf_vector.toarray(), index = articles.index.values)
    result.columns = tf_idf_vectorizer.get_feature_names()

    return result

def determine_word_embeddings_for_feature_vector(feature_vector, glove_model):
    return pd.DataFrame([ glove_model.get(word, [0] * len(glove_model['.'])) for word in feature_vector ], index = feature_vector)

def determine_weighted_word_embeddings_for_articles(articles):
    glove_model = provide_glove_model()

    tf_idf_matrix = determine_tf_idfs_for_list_of_articles(articles, glove_model)

    feature_vector = tf_idf_matrix.columns.values
    word_embedding_matrix =  determine_word_embeddings_for_feature_vector(feature_vector, glove_model)

    return tf_idf_matrix.dot(word_embedding_matrix)

def init_word_embeddings_calculation_for_articles():
    execute_visitberlin_queries()
    execute_wikipedia_queries()

    text_df = create_integrated_text_df()

    weighted_word_matrix = determine_weighted_word_embeddings_for_articles(text_df)

    for index, row in weighted_word_matrix.iterrows():
        ps.update_feature_vector_by_id(index, row.get_values().tolist())

def execute_wikipedia_queries():
    df = pps.get_all_points_of_interests_as_df()
    already_queried_tuples = ps.get_queried_pois_wikipedia()
    already_queries_ids = [i[0] for i in already_queried_tuples]

    for index, row in df.iterrows():
        if index not in already_queries_ids:
            wiki_title, wiki_url, wiki_text = execute_wikipedia_query(row['name'])
            ps.insert_query_data_wikipedia(index, wiki_title, wiki_url, wiki_text)

def execute_visitberlin_queries():
    df = pps.get_all_points_of_interests_as_df()
    already_queried_tuples = ps.get_queried_pois_visitberlin()
    already_queries_ids = [i[0] for i in already_queried_tuples]

    for index, row in df.iterrows():
        if index not in already_queries_ids:
            vb_title, vb_url, vb_text = execute_visitberlin_query(row['name'])
            ps.insert_query_data_visitberlin(index, vb_title, vb_url, vb_text)

def create_integrated_text_df():
    wikipedia_queries = pps.get_all_wiki_data_as_df()
    visitberlin_queries = pps.get_all_visitberlin_data_as_df()

    text_df = pd.DataFrame(columns = [POI_ID, 'text']).set_index(POI_ID)

    for index, row in wikipedia_queries.iterrows():
        if row[WIKI_TEXT] is not None and row[WIKI_TEXT] != '':
            text_df.loc[index] = [row[WIKI_TEXT]]

    for index, row in visitberlin_queries.iterrows():
        if row[VISITBERLIN_TEXT] is not None and row[VISITBERLIN_TEXT] != '':
            if index not in text_df.index:
                text_df.loc[index] = [row[VISITBERLIN_TEXT]]
            else:
                text_df.loc[index] = row[VISITBERLIN_TEXT] + ' ' + text_df.loc[index]['text']

    print('Have source text for {} POIs in total'.format(len(text_df)))

    return text_df

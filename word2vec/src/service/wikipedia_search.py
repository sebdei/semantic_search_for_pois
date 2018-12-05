import wikipedia
import string
import pandas as pd

from .persistence_service import get_all_points_of_interests

def clean_query(query):
    exclude = set(string.punctuation)
    no_punctuation = ''.join(ch for ch in query if ch not in exclude)

    return no_punctuation

def get_wikipedia_text(query):
    search_query = clean_query(query)
    print('lookup wikipedia for searchquery >>' + search_query + '<<')

    results_with_berlin = wikipedia.search(search_query + " Berlin")
    results_without_berlin = wikipedia.search(search_query)

    if len(results_with_berlin) == 0 and len(results_without_berlin) == 0:
        # do further search
        wiki_page = "Berlin" # dummy for now
    elif len(results_with_berlin) == 0:
        wiki_page = results_without_berlin[0]
    elif len(results_without_berlin) == 0:
        wiki_page = results_with_berlin[0]
    else:
        # prefer result with "Berlin"
        wiki_page = results_with_berlin[0]

    wiki_text = wikipedia.page(title = wiki_page).content

    return wiki_text

def perform_wikipedia_lookup():
    columns = ['id', 'name', 'street_name', 'street_number', 'zip_code', 'long', 'lat', 'opening_hours', 'word2vec']
    dataframe = pd.DataFrame(get_all_points_of_interests(), columns = columns)[['id', 'name']]

    dataframe['text'] = dataframe.apply(lambda row: get_wikipedia_text(row['name']), axis = 1)

    return dataframe

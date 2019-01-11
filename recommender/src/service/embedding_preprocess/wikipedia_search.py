import wikipedia
import string
import pandas as pd
import re
from py_stringmatching import SmithWaterman

sw = SmithWaterman()

def clean_query(query):
    exclude = set(string.punctuation)
    no_punctuation = ''.join((ch if ch not in exclude else ' ') for ch in query)
    no_punctuation = re.sub(r'\s+', ' ', no_punctuation)
    return no_punctuation

def get_wikipedia_text(query):
    search_query = clean_query(query)
    print('lookup wikipedia for searchquery >>' + search_query + '<<')

    wiki_titles = wikipedia.search(search_query)

    foundArticle = False
    wiki_text = ''
    wiki_title = ''

    while not foundArticle and len(wiki_titles) > 0:
        wiki_title = wiki_titles.pop(0) # take first element
        sim = sw.get_raw_score(wiki_title, query) / max(len(wiki_title), len(query))
        if sim < 0.5: # low sim --> probably a false positive --> continue
            continue
        else:
            try:
                wiki_page = wikipedia.page(title = wiki_title)
            except Exception as e:
                print('there was an error fetching a page:', wiki_title, e)
                continue
            
            wiki_text = wiki_page.content
            foundArticle = True

    if wiki_text == '':
        print('Found none.')
    else:
        print('Found ' + wiki_title)

    return wiki_text

def perform_wikipedia_lookup(dataframe):
    dataframe['text'] = dataframe.apply(lambda row: get_wikipedia_text(row['name']), axis = 1)

    dataframe_with_texts = dataframe[dataframe.text != '']

    return dataframe_with_texts

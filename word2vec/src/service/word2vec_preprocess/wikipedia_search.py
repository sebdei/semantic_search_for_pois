import wikipedia
import string
import pandas as pd
import re

def clean_query(query):
    exclude = set(string.punctuation)
    no_punctuation = ''.join((ch if ch not in exclude else ' ') for ch in query)
    no_punctuation = re.sub(r'\s+', ' ', no_punctuation)
    return no_punctuation

def get_wikipedia_text(query):
    search_query = clean_query(query)
    print('lookup wikipedia for searchquery >>' + search_query + '<<')

    results_with_berlin = wikipedia.search(search_query + " Berlin")
    results_without_berlin = wikipedia.search(search_query)

    wiki_titles = []
    wiki_titles.extend(results_with_berlin)
    wiki_titles.extend(results_without_berlin)

    foundArticle = False
    wiki_text = ''
    wiki_title = ''

    while not foundArticle and len(wiki_titles) > 0:
        wiki_title = wiki_titles.pop(0) # take first element
        if wiki_title == 'Berlin':
            continue
        else:
            wiki_page = wikipedia.page(title = wiki_title)

            exclude_people_regex = re.compile(r'\d+ births|Year of birth missing .*')
            category_matches = [cat for cat in wiki_page.categories if len(exclude_people_regex.findall(cat)) > 0]

            if len(category_matches) == 0:
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

import wikipedia
import string

def clean_query(query):
    exclude = set(string.punctuation)
    no_punctuation = ''.join(ch for ch in query if ch not in exclude)
    return no_punctuation

def get_wikipedia_text(query):
    search_query = clean_query(query)
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
    
    wiki_text = wikipedia.page(title=wiki_page).content
    print(query + "\n\t" + wiki_page)
    
    return (wiki_page, wiki_text)

# names = open("names.txt")
# for line in names.read().split('\n'):
#     print(get_wikipedia_text(line))
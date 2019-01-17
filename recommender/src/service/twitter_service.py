import tweepy #pip install tweepy

consumer_key= '5Y1SpW5U6R2GgRkfoWqgPOoyn'
consumer_secret= 'HelZN5y2bBT9UOWdubeJrcfazkHchCiTEng2nL0GjxarGCNR8X'
access_token= '1070306404072869888-4xAMzTS4xlUupsvdnx5Nt22oHWmOiW'
access_token_secret= 'TqeCMspoajmXngAXBJwSCi17Olh1cbjKfVTuBh5l9Tosj'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
q='l=en'

def get_recent_tweets_of_user_by_id(id):
    tweet_list=list()
    user_timeline=api.user_timeline(id)
    for i, val in enumerate(user_timeline):
        tweet_list.append(user_timeline[i].text)
    return tweet_list

def search_for_user_ids(q):
    id_list=list()
    complete_users= (api.search_users(q))
    for i, val in enumerate(complete_users):
        id_list.append([complete_users[i].id, complete_users[i].name, complete_users[i].screen_name])
    return id_list

def get_recent_tweets_of_user_by_name(name):
    tweet_list=list()
    user_timeline=api.user_timeline(name)
    for i, val in enumerate(user_timeline):
        tweet_list.append(user_timeline[i].text)
    return tweet_list

import tweepy

access_token = '1070306404072869888-4xAMzTS4xlUupsvdnx5Nt22oHWmOiW'
access_token_secret = 'TqeCMspoajmXngAXBJwSCi17Olh1cbjKfVTuBh5l9Tosj'
consumer_key = '5Y1SpW5U6R2GgRkfoWqgPOoyn'
consumer_secret = 'HelZN5y2bBT9UOWdubeJrcfazkHchCiTEng2nL0GjxarGCNR8X'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_recent_tweets_of_user_by_name(name):
    tweet_list = list()
    user_timeline = api.user_timeline(name, tweet_mode='extended')

    for i, val in enumerate(user_timeline):
        tweet_list.append(user_timeline[i].full_text)

    return tweet_list

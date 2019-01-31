import tweepy

access_token = 'TWITTER_ACCESS_TOKEN'
access_token_secret = 'TWITTER_ACCESS_TOKEN_SECRET'
consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_recent_tweets_of_user_by_name(name):
    tweet_list = list()
    user_timeline = api.user_timeline(name, tweet_mode='extended')

    for i, val in enumerate(user_timeline):
        tweet_list.append(user_timeline[i].full_text)

    return tweet_list

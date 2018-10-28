# Let's get this party started!

import falcon
from falcon_auth import FalconAuthMiddleware, JWTAuthBackend
import json
from utils import TwitterClient
import ast
import re

class SearchTwitter(object):
    "class responsible for fetchng data from twitter and genrating sentiment analysis"
    def on_post(self,req,resp):
        data_body=str(req.stream.read().decode('utf-8'))
        data_dict=ast.literal_eval(re.sub('[\n|\r| +|\t]',' ',data_body))
        Query =data_dict['query']
        Twee = TwitterClient()
        tweets = Twee.get_tweets(query = Query, count = 800)
        ptweets = [tweet for tweet in tweets if tweet['sentiment'][0] == 'positive']
        ntweets = [tweet for tweet in tweets if tweet['sentiment'][0] == 'negative']
        PTP=100*(len(ptweets)/len(tweets))
        NTP=100*(len(ntweets)/len(tweets))
        NTWP=100*((len(tweets) - len(ntweets) - len(ptweets))/len(tweets))
        resp.status=falcon.HTTP_200
        resp.body=json.dumps({'PTP':str(PTP),'NTP':str(NTP),'NTWP':str(NTWP),
                               'ptweets':ptweets,'ntweets':ntweets,'tweets':tweets})

class AnalyzeTweets(object):
    "class responsible for fetchng data from twitter and genrating sentiment analysis"
    def on_post(self,req,resp):
        data_body=str(req.stream.read().decode('utf-8'))
        data_dict=ast.literal_eval(re.sub('[\n|\r| +|\t]',' ',data_body))
        Query =data_dict['query']
        Twee = TwitterClient()
        tweets = Twee.get_tweets(query = Query, count = 800)
        ptweets = sum([tweet['sentiment'][0] == 'positive' for tweet in tweets])
        ntweets = sum([tweet['sentiment'][0] == 'negative' for tweet in tweets])
        PTP=100*(ptweets/len(tweets))
        NTP=100*(ntweets/len(tweets))
        NTWP=100*((len(tweets) - ntweets - ptweets)/len(tweets))
        resp.status=falcon.HTTP_200
        resp.body=json.dumps({'PTP':str(PTP),'NTP':str(NTP),'NTWP':str(NTWP)})

class GetSent(object):
    "class responsible for getting sentiments of a sentence"
    def on_post(self,req,resp):
        data_body=str(req.stream.read().decode('utf-8'))
        data_dict=ast.literal_eval(re.sub('[\n|\r| +|\t]',' ',data_body))
        Tweet =data_dict['tweet']
        Twee = TwitterClient()
        sentiment,polarity,cleaned_text = Twee.get_tweet_sentiment(tweet = Tweet)

        resp.status=falcon.HTTP_200
        resp.body=json.dumps({'sentiment':sentiment,'polarity':polarity,'cleaned_text':cleaned_text})

APP = falcon.API(middleware=[])

# things will handle all requests to the '/things' URL path
APP.add_route('/api/SearchTwitter', SearchTwitter())
APP.add_route('/api/GetSent',GetSent())
APP.add_route('/api/AnalyzeTweets',AnalyzeTweets())



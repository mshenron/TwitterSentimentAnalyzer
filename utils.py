import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    EMOTICONS = { # (facial expression, sentiment)-keys
    (" ~love~ " , +1.00): set(("<3", "♥")),
    (" ~grin~ " , +1.00): set((">:D", ":-D", ":D", "=-D", "=D", "X-D", "x-D", "XD", "xD", "8-D")),
    (" ~taunt~ ", +0.75): set((">:P", ":-P", ":P", ":-p", ":p", ":-b", ":b", ":c)", ":o)", ":^)")),
    (" ~smile~ ", +0.50): set((">:)", ":-)", ":)", "=)", "=]", ":]", ":}", ":>", ":3", "8)", "8-)")),
    (" ~wink~ " , +0.25): set((">;]", ";-)", ";)", ";-]", ";]", ";D", ";^)", "*-)", "*)")),
    (" ~gasp~ " , +0.05): set((">:o", ":-O", ":O", ":o", ":-o", "o_O", "o.O", "°O°", "°o°")),
    (" ~worry~ ", -0.25): set((">:/",  ":-/", ":/", ":\\", ">:\\", ":-.", ":-s", ":s", ":S", ":-S", ">.>")),
    (" ~frown~ ", -0.75): set((">:[", ":-(", ":(", "=(", ":-[", ":[", ":{", ":-<", ":c", ":-c", "=/")),
    (" ~cry~ "  , -1.00): set((":'(", ":'''(", ";'("))}
    REV_EMOTICONS = { # (facial expression, sentiment)-keys
    "~love~":"<3",
    "~grin~": ">:D", 
    "~taunt~":">:P",
    "~smile~": ">:)",
    "~wink~" : ">;]",
    "~gasp~" : ">:o",
    "~worry~": ">:/",
    "~frown~": ">:[",
    "~cry~"  : ":'("}

    RE_EMOTICONS = {k[0]:[r" ?".join([re.escape(each) for each in e]) for e in v] for k,v in EMOTICONS.items()}
    RE_EMOTICONS = {k:re.compile(r"(%s)($|\s)" % "|".join(e)) for k,e in RE_EMOTICONS.items()}

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key='#YOUR CUSTOMER KEY HERE'
        consumer_secret='#YOUR CUSTOMER SECRET HERE'
        access_token='#YOUR ACCESS TOKEN HERE'
        access_token_secret='YOUR ACCESS TOKEN SECRET HERE'


        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        for k,v in self.RE_EMOTICONS.items():
            tweet=re.sub(v,k,tweet)
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z~ \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        cleaned_tweet=self.clean_tweet(tweet)
        for k,v in self.REV_EMOTICONS.items():
            tweet=re.sub(k,v,tweet)
        #print(tweet)
        analysis = TextBlob(cleaned_tweet)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive',analysis.sentiment.polarity,cleaned_tweet
        elif analysis.sentiment.polarity == 0:
            return 'neutral',analysis.sentiment.polarity,cleaned_tweet
        else:
            return 'negative',analysis.sentiment.polarity,cleaned_tweet
 
    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

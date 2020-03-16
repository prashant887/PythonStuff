from __future__ import unicode_literals
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy as tw
import json
import time

with open('C:\\Users\\Owner\\Documents\\PythonTwitterStream\\twitterauthcredintails.json') as json_file:
    data = json.load(json_file)

consumer_key = data['consumer_key']
consumer_secret = data['consumer_secret']
access_token = data['access_token']
access_token_secret = data['access_token_secret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


print('Application Started')

search_word = 'COVID'
date_since = '2020-03-10'
tweets = tw.Cursor(api.search, q=search_word, lang="en", since=date_since).items(5)

json_message_list = []

for tweet in tweets:
    print(tweet.text)
    json_message_list.append(tweet)

print("All Tweets")
print(json_message_list)

print('Application Finished')

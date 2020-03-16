from __future__ import unicode_literals
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import tweepy as tw
import json
import time

with open('C:\\Users\\Owner\\Documents\\PythonTwitterStream\\twitterauthcredintails.json') as json_file:
    data = json.load(json_file)

consumer_key = data['consumer_key']
consumer_secret = data['consumer_secret']
access_token = data['access_token']
access_token_secret = data['access_token_secret']


##This is a class that recives and prints tweet to console

class StreamListenerClass(StreamListener):
    def on_data(self, tweet_data):
        tweet_data_json = json.loads(tweet_data)
        #print(tweet_data_json)

        tweet_msg_text = '"' + tweet_data_json["text"].replace("\n", " ") + '"'
        part_of_tweet_msg_lst = [str(tweet_data_json["id"]), tweet_data_json["user"]["screen_name"],
                                 tweet_data_json["created_at"],
                                 str(tweet_data_json["user"]["followers_count"]), tweet_msg_text]
        part_of_tweet_msg = "|".join(part_of_tweet_msg_lst)
        print(part_of_tweet_msg)

        return True

    def on_error(self, status):
        print("Print On Error Function: " + status)


if __name__ == '__main__':
    print('\n Tweet Streaming Application Started \n')
    dmStreamListiner = StreamListenerClass()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth)
    stream = Stream(auth, dmStreamListiner)
    print(stream.verify)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    # Below line will filter Twiteer stream based on keywords Inida , Karnataka , Bangalore
    try:
        stream.filter(track=['India', 'Karnataka', 'Bangalore', 'COVID'])
    except:
        pass

    print("\n Application Ended \n")

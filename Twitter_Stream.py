from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import sqlite3
from unidecode import unidecode
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

analyzer=SentimentIntensityAnalyzer()

conn=sqlite3.connect('twitter.db')
c=conn.cursor()

#Creates a table with 3 collumns 
def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL,tweet TEXT,sentiment REAL)")
	conn.commit()

create_table()

ckey='##############'
csecret='###########################'
atoken='#################################'
asecret='#####################################'

#Streams and collects data from Twitter
class listener(StreamListener):
	def on_data(self,data):
		try:
			data=json.loads(data)
			tweet=unidecode(data['text'])
			time_ms=data['timestamp_ms']
			analysis=TextBlob(tweet)
			sentiment=analysis.sentiment.polarity
			print(time_ms,tweet,sentiment)
			c.execute("INSERT INTO sentiment(unix,tweet,sentiment) VALUES (?,?,?)", (time_ms,tweet,sentiment))
			conn.commit()
		except KeyError as e:
			print(str(e))
		return(True)

	def on_error(self,status):
		print(status)

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
twitterStream=Stream(auth,listener())
twitterStream.filter(track=["a","e","i","o","u"]) #Tracking all tweets

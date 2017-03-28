from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

ckey = ' ' #your consumer key
csecret = ' ' #your consumer secret
atoken = ' ' #your access token
asecret = ' ' #your access secret

class listener(StreamListener):

    def on_data(self, data):
        try:
        
		#print data
		tweet = data.split(',"text":"')[1].split('","source')[0] #[1] as we want the right side not the left side of this split
		print tweet
		
		saveThis = str(time.time()) + '::' +tweet #to get unix time
		saveFile = open('twitDB2.txt','a')
		saveFile.write(saveThis)
		saveFile.write('\n')
		saveFile.close()
        	return True
	except BaseException,e:
		print 'failed on data,',str(e)
		time.sleep(5)
    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["text"]) #replace text with entity related to which tweets are to be extracted. In my case, I used "Narendra Modi"

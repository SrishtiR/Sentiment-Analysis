import sqlite3
import time
import csv
conn = sqlite3.connect('KB.db')
c = conn.cursor()

negativeWords = []
positiveWords = []
sql = "SELECT * FROM wordVals WHERE value =?"
def loadWordArrays():
	for negRow in c.execute(sql,[(-1)]):
		negativeWords.append(negRow[0])
	print 'neg words loaded'
	
	for posRow in c.execute(sql,[(1)]):
		positiveWords.append(posRow[0])
	print 'pos word loaded'
	
def testSentiment():
	z = csv.writer(open("TweetSentiment6.csv", "w"))
	z.writerow(["ID","Polarity"])

	i = 1
	f = open('twitsample.txt','r')
	data = f.read()
	k = '####################################################################################################'
	text = data.decode("utf8")
	tweets = text.split(k) 
	for tweet in tweets:
	
		sentCounter = 0
	
		for eachPosWord in positiveWords:
			if eachPosWord in tweet:
				sentCounter +=1
				#print eachPosWord
		for eachNegWord in negativeWords:
			if eachNegWord in tweet:
				sentCounter -=1
				#print eachNegWord
		
		if sentCounter >0:
			print "Positive"
			#z.writerow([i,"Positive"])
			
		if sentCounter <0:
			print "Negetive"
			#z.writerow([i,"Negative"])
		if sentCounter ==0:
			print "Neutral"
			#z.writerow([i,"Neutral"])
		
		i = i+1
loadWordArrays()
testSentiment()

#NER,storage of RSS feeds on huffingtonpost.com


import sqlite3
import time
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import datetime
import nltk


cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0')]
 
conn = sqlite3.connect('KB.db')
c = conn.cursor()
#c.execute("CREATE TABLE Hello (unix REAL,dateStamp TEXT,namedEntity TEXT,relatedWord TEXT)")

visitedLinks = []

def processor(data):
	try:
		tokenized = nltk.word_tokenize(data)
		tagged = nltk.pos_tag(tokenized)
		namedEnt = nltk.ne_chunk(tagged,binary = True)
		
		entities = re.findall(r'NE\s(.*?)/',str(namedEnt))
		descriptives = re.findall(r'\(\'(\w*)\',\s\'JJ\w?\'',str(tagged))
		if len(entities) > 1:
			pass
		elif len(entities) == 0:
			pass
		else:
			print 'Named: ',entities[0]  
			print 'Descriptions: '
			for eachDesc in descriptives:
				print eachDesc	
				currentTime =time.time() #our unix time
				dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S') #converts unix stamp to datestamp
				namedEntity = entities[0]
				relatedWord = eachDesc
				
				c.execute("INSERT INTO Hello (unix,dateStamp,namedEntity,relatedWord) VALUES (?,?,?,?)",(currentTime,dateStamp,namedEntity,relatedWord))
				conn.commit() #database might get locked up or corrupted
					
	except Exception,e:
		print 'failed in the first try of processor'
		print str(e)


	
def huffingtonRSSvisit():
	try:
		page = 'http://www.huffingtonpost.com/feeds/index.xml'
		sourceCode = opener.open(page).read()
		try:
			links = re.findall(r'<link>(.*?)</link>',sourceCode)
			
			for link in links:
				if 'http' in link:
					visitedLinks.append(link)
					print 'visiting the link'
					print '#########'
					linkSource = opener.open(link).read()
					linesOfInterest = re.findall(r'<p>(.*?)</p>',str(linkSource))
					print 'Content:'
					for eachLine in linesOfInterest:
	 					if '<img width' in eachLine:
	 						pass
	 					elif '<a href=' in eachLine:
	 						pass
	 					else:
	 						processor(eachLine)
	 				time.sleep(5)
				
				elif link in visitedLinks:
					print 'link already visited'
				else:
					pass
			 
			
		except Exception,e:
			print 'failed 2nd loop of huffington RSS'
			print str(e)
	
	except Exception,e:
		print 'failed main loop of huffington RSS'
		print str(e)
	
while 1<2 :
	huffingtonRSSvisit()

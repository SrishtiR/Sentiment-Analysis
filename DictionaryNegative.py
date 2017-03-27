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



startingWord = 'negative'
startingWordVal = -1

#c.execute("INSERT INTO wordVals (word,value) VALUES (?,?)",(startingWord,startingWordVal))
 
synArray = [] #empty array

def main():
	try:
		page = 'http://thesaurus.com/browse/'+startingWord+'?s=t'
		sourceCode = opener.open(page).read()
		print sourceCode
		try:
			synoNym = sourceCode.split('Synonyms <span>for negative</span>')#creates an array or table with variable number of entries 

			x=1
			while x < len(synoNym):
				try :
					synoNymSplit = synoNym[x].split ('<div class="synonyms-horizontal-divider"></div>')[0]
					synoNyms = re.findall(r'\"text">(\w*?)</span>',synoNymSplit)
									
					print synoNyms
					for eachSyn in synoNyms:
						query = "SELECT * FROM wordVals WHERE word =?"
						c.execute(query, [(eachSyn)]) #will return either something or nothing
						data = c.fetchone() #to find if next synonym to the cursor. Either none or some		 
						if data is None:
							print 'not here yet'
							c.execute("INSERT INTO wordVals (word,value) VALUES (?,?)",(eachSyn,startingWordVal))
							conn.commit()
						else:
							print 'Word already here!'
				except Exception,e :
					print str(e)
					print 'failed in 3rd try'
				x+=1
		
		except Exception,e:
			print str(e)
			print 'failed in the 2nd try'
	
	
	except Exception,e:
		print str(e)
		print 'failed in the main loop'
		
main()

c.execute("INSERT INTO doneSynonyms(word,value) VALUES (?,?)",(startingWord,startingWordVal))
conn.commit()

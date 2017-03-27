import sqlite3
import nltk
import re
conn = sqlite3.connect('KB.db')
conn.text_factory = str
c = conn.cursor()
Words = []

sql = "SELECT relatedWord FROM Hello WHERE namedEntity =?"
def loadWordArrays():
	for Row in c.execute(sql,[('Great')]):
		Words.append(Row[0])
	
	for i in range(0,len(Words)):
		print Words[i]
		
	
loadWordArrays()

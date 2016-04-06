import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pprint as pp
import json, math, re, csv, itertools, os
from nltk.corpus import stopwords
import nltk.stem.snowball as snowball
from bs4 import BeautifulSoup


stemmer = snowball.EnglishStemmer()
files = [f for f in os.listdir("documents")]

bag = {}

for fn in files:
	xml = open("documents/"+fn).read()
	soup = BeautifulSoup(xml)
	title = soup.hedline.text.strip().replace("\n","")
	lead = soup.find_all("block",class_="full_text")
	if len(lead)==0: continue
	lead = lead[0].text
	letter_only = re.sub("[^a-zA-Z]"," ", title + lead).lower()
	# print letter_only
	words = [w for w in letter_only.split() if not w in stopwords.words("english") and len(w)>2]
	# print words
	stemmed_words = [stemmer.stem(w) for w in words]
	for w in stemmed_words:
		if w not in bag: bag[w]=1
		bag[w]+=1



print bag
with open("bag_of_words_nyt.json","w") as outfile:
	outfile.write(json.dumps(bag, indent=4))


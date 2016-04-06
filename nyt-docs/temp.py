import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pprint as pp
import json, math, re, csv, itertools, os
import nltk.stem.snowball as snowball
from bs4 import BeautifulSoup

empties_json = json.loads(open("empties.json","r").read())
print "# of empties: " + str(len(empties_json.keys()))



corrections_json = json.loads(open("corrections.json","r").read())
print "# of Corrections: " + str(len(corrections_json.keys()))

duplicates_json = json.loads(open("duplicates.json","r").read())
pp.pprint([(key[:20], len(s_list),  ) for key, s_list in duplicates_json.iteritems() if len(s_list)>1])

print len([len(s_list) for key, s_list in duplicates_json.iteritems() if len(s_list)>1])
print sum([len(s_list) for key, s_list in duplicates_json.iteritems() if len(s_list)>1])
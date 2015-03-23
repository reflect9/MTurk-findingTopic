import pprint as pp
import json, math, re, csv, itertools, os
from datetime import datetime
import numpy as np

path_to_batch_results = "./batch_results"
batch_files = os.listdir(path_to_batch_results)
dict_turkers = {}
for bf_name in batch_files:
	print bf_name
	with open(path_to_batch_results+"/"+bf_name, mode='r') as bf:
	    reader = csv.DictReader(bf)
	    for row in reader:
	    	if row['Title'] not in dict_turkers: dict_turkers[row['Title']]={}
	    	if row['WorkerId'] not in dict_turkers[row['Title']]: 
	    		dict_turkers[row['Title']][row['WorkerId']]=[]
	    	dict_turkers[row['Title']][row['WorkerId']].append(row['Answer.surveycode'])

pp.pprint(dict_turkers)


# hits_per_turker = [len(hitlist) for tid, hitlist in dict_turkers['Word labeling tasks'].iteritems()]
# print hits_per_turker

# print np.mean(hits_per_turker)
# print np.std(hits_per_turker)
# print np.max(hits_per_turker)
# print np.min(hits_per_turker)



hits_per_turker = [len(hitlist) for tid, hitlist in dict_turkers['Pick the best label for a set of documents'].iteritems()]
print hits_per_turker

print np.mean(hits_per_turker)
print np.std(hits_per_turker)
print np.max(hits_per_turker)
print np.min(hits_per_turker)



# with open('turkers.json','w') as outfile:
# 	json.dump(dict_turkers, outfile, indent = 4)


# file_topicJSON = open("nyt-50-topics-documents.json","r")
# topicJSON = json.loads(file_topicJSON.read())
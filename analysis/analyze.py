import numpy as np
from numpy import arange,array,ones,linalg
import scipy.stats as stats
import matplotlib.pyplot as plt
import pprint as pp
import json, math, re, csv, itertools
import nltk.stem.snowball as snowball
from bs4 import BeautifulSoup
import random


modes = ["word","histogram","wordcloud","topic-in-a-box"]
wordNums = ["5","10","20"]
file_topicJSON = open("nyt-50-topics-documents.json","r")
topicJSON = json.loads(file_topicJSON.read())
path_to_documents = "../findingtopic/dataset/documents/"

with open('csv_backup_3/Answer.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    answers = [rows for rows in reader]


# ANALYSIS 1. OVERALL DURATION 
# plt.figure(facecolor="white")
# durations = [int(a['duration']) for a in answers if int(a['duration'])>1]
# n, bins, patches = plt.hist(durations, bins=100)
# plt.axis([0,600,0,600])
# plt.ylabel("Frequency")
# plt.xlabel("Time spent per task (seconds)")
# plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75)	
# plt.title("Overall Time Spent For Each Task ")

# plt.show()
# print "%s: #:%d, Avg:%f, Median:%f, Stdev:%f, min:%d , max:%d" % ('DURATIONS', len(durations), np.mean(durations), np.median(durations), np.std(durations), min(durations), max(durations))


# ANALYSIS 1a. COMPARE DURATION BETWEEN MODES
# all_durations = []
# plt.figure(1,facecolor="white")
# for i in range(len(modes)):
# 	mode = modes[i]
# 	durations = [int(a['duration']) for a in answers if a['mode']==mode]
# 	durations = [d for d in durations if d>1]
# 	all_durations.append(durations)
# 	fig = plt.subplot(4,1,i+1)
# 	plt.ylabel(mode)
# 	# plt.ylabel("Frequency")
# 	print "%20s: #:%d, Avg:%f, Median:%f, Stdev:%f, min:%d , max:%d, normalityTest:%s" % (mode, len(durations), np.mean(durations), np.median(durations), np.std(durations), min(durations), max(durations), str(stats.normaltest(durations)))
# 	n, bins, patches = plt.hist(durations, bins=range(0, 200 + 10, 10))
# 	plt.axis([0,400,0,200])
# 	plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75)	
# plt.gcf().suptitle("Time Spent For Each Task ")
# plt.show()
# plt.figure(2,facecolor="white")
# plt.boxplot(all_durations)
# plt.ylim([0,120])
# plt.show()



# ANALYSIS 1b. COMPARE DURATION BETWEEN MODES AND WORDNUMS
# plt.figure(3,facecolor="white")
# count=0
# all_durations = []
# for i in range(len(modes)):
# 	for j in range(len(wordNums)):
# 		count+=1
# 		mode = modes[i]
# 		wordNum = wordNums[j]
# 		durations = [int(a['duration']) for a in answers if a['mode']==mode and a['wordNum']==wordNum]
# 		durations = [d for d in durations if d>1]
# 		all_durations.append(durations)
# 		plt.subplot(len(modes),len(wordNums),count)
# 		if count==1 or count==4 or count==7 or count==10:
# 			plt.ylabel(mode)   
# 		if count<10:
# 			plt.gca().get_xaxis().set_visible(False)
# 		else:
# 			plt.xlabel("Time spent (seconds) using "+wordNum+" words")   
# 		print "%20s: #:%d, Avg:%f, Median:%f, Stdev:%f, min:%d , max:%d" % (mode+" "+str(wordNum), len(durations), np.mean(durations), np.median(durations), np.std(durations), min(durations), max(durations))
# 		n, bins, patches = plt.hist(durations, bins=range(0, 200 + 5, 5))
# 		plt.axis([0,300,0,35])
# 		plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75)	
# plt.show()
# plt.figure(4,facecolor="white")
# plt.title("Time Spent For Each Task")
# plt.boxplot(all_durations)
# plt.ylim([0,320])
# plt.xticks(range(1,13), [x+"-"+str(y) for x in modes for y in wordNums], rotation='vertical')
# plt.subplots_adjust(bottom=0.3)
# plt.show()

# ANALYSIS 2a. COMPARE WORD LENGTH BEWTEEN MODES
# plt.figure(5,facecolor="white")
# count=0
# all_values = []
# for i in range(len(modes)):
# 	for j in range(len(wordNums)):
# 		count+=1
# 		mode = modes[i]
# 		wordNum = wordNums[j]
# 		values = [len(a['long'].split(" ")) for a in answers if a['mode']==mode and a['wordNum']==wordNum]
# 		all_values.append(values)
# 		plt.subplot(len(modes),len(wordNums),count)
# 		if count==1 or count==4 or count==7 or count==10:
# 			plt.ylabel(mode)   
# 		if count<10:
# 			plt.gca().get_xaxis().set_visible(False)
# 		else:
# 			plt.xlabel("Word lengths with "+wordNum+"-word settings")  
# 		print "%20s: #:%d, Avg:%f, Median:%f, Stdev:%f, min:%d , max:%d" % (mode+" "+str(wordNum), len(values), np.mean(values), np.median(values), np.std(values), min(values), max(values))
# 		n, bins, patches = plt.hist(values, bins=range(0, 30, 1))
# 		plt.axis([0,20,0,35])
# 		plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75)	
# plt.gcf().suptitle("Length of Sentence Description (# of words)")
# plt.show()
# plt.figure(6,facecolor="white")
# plt.boxplot(all_values)
# plt.ylim([0,30])
# plt.xticks(range(1,13), [x+"-"+str(y) for x in modes for y in wordNums], rotation='vertical')
# plt.subplots_adjust(bottom=0.3)
# plt.show()

# ANALYSIS 2b. COMPARE SHORT DESCRIPTION LENGTH BEWTEEN MODES
# plt.figure(5,facecolor="white")
# count=0
# all_values = []
# for i in range(len(modes)):
# 	for j in range(len(wordNums)):
# 		count+=1
# 		mode = modes[i]
# 		wordNum = wordNums[j]
# 		values = [len(a['short'].split(" ")) for a in answers if a['mode']==mode and a['wordNum']==wordNum]
# 		all_values.append(values)
# 		plt.subplot(len(modes),len(wordNums),count)
# 		if count==1 or count==4 or count==7 or count==10:
# 			plt.ylabel(mode)   
# 		if count<10:
# 			plt.gca().get_xaxis().set_visible(False)
# 		else:
# 			plt.xlabel("Word lengths with "+wordNum+"-word settings")  
# 		print "%20s: #:%d, Avg:%f, Median:%f, Stdev:%f, min:%d , max:%d" % (mode+" "+str(wordNum), len(values), np.mean(values), np.median(values), np.std(values), min(values), max(values))
# 		n, bins, patches = plt.hist(values, bins=range(0, 30, 1))
# 		plt.axis([0,5,0,200])
# 		plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75)	
# plt.gcf().suptitle("Length of Short Summary (# of words)")		
# plt.show()
# plt.figure(6)
# plt.boxplot(all_values)
# plt.ylim([0,5])

# plt.show()



# ANALYSIS 3. SELF-REPORTED CONFIDENCE
# plt.figure(1,facecolor="white")
# confidence = [int(a['conf']) for a in answers]
# n, bins, patches = plt.hist(confidence, bins=100)
# # plt.axis([0,1000,0,800])
# plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75)	
# plt.show()
# print "%s: #:%d, Avg:%f, Median:%f, Stdev:%f, min:%d , max:%d" % ('confidence', len(confidence), np.mean(confidence), np.median(confidence), np.std(confidence), min(confidence), max(confidence))

# plt.figure(1,facecolor="white")
# count=0
# all_values = []
# for i in range(len(modes)):
# 	for j in range(len(wordNums)):
# 		count+=1
# 		mode = modes[i]
# 		wordNum = wordNums[j]
# 		values = [int(a['conf']) for a in answers if a['mode']==mode and a['wordNum']==wordNum]
# 		all_values.append(values)
# 		plt.subplot(len(modes),len(wordNums),count)
# 		if count==1 or count==4 or count==7 or count==10:
# 			plt.ylabel(mode)   
# 		if count<10:
# 			plt.gca().get_xaxis().set_visible(False)
# 		else:
# 			plt.xlabel("Confidence: "+wordNum+"-word settings")  
# 		print "%20s: \t#:%d, \tAvg:%f, \tMedian:%f, \tStdev:%f, \tmin:%d , \tmax:%d" % (mode+" "+str(wordNum), len(values), np.mean(values), np.median(values), np.std(values), min(values), max(values))
# 		n, bins, patches = plt.hist(values, bins=range(0, 30, 1))
# 		plt.axis([0,5,0,200])
# 		plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75)	
# plt.gcf().suptitle("Self-Reported Confidence")				
# plt.show()

# fig = plt.figure(2,facecolor="white")
# ax = fig.add_subplot(111)
# means = {}
# stdev = {}
# for mode in modes:
# 	means[mode]=[]
# 	stdev[mode]=[]
# for mode in modes:
# 	for wordNum in wordNums:
# 		conf_values = [int(a['conf']) for a in answers if a['mode']==mode and a['wordNum']==wordNum]		
# 		means[mode].append(np.mean(conf_values))
# 		stdev[mode].append(np.std(conf_values))

# ind = np.arange(3)
# width=0.15

# rects1 = ax.bar(ind, means[modes[0]], width, color='red', 
# 	yerr=stdev[modes[0]], error_kw=dict(elinewidth=2,ecolor='black'))
# rects2 = ax.bar(ind+width, means[modes[1]], width, color='blue', 
# 	yerr=stdev[modes[1]], error_kw=dict(elinewidth=2,ecolor='black'))
# rects3 = ax.bar(ind+(width*2), means[modes[2]], width, color='green', 
# 	yerr=stdev[modes[2]], error_kw=dict(elinewidth=2,ecolor='black'))
# rects4 = ax.bar(ind+(width*3), means[modes[3]], width, color='gray', 
# 	yerr=stdev[modes[3]], error_kw=dict(elinewidth=2,ecolor='black'))
# ax.set_xlim(-width,len(ind)+width)
# ax.set_ylim(0,5)
# ax.set_ylabel('Confidence')
# ax.set_title('Confidence by visualization and # of words')
# xTickMarks = [wn+" words" for wn in wordNums]
# ax.set_xticks(ind+width)
# xtickNames = ax.set_xticklabels(xTickMarks)
# plt.setp(xtickNames)

# ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), modes, loc=4)



# plt.show()

# plt.figure(6,facecolor="white")
# plt.boxplot(all_values)
# plt.ylim([0,5])
# plt.show()


# ANALYSIS 4. CONTENT ANALYSIS
# topicIdx = 39

# for wordNum in wordNums:
# 	for mode in modes:
# 		print "--------%s----" % mode+" "+str(wordNum)
# 		if mode!="topic-in-a-box":
# 			values = [a['long']+"("+a['conf']+") "+a['duration'] for a in answers if a['mode']==mode and a['wordNum']==wordNum and int(a['topicIdx'])==topicIdx]
# 		else:
# 			values = [a['long']+"("+a['conf']+") "+a['duration'] for a in answers if a['mode']==mode and a['wordNum']==wordNum and int(a['topicIdx'])==topicIdx+1]
# 		pp.pprint(values[:10])



# ANALYSIS 5. WHERE THE WORDS ARE TAKEN FROM
# do word size and bar length affect choice of words? 
# ? 20 word list, histogram, and topicbox tend to lose focus 
# ? Do people use bigram chains in topicbox


# ANALYSIS 5a. SHORT DESCRIPTIONS
# stemmer = snowball.EnglishStemmer()
# all_data = {}

# for topicIdx in range(0,49):
# 	print "\n\n=============== TOPIC "+str(topicIdx)+" =========================="
# 	topicTerms_raw = [terms['first'] for terms in topicJSON['topics'][topicIdx]['terms']]
# 	topicTerms = [stemmer.stem(t) for t in topicTerms_raw]
# 	for mode in modes:
# 		for wordNum in wordNums:
# 			if mode not in all_data:  all_data[mode]={}
# 			if wordNum not in all_data[mode]: all_data[mode][wordNum]=[]

# 			print "--------%s----" % mode+" "+str(wordNum)
# 			if mode!="topic-in-a-box":
# 				records = [a for a in answers if a['mode']==mode and a['wordNum']==wordNum and int(a['topicIdx'])==topicIdx]
# 			else:
# 				records = [a for a in answers if a['mode']==mode and a['wordNum']==wordNum and int(a['topicIdx'])==topicIdx+1]
# 			# now analyze terms in the records
# 			shorts_raw = [r['short'] for r in records] 
# 			shorts = [re.sub('[^0-9a-zA-Z ]+', '', r['short']).split(" ") for r in records] 
# 			shorts = [[stemmer.stem(s.lower()) for s in sl if len(s)>0] for sl in shorts] # removing empty tokens and lowercase
# 			print "SHORT DESCRIPTIONS: "+str(shorts_raw)
# 			print "STEMMED DESCRIPTIONS: "+str(shorts)
# 			print "TOPIC TERMS: "+ str(topicTerms_raw[:int(wordNum)])
# 			print "STEMMED TOPIC TERMS: "+ str(topicTerms[:int(wordNum)])
# 			terms_taken_from_topic = [[s for s in sl if s in topicTerms[:int(wordNum)]] for sl in shorts]
# 			print terms_taken_from_topic
# 			if len(terms_taken_from_topic)>0:
# 				avg_num_words_from_topic = sum([len(s) for s in terms_taken_from_topic]) / (len(terms_taken_from_topic) *1.0)
# 				print avg_num_words_from_topic
# 				all_data[mode][wordNum].append(avg_num_words_from_topic)
# 			# longs = [r['long'] for r in records] 

# # DRAW BAR CHART OF WORD->MODE
# fig = plt.figure(2,facecolor="white")
# ax = fig.add_subplot(111)
# all_data_avg = [[np.mean(vk) for kk,vk in v.iteritems()] for k,v in all_data.iteritems()]
# all_data_stdev = [[np.std(vk) for kk,vk in v.iteritems()] for k,v in all_data.iteritems()]
# print all_data_avg
# print all_data_stdev
# ind = np.arange(3)
# width=0.15
# rects1 = ax.bar(ind, all_data_avg[0], width, color='red', 
# 	yerr=all_data_stdev[0], error_kw=dict(elinewidth=2,ecolor='black'))
# rects2 = ax.bar(ind+width, all_data_avg[1], width, color='blue', 
# 	yerr=all_data_stdev[1], error_kw=dict(elinewidth=2,ecolor='black'))
# rects3 = ax.bar(ind+(width*2), all_data_avg[2], width, color='green', 
# 	yerr=all_data_stdev[2], error_kw=dict(elinewidth=2,ecolor='black'))
# rects4 = ax.bar(ind+(width*3), all_data_avg[3], width, color='gray', 
# 	yerr=all_data_stdev[3], error_kw=dict(elinewidth=2,ecolor='black'))

# ax.set_xlim(-width,len(ind)+width)
# ax.set_ylim(0,2.5)
# ax.set_ylabel('Avg. number of shared terms ')
# ax.set_title('# of Terms in Short Description taken from topics')
# xTickMarks = [wn+" words" for wn in wordNums]
# ax.set_xticks(ind+width)
# xtickNames = ax.set_xticklabels(xTickMarks)
# plt.setp(xtickNames)

# ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), modes, loc=1)
# plt.show()


# ANALYSIS 5b. LONG DESCRIPTIONS
# stemmer = snowball.EnglishStemmer()
# all_data = {}
# for topicIdx in range(0,49):
# 	print "\n\n=============== TOPIC "+str(topicIdx)+" =========================="
# 	topicTerms_raw = [terms['first'] for terms in topicJSON['topics'][topicIdx]['terms']]
# 	topicTerms = [stemmer.stem(t) for t in topicTerms_raw]
# 	for mode in modes:
# 		for wordNum in wordNums:
# 			if mode not in all_data:  all_data[mode]={}
# 			if wordNum not in all_data[mode]: all_data[mode][wordNum]=[]

# 			print "--------%s----" % mode+" "+str(wordNum)
# 			if mode!="topic-in-a-box":
# 				records = [a for a in answers if a['mode']==mode and a['wordNum']==wordNum and int(a['topicIdx'])==topicIdx]
# 			else:
# 				records = [a for a in answers if a['mode']==mode and a['wordNum']==wordNum and int(a['topicIdx'])==topicIdx+1]
# 			# now analyze terms in the records
# 			longs_raw = [r['long'] for r in records] 
# 			longs = [re.sub('[^0-9a-zA-Z ]+', '', r['long']).split(" ") for r in records] 
# 			longs = [[stemmer.stem(s.lower()) for s in sl if len(s)>0] for sl in longs] # removing empty tokens and lowercase
# 			print "LONG DESCRIPTIONS: "+str(longs_raw)
# 			print "STEMMED DESCRIPTIONS: "+str(longs)
# 			print "TOPIC TERMS: "+ str(topicTerms_raw[:int(wordNum)])
# 			print "STEMMED TOPIC TERMS: "+ str(topicTerms[:int(wordNum)])
# 			terms_taken_from_topic = [[s for s in sl if s in topicTerms[:int(wordNum)]] for sl in longs]
# 			print "SHARED TERMS: "+str(terms_taken_from_topic)
# 			if len(terms_taken_from_topic)>0:
# 				avg_num_words_from_topic = sum([len(s) for s in terms_taken_from_topic]) / (len(terms_taken_from_topic) *1.0)
# 				print avg_num_words_from_topic
# 				portions = [len(shared_terms)/(len(longs[i])*1.0) for i,shared_terms in enumerate(terms_taken_from_topic)]
# 				print portions
# 				all_data[mode][wordNum].append(np.mean(portions))
# 			# longs = [r['long'] for r in records] 

# # DRAW BAR CHART OF WORD->MODE
# fig = plt.figure(2,facecolor="white")
# ax = fig.add_subplot(111)
# all_data_avg = [[np.mean(vk) for kk,vk in v.iteritems()] for k,v in all_data.iteritems()]
# all_data_stdev = [[np.std(vk) for kk,vk in v.iteritems()] for k,v in all_data.iteritems()]
# print all_data_avg
# print all_data_stdev
# ind = np.arange(3)
# width=0.15
# rects1 = ax.bar(ind, all_data_avg[0], width, color='red', 
# 	yerr=all_data_stdev[0], error_kw=dict(elinewidth=2,ecolor='black'))
# rects2 = ax.bar(ind+width, all_data_avg[1], width, color='blue', 
# 	yerr=all_data_stdev[1], error_kw=dict(elinewidth=2,ecolor='black'))
# rects3 = ax.bar(ind+(width*2), all_data_avg[2], width, color='green', 
# 	yerr=all_data_stdev[2], error_kw=dict(elinewidth=2,ecolor='black'))
# rects4 = ax.bar(ind+(width*3), all_data_avg[3], width, color='gray', 
# 	yerr=all_data_stdev[3], error_kw=dict(elinewidth=2,ecolor='black'))

# ax.set_xlim(-width,len(ind)+width)
# ax.set_ylim(0,0.65)
# ax.set_ylabel('Avg. portions of shared terms ')
# ax.set_title('Portion of Terms in Long Description taken from topics')
# xTickMarks = [wn+" words" for wn in wordNums]
# ax.set_xticks(ind+width)
# xtickNames = ax.set_xticklabels(xTickMarks)
# plt.setp(xtickNames)

# ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), modes, loc=1)
# plt.show()




# ANALYSIS 5c. FURTHER ANALYSIS OF SHARED TERMS
# stemmer = snowball.EnglishStemmer()
# all_data = {}

# for topicIdx in range(0,50):
# 	# print "\n\n=============== TOPIC "+str(topicIdx)+" =========================="
# 	topicTerms_raw = topicJSON['topics'][str(topicIdx)]['terms']
# 	topicTerms = {}
# 	for term in topicTerms_raw:
# 		tStr = term['first']
# 		prob = term['second']
# 		if tStr not in topicTerms: 
# 			topicTerms[tStr] = prob
# 		else:
# 			topicTerms[tStr] += prob
# 	for mode in modes:
# 		for wordNum in wordNums:
# 			if topicIdx not in all_data:  all_data[topicIdx]={}
# 			if mode not in all_data[topicIdx]:  all_data[topicIdx][mode]={}
# 			# if wordNum not in all_data[topicIdx][mode]: all_data[topicIdx][mode][wordNum]={}

# 			# print "--------%s----" % mode+" "+str(wordNum)
# 			if mode!="topic-in-a-box":
# 				records = [a for a in answers if a['mode']==mode and a['wordNum']==wordNum and int(a['topicIdx'])==topicIdx]
# 			else:
# 				records = [a for a in answers if a['mode']==mode and a['wordNum']==wordNum and int(a['topicIdx'])==topicIdx+1]
# 			# now analyze terms in the records
# 			shorts_raw = [r['short'] for r in records] 
# 			shorts = [re.sub('[^0-9a-zA-Z ]+', '', r['short']).split(" ") for r in records] 
# 			shorts = [[stemmer.stem(s.lower()) for s in sl if len(s)>0] for sl in shorts] # removing empty tokens and lowercase
# 			# print "SHORT DESCRIPTIONS: "+str(shorts_raw)
# 			# print "STEMMED DESCRIPTIONS: "+str(shorts)
# 			# # print "TOPIC TERMS: "+ str(topicTerms_raw[:int(wordNum)])
# 			# print "STEMMED TOPIC TERMS: "+ str([term for term, data in sorted(topicTerms.iteritems(),key=lambda k: k[1], reverse=True)[:int(wordNum)]])
# 			bag = {term:{'prob':prob, 'freq':0} for term, prob in topicTerms.iteritems()} 
# 			for sl in shorts:
# 				for s in sl:
# 					if s in bag:   
# 						bag[s]['freq'] += 1
# 			# pp.pprint(sorted(bag.iteritems(), key=lambda k:k[1]['prob'], reverse=True))
# 			all_data[topicIdx][mode][wordNum]=bag
# 			# terms_taken_from_topic = [[s for s in sl if s in topicTerms[:int(wordNum)]] for sl in shorts]
# 			# print terms_taken_from_topic
# 			# if len(terms_taken_from_topic)>0:
# 			# 	avg_num_words_from_topic = sum([len(s) for s in terms_taken_from_topic]) / (len(terms_taken_from_topic) *1.0)
# 			# 	print avg_num_words_from_topic
# 			# 	all_data[mode][wordNum].append(avg_num_words_from_topic)
# 			# longs = [r['long'] for r in records] 


# fig = plt.figure(2,facecolor="white")
# ax = fig.add_subplot(111)
# prob = []
# freq = []
# for mode in modes:
# 	for wordNum in wordNums:		
# 		for topicIdx in range(50):
# 			bag = all_data[topicIdx][mode][wordNum]
# 			for term, data in bag.iteritems():
# 				prob.append(data['prob'])
# 				freq.append(data['freq']+random.uniform(-0.15,0.15))


# ax.scatter(prob,freq, s=2, marker="+")
# ax.set_title("Terms probability and Frequency of Being Used in Short Descriptions ")
# ax.set_ylabel("Frequency")   
# ax.set_xlabel("Term Probability")   
# ax.text(0.95, 0.95, "correlation = "+ str(np.corrcoef(prob,freq)[0][1]), ha='right', va='top', transform=ax.transAxes)
# plt.show()
# # DRAW PROB,FREQ scatterplot for different settings
# fig = plt.figure(3,facecolor="white")
# count = 1
# for mode in modes:
# 	for wordNum in wordNums:
# 		# COLLECT PROB,FREQ INFO FROM ALL TOPICS
# 		prob = []
# 		freq = []
# 		for topicIdx in range(50):
# 			bag = all_data[topicIdx][mode][wordNum]
# 			for term, data in bag.iteritems():
# 				prob.append(data['prob'])
# 				freq.append(data['freq']+random.uniform(-0.15,0.15))
# 		# LETS DRAW SCATTERPLOT
# 		ax = fig.add_subplot(len(modes),len(wordNums),count)
# 		ax.tick_params(axis='both',which='major', labelsize=8)
# 		ax.tick_params(axis='both',which='minor', labelsize=7)
# 		ax.set_ylim(0,8)
# 		ax.scatter(prob,freq, s=3, marker='+')
# 		ax.text(0.98, 0.98, str(np.corrcoef(prob,freq)[0][1])[:8], ha='right', va='top', transform=ax.transAxes)
# 		if count==1 or count==4 or count==7 or count==10:
# 			ax.set_ylabel(mode)   
# 		if count<10:
# 			ax.get_xaxis().set_visible(False)
# 		else:
# 			ax.set_xlabel(wordNum + " words")   
# 		count += 1
# plt.show()
 

# DRAW BAR CHART OF WORD->MODE
# fig = plt.figure(2,facecolor="white")
# ax = fig.add_subplot(111)
# all_data_avg = [[np.mean(vk) for kk,vk in v.iteritems()] for k,v in all_data.iteritems()]
# all_data_stdev = [[np.std(vk) for kk,vk in v.iteritems()] for k,v in all_data.iteritems()]
# print all_data_avg
# print all_data_stdev
# ind = np.arange(3)
# width=0.15
# rects1 = ax.bar(ind, all_data_avg[0], width, color='red', 
# 	yerr=all_data_stdev[0], error_kw=dict(elinewidth=2,ecolor='black'))
# rects2 = ax.bar(ind+width, all_data_avg[1], width, color='blue', 
# 	yerr=all_data_stdev[1], error_kw=dict(elinewidth=2,ecolor='black'))
# rects3 = ax.bar(ind+(width*2), all_data_avg[2], width, color='green', 
# 	yerr=all_data_stdev[2], error_kw=dict(elinewidth=2,ecolor='black'))
# rects4 = ax.bar(ind+(width*3), all_data_avg[3], width, color='gray', 
# 	yerr=all_data_stdev[3], error_kw=dict(elinewidth=2,ecolor='black'))

# ax.set_xlim(-width,len(ind)+width)
# ax.set_ylim(0,2.5)
# ax.set_ylabel('Avg. number of shared terms ')
# ax.set_title('# of Terms in Short Description taken from topics')
# xTickMarks = [wn+" words" for wn in wordNums]
# ax.set_xticks(ind+width)
# xtickNames = ax.set_xticklabels(xTickMarks)
# plt.setp(xtickNames)

# ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), modes, loc=1)
# plt.show()




#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
# ANALYSIS 6. DOCUMENT ANALYSIS
# topicIdx = 3
# for topicIdx in range(50):
# 	topicTerms = [term['first'].encode("utf8") for term in topicJSON['topics'][str(topicIdx)]['terms']]
# 	doc_id_list = [(doc['first'],doc['second']) for doc in topicJSON['topics'][str(topicIdx)]['docs']]
# 	doc_xml_list = [open(path_to_documents+df[0]).read() for df in doc_id_list]
# 	doc_soup_list = [BeautifulSoup(doc_xml) for doc_xml in doc_xml_list]
# 	titles = [ds.hedline.text.strip().replace("\n","") for ds in doc_soup_list]
# 	leads = [ds.find_all("block",class_="full_text") for ds in doc_soup_list]

# 	print "================================================================="
# 	print "TOPIC "+str(topicIdx) + " --- " + str(topicTerms) + ""
# 	print "================================================================="
# 	# print "TOP-DOCS"+str(doc_id_list)
# 	for i in range(len(doc_xml_list)):
# 		print "["+str(titles[i].encode("utf8")) + "]\t\t(" + str(doc_id_list[i][1]) + ")"
# 		# print "["+str(titles[i].encode("utf8")) + "]"
# 		print "\t"+(leads[i][0].text.encode("utf8").strip().replace("\n","  ")[:500]+"..." if len(leads[i])>0 else "EMPTY")
# 		print ""
# # leads = [lead[0].text for lead in leads]


# for wordNum in wordNums:
# 	for mode in modes:
# 		print "--------%s----" % mode+" "+str(wordNum)
# 		if mode!="topic-in-a-box":
# 			values = [a['long']+"("+a['conf']+") "+a['duration'] for a in answers if a['mode']==mode and a['wordNum']==wordNum and int(a['topicIdx'])==topicIdx]
# 		else:
# 			values = [a['long']+"("+a['conf']+") "+a['duration'] for a in answers if a['mode']==mode and a['wordNum']==wordNum and int(a['topicIdx'])==topicIdx+1]
# 		# pp.pprint(values[:10])




# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# # ANALYSIS 7. LABELING HIT ANALYSIS

# with open('csv_backup_3/LabelingHit.csv', mode='r') as infile:
#     reader = csv.DictReader(infile)
#     hits = [rows for rows in reader]

# dict_usercode = {}
# for hit in hits:
# 	uc = hit['usercode']
# 	if uc in dict_usercode:
# 		dict_usercode[uc] += 1
# 	else:
# 		dict_usercode[uc] = 1

# pp.pprint(dict_usercode)
# print len(dict_usercode.keys())
# print len(dict_usercode.keys()) * 5
# print len(answers)





# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# # ANALYSIS 8. EVALUATION ANALYSIS




with open('csv_backup_4/Evaluation.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    evals = [rows for rows in reader]
    # pp.pprint(evals[:5])

## CREATE DICT FILE FOR ALL_DESCRIPTION PAGE
## 8-5-topic-in-a-box-3-long
## topicIdx -> wordNum -> 4 modes + algorithm -> desc -> short/long
# data = {}
# for ev in evals:
# 	if ev['best'] != "":
# 		best =  re.sub(r'[\[\]\'u]', '', ev['best']).split(", ")
# 		for kn in best:
# 			if "bad" in kn: continue
# 			if kn not in data: 
# 				data[kn]={'best':0, 'worst':0}
# 			data[kn]['best']+=1
# 	if ev['worst'] != "":
# 		worst =  re.sub(r'[\[\]\'u]', '', ev['worst']).split(", ")
# 		for kn in worst:
# 			if "bad" in kn: continue
# 			if kn not in data: 
# 				data[kn]={'best':0, 'worst':0}
# 			data[kn]['worst']+=1
# with open('csv_backup_4/evaluation_dict.json', 'w') as outfile:
# 	json.dump(data, outfile, indent=4)



dict_eval = {}
for wordNum in wordNums:
	dict_eval[wordNum]={}
	for mode in modes+["algorithm"]:
		dict_eval[wordNum][mode]={}
		for shortOrLong in ["short","long"]:
			dict_eval[wordNum][mode][shortOrLong]={'best':0, 'worst':0}

evals = [ev for ev in evals if ev['done']=='True' and "bad" not in ev['worst'] and "bad" not in ev['best'] ]
for ev in evals:
	# print "------------------------"
	# print ev
	if ev['best'] != "":
		# print "BEST: "+ev['best']
		best =  ev['best'].replace("u'","").replace("[","").replace("]","").replace("'","").split(", ")
		# print best
		for kn in best:	
			if kn=="algorithm": mode=kn
			else: mode = [mode for mode in modes if mode==kn or mode+"-" in kn][0] 
			# print mode
			# print dict_eval[ev['wordNum']][mode][ev['shortOrLong']]
			dict_eval[ev['wordNum']][mode][ev['shortOrLong']]['best'] += 1
			# print "-->"+str(dict_eval[ev['wordNum']][mode][ev['shortOrLong']])
	if ev['worst'] != "":
		# print "WORST: "+ev['worst']
		worst =  ev['worst'].replace("u'","").replace("[","").replace("]","").replace("'","").split(", ")
		# print worst
		for kn in worst:	
			if kn=="algorithm": mode=kn
			else: mode = [mode for mode in modes if mode==kn or mode+"-" in kn][0] 
			# print mode
			# print dict_eval[ev['wordNum']][mode][ev['shortOrLong']]
			dict_eval[ev['wordNum']][mode][ev['shortOrLong']]['worst'] += 1
			# print "-->"+ str(dict_eval[ev['wordNum']][mode][ev['shortOrLong']])

pp.pprint(dict_eval)

# # BAR CHART OF SHORT LABELS (ALSO SHOWS ALGORITHM) 
fig = plt.figure(1,facecolor="white")
count=0
ind = np.arange(5)
width=0.35
for wordNum in wordNums:
	d = dict_eval[wordNum]
	count+=1
	ax = fig.add_subplot(3,1,count)
	best_data = []
	worst_data = []
	for mi, mode in enumerate(modes+["algorithm"]):
		dd = d[mode]
		best_data.append(dd['short']['best'])
		worst_data.append(dd['short']['worst'])
	ax_best= ax.bar(ind, best_data, width, color='b')
	ax_worst= ax.bar(ind+width, worst_data, width, color='r')
	ax.set_ylim(0,110)
	ax.set_ylabel(str(wordNum) + " words")
	xTickMarks = [mode for mode in modes+["algorithm"]]
	ax.set_xticks(ind+width)
	xtickNames = ax.set_xticklabels(xTickMarks)
	plt.setp(xtickNames)

# plt.legend([ax_best, ax_worst], ('Best','Worst'), loc='upper right')

fig.text(0.03, 0.5, '# of best / worst votes', fontsize=15, ha='center', va='center', rotation='vertical')
fig.text(0.5, 0.98, 'Label Evaluation (Short)', fontsize=17, ha='center', va='top')
# ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), modes, loc=1)

plt.show()
			

# BAR CHART OF LONG LABELS (ALSO SHOWS ALGORITHM) 
# fig = plt.figure(1,facecolor="white")
# count=0
# ind = np.arange(4)
# width=0.35
# for wordNum in wordNums:
# 	d = dict_eval[wordNum]
# 	count+=1
# 	ax = fig.add_subplot(3,1,count)
# 	best_data = []
# 	worst_data = []
# 	for mi, mode in enumerate(modes):
# 		dd = d[mode]
# 		best_data.append(dd['long']['best'])
# 		worst_data.append(dd['long']['worst'])
# 	ax_best= ax.bar(ind, best_data, width, color='b')
# 	ax_worst= ax.bar(ind+width, worst_data, width, color='r')
# 	ax.set_ylim(0,85)
# 	ax.set_ylabel(str(wordNum) + " words")
# 	xTickMarks = [mode for mode in modes]
# 	ax.set_xticks(ind+width)
# 	xtickNames = ax.set_xticklabels(xTickMarks)
# 	plt.setp(xtickNames)

# # plt.legend([ax_best, ax_worst], ('Best','Worst'), loc='upper right')

# fig.text(0.03, 0.5, '# of best / worst votes', fontsize=15, ha='center', va='center', rotation='vertical')
# fig.text(0.5, 0.98, 'Label Evaluation (Long)', fontsize=17, ha='center', va='top')
# # ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), modes, loc=1)

# plt.show()
		


# # # BAR CHART OF SHORT LABELS: DIFFERENCE 
# fig = plt.figure(1,facecolor="white")
# count=0
# ind = np.arange(5)
# width=0.35
# for wordNum in wordNums:
# 	d = dict_eval[wordNum]
# 	count+=1
# 	ax = fig.add_subplot(3,1,count)
# 	diff_data = []
# 	for mi, mode in enumerate(modes+["algorithm"]):
# 		dd = d[mode]
# 		diff_data.append(dd['short']['best']-dd['short']['worst'])
# 	ax.bar(ind+width/2, diff_data, width=width, color='g')
# 	ax.set_ylim(-70,50)
# 	ax.set_ylabel(str(wordNum) + " words")
# 	xTickMarks = [mode for mode in modes+["algorithm"]]
# 	ax.set_xticks(ind+width)
# 	xtickNames = ax.set_xticklabels(xTickMarks)
# 	plt.setp(xtickNames)
# 	plt.gca().grid(True)

# # plt.legend([ax_best, ax_worst], ('Best','Worst'), loc='upper right')

# fig.text(0.03, 0.5, '# of best votes - # of worst votes', fontsize=15, ha='center', va='center', rotation='vertical')
# fig.text(0.5, 0.98, 'Label Evaluation (Short)', fontsize=17, ha='center', va='top')
# # ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), modes, loc=1)
# plt.show()



# # # BAR CHART OF LONG LABELS: DIFFERENCE 
# fig = plt.figure(1,facecolor="white")
# count=0
# ind = np.arange(4)
# width=0.35
# for wordNum in wordNums:
# 	d = dict_eval[wordNum]
# 	count+=1
# 	ax = fig.add_subplot(3,1,count)
# 	diff_data = []
# 	for mi, mode in enumerate(modes):
# 		dd = d[mode]
# 		diff_data.append(dd['long']['best']-dd['long']['worst'])
# 	ax.bar(ind+width/2, diff_data, width=width, color='g')
# 	ax.set_ylim(-70,50)
# 	ax.set_ylabel(str(wordNum) + " words")
# 	xTickMarks = [mode for mode in modes]
# 	ax.set_xticks(ind+width)
# 	xtickNames = ax.set_xticklabels(xTickMarks)
# 	plt.setp(xtickNames)
# 	plt.gca().grid(True)

# # plt.legend([ax_best, ax_worst], ('Best','Worst'), loc='upper right')

# fig.text(0.03, 0.5, '# of best votes - # of worst votes', fontsize=15, ha='center', va='center', rotation='vertical')
# fig.text(0.5, 0.98, 'Label Evaluation (Long)', fontsize=17, ha='center', va='top')
# # ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), modes, loc=1)
# plt.show()

	# ax = fig.add_subplot(111)


# player_dict = {mode:0 for mode in modes}
# player_dict['algorithm'] = 0
# winner_dict = {mode:0 for mode in modes}
# loser_dict = {mode:0 for mode in modes}
# winner_dict['algorithm'] = 0
# loser_dict['algorithm'] = 0
# for ev in evals:
# 	players = [mode for mode in player_dict.keys() if mode+"-" in ev['players']]
# 	for w in players: player_dict[w] += 1

# 	winners = [mode for mode in winner_dict.keys() if mode+"-" in ev['best']]
# 	for w in winners: winner_dict[w] += 1

# 	losers = [mode for mode in loser_dict.keys() if mode+"-" in ev['worst']]
# 	for w in losers: loser_dict[w] += 1
# 	# print ev['best'] + " , " + str(winner)

# pp.pprint(player_dict)
# pp.pprint(winner_dict)
# pp.pprint(loser_dict)
# pp.pprint([winner_dict[mode] - loser_dict[mode] for mode in modes])



















#plt.savefig("path.png")
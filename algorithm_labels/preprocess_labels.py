import pprint as pp
import json, re, csv, itertools, os

file = open("labels.txt","r")
label_dict = {}
while True:
	line = file.readline()
	if "\t[" in line:
		topicIdx = int(line.split("\t")[0])
		label_dict[topicIdx] = []
		# terms = line.split("\t")[1].replace("[","").replace("[","").split(" ")
	if "----" == line[:4]:
		# print line.split(",")[2]
		label_dict[topicIdx].append(line.split(",")[2].strip())
	if line=="":
		break

label_dict = {k:v[:3] for k,v in label_dict.iteritems()}
pp.pprint(label_dict)
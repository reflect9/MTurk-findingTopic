import pprint as pp
import json, re, csv, itertools, os, random


# THIS WILL GENERATE 300 RANDOM LABELS BY CONCATENATING 3 WORDS FROM UNIX DICTINARY

file = open("/usr/share/dict/words","r")
labels = []
words = [line.replace("\n","") for line in file.readlines()]
for i in range(300):
	labels.append(" ".join(random.sample(words,3)))
print labels
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pprint as pp
import json, math, re, csv, itertools, os
import nltk.stem.snowball as snowball
from bs4 import BeautifulSoup


file_topicJSON = open("nyt-50-topics-40docs.json","r")
topicJSON = json.loads(file_topicJSON.read())
path_to_documents = "./documents"

document_dict = {}

for topicIdx in range(50):
	topicTerms = [term['first'].encode("utf8") for term in topicJSON['topics'][str(topicIdx)]['terms']]
	doc_id_list = [(doc['first'],doc['second']) for doc in topicJSON['topics'][str(topicIdx)]['docs']]
	doc_xml_list = [open(path_to_documents+"/"+df[0]).read() for df in doc_id_list]
	doc_soup_list = [BeautifulSoup(doc_xml) for doc_xml in doc_xml_list]
	titles = [ds.hedline.text.strip().replace("\n","") for ds in doc_soup_list]
	leads = [ds.find_all("block",class_="full_text") for ds in doc_soup_list]
	leads = [lead[0].text.encode("utf8").strip().replace("\n","  ") if len(lead)>0 else "EMPTY" for lead in leads]
	together = [{'id':doc_id_list[i][0], 'prob':doc_id_list[i][1], 'title':title, 'fulltext':leads[i]} for i,title in enumerate(titles)]
	document_dict[str(topicIdx)] = together


with open("nyt-topic-to-document.json","w") as outfile:
	outfile.write(json.dumps(document_dict, indent=4))



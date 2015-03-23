import networkx as nx
import matplotlib.pyplot as plt
import pprint as pp
import json, math, re

def topicbox_graph(word_limit=20):
	""" Returns 50 topic modeling graphs created from NYTimes articles.
	"""
	bg_file = open("nyt-bigrams.json","r")
	bigrams = json.loads(bg_file.read())
	bigram_dict = {}	# {"The, National":40,...
	for value,bigram in enumerate(bigrams):
		w1 = (bigram.split(',')[0]).strip().lower()
		w2 = (bigram.split(',')[1]).strip().lower()
		w1 = re.sub('[^0-9a-zA-Z]+', '', w1)
		w2 = re.sub('[^0-9a-zA-Z]+', '', w2)
		if bigram_dict.has_key(w1)==False:
			bigram_dict[w1]={}
		bigram_dict[w1][w2]= value
	# pp.pprint(bigram_dict)
	
	topic_file = open("nyt-50-topics.json","r")
	topics = json.loads(topic_file.read())['topics']
	# {"topics":[{"terms":[{"first":"states","second":0.03720213504660771},...
	
	G_50 = []
	for topic in topics:
		G = nx.Graph()
		terms = topic['terms'][:word_limit]
		for term in terms: 
			# print term
			G.add_node(term['first'], probability=term['second'])
		# now add edges
		for i in range(len(terms)):
			for j in range(i,len(terms)):
				# print i,j;
				t1 = terms[i]['first']
				t2 = terms[j]['first']
				# print topic['terms'][i]['first']
				
				if t1==t2: continue
				weight_t1_t2 = 0
				# print t1,t2;
				if bigram_dict.has_key(t1):
					# pp.pprint(bigram_dict[t1])
					if bigram_dict[t1].has_key(t2):
						# print t1,t2;
						weight_t1_t2 = weight_t1_t2 + bigram_dict[t1][t2]
				if bigram_dict.has_key(t2):
					# pp.pprint(bigram_dict[t2])
					if bigram_dict[t2].has_key(t1):
						# print t1,t2;
						weight_t1_t2 = weight_t1_t2 + bigram_dict[t2][t1]
				if weight_t1_t2<0.1: continue
				# print t1, t2, weight_t1_t2
				G.add_edge(t1,t2,weight=math.log(int(weight_t1_t2)))
		G_50.append(G)
	return G_50



def generate_all():
	for wl in [5,10,20]:
		Gs = topicbox_graph(word_limit=wl)
		for i,G in enumerate(Gs):
			for il in [1,2,3,4,5]:
				pos = nx.spring_layout(Gs[i], scale=1, k=0.4)
				node_size = list((data['probability']*150000) for term,data in Gs[i].nodes(data=True))
				# pp.pprint(node_size)
				plt.figure(figsize=(4,2.5), dpi=200)


				nx.draw_networkx_nodes(Gs[i], pos=pos, node_size=node_size, node_color='gray', alpha=0.25, linewidths=0)
				nx.draw_networkx_edges(Gs[i], pos=pos, alpha=0.25, width=1)
				nx.draw_networkx_labels(Gs[i], pos=pos, font_size=8)
				plt.axis('off')
				# cut = 1.05
				# xmax= cut*max(xx for xx,yy in pos.values())
				# ymax= cut*max(yy for xx,yy in pos.values())
				# plt.xlim(0,xmax)
				# plt.ylim(0,ymax)
				plt.savefig("topicBox_"+str(i+1)+"_"+str(wl)+"_"+str(il)+".png", bbox_inches='tight', dpi=200)
				print "topicBox_"+str(i+1)+"_"+str(wl)+"_"+str(il)+".png"
				plt.close()
				# plt.show()


def generate(topicIdx):
	i = topicIdx
	for wl in [5,10,20]:
		Gs = topicbox_graph(word_limit=wl)
		for il in range(10):
			pos = nx.spring_layout(Gs[i], scale=1, k=0.4)
			node_size = list((data['probability']*150000) for term,data in Gs[i].nodes(data=True))
			plt.figure(figsize=(4,2.5), dpi=500)
			nx.draw_networkx_nodes(Gs[i], pos=pos, node_size=node_size, node_color='gray', alpha=0.25, linewidths=0)
			nx.draw_networkx_edges(Gs[i], pos=pos, alpha=0.25, width=1)
			nx.draw_networkx_labels(Gs[i], pos=pos, font_size=8)
			plt.axis('off')
			plt.savefig("highres_topicbox_"+str(i+1)+"_"+str(wl)+"_"+str(il)+".png", bbox_inches='tight', dpi=500)
			print "highres_topicbox_"+str(i+1)+"_"+str(wl)+"_"+str(il)+".png"
			plt.close()


generate(6)


# G=nx.Graph()
# G.add_node("a")
# G.add_node("b")
# G.add_node("c")
# G.add_edge("a","b")
# G.add_edge("d","e")

# nx.draw(G)
# plt.show()


#plt.savefig("path.png")
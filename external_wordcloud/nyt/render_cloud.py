import os, json
from wordcloud import WordCloud

def color_func(word, font_size, position, orientation, random_state=None):
	if random_state is None:
		random_state = Random()
	return "hsl(240, 0%%, %d%%)" % random_state.randint(10, 60)
	# return "hsl(220, 30%%, 0%%)"
	# return "hsl(240, 0%%, %d%%)" % max(0,(60-font_size))
	# return "black"


def genWordCloud(words_, fileName):
    words = WordCloud(width=400, height=250, 
    		prefer_horizontal=1, max_font_size=80, margin=10,
    		color_func=color_func, background_color="white", 
    		font_path='arial.ttf')
    # words.generate(text)
    words.words_ = words_
    words.fit_words(words.words_)
    words.to_file(fileName+'.png')

if __name__ == '__main__':
	file_topicJSON = open("nyt-50-topics.json","r")
	topicJSON = json.loads(file_topicJSON.read())
	topics = topicJSON['topics']
	topics_cleaned = []
	for topic in topics:
		topics_cleaned.append(map(lambda x: [x['first'], x['second']], topic['terms']))

	# print topics_cleaned
	for i, topic in enumerate(topics_cleaned):
		for k in [5,10,20]:
			# genWordCloud(topic[:k],"nyt_"+str(i+1)+"_"+str(k));
			for l in [1,2,3,4,5]:
				genWordCloud(topic[:k],"nyt_"+str(i)+"_"+str(k)+"_"+str(l));
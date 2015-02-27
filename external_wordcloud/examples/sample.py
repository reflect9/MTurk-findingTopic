import os
from wordcloud import WordCloud

def bw(word, font_size, position, orientation, random_state=None):
	if random_state is None:
		random_state = Random()
	return "hsl(220, 30%%, %d%%)" % random_state.randint(15, 70)

def genWordCloud(filename):
    text = open(filename).read()
    words = WordCloud(width=300, height=270, prefer_horizontal=1, color_func=bw , background_color="white", font_path='font.ttf')
    # words.generate(text)
    words.words_ = [["a",0.9],["b",0.5],["c",0.2]]
    words.fit_words(words.words_)
    words.to_file(os.path.splitext(filename)[0]+'.png')

if __name__ == '__main__':
    genWordCloud('a_new_hope.txt')
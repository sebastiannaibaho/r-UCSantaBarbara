import word_utility
import gensim

#PRECONDITION: post is a list of [x,y] where x is a topicid and y is assigned probability             
#POSTCONDITION: returns the topic,probability array with highest probability
def get_top_topic(post):
	max = post[0]
	for i in range(len(post)):
		if post[i][1] > max[1]:
			max = post[i]
	return max

#PRECONDITION: model is the ldamodel to be used, post is one reddit post in string format
#              id2word is dictionary corpus of the lda model
#POSTCONDITION: returns the most likely topic number of the post as an integer
def get_topic(model, id2word, post):

	doc = []
	doc.append([post])
	doc[0] = doc[0][0].split(" ")
	doc[0] = word_utility.remove_stopwords(doc[0])
	doc[0] = word_utility.lemmatize(doc[0])

	bow = [id2word.doc2bow(text) for text in doc]

	topic = get_top_topic(model.get_document_topics(bow[0]))
	return topic[0]

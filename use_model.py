import gensim #pip install gensim
import word_utility
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from pprint import pprint #pip install pprint
import pyLDAvis #pip install pyLDAvis
import pyLDAvis.gensim
import csv
import lda_model #need id2word variable

mallet_path = "mallet-2.0.8/bin/mallet"

#PRECONDITION: post is a list of [x,y] where x is a topicid and y is assigned probability             
#POSTCONDITION: returns the topic,probability array with highest probability
def get_top_topic(post):
	max = post[0]
	for i in range(len(post)):
		if post[i][1] > max[1]:
			max = post[i]
	return max

#PRECONDITION: model is the ldamodel to be used, post is one reddit post in string format
#POSTCONDITION: returns the most likely topic number of the post as an integer
def get_topic(model, post):

	doc = []
	doc.append([post])
	doc[0] = doc[0][0].split(" ")
	doc[0] = word_utility.remove_stopwords(doc[0])
	doc[0] = word_utility.lemmatize(doc[0])

	print(doc)
	#idword = corpora.Dictionary(doc)
	bow = [lda_model.id2word.doc2bow(text) for text in doc]

	#print(bow)
	#print(idword)
	print(model.get_document_topics(bow[0]))

	topic = get_top_topic(model.get_document_topics(bow[0]))
	return topic[0]
	
if __name__ == '__main__':

	#either build the model
	'''
	with open("output.csv", newline = '') as f: #read csv file
		reader = csv.reader(f)
		#remove empty rows
		format1 = []
		for row in reader: 
			if row != []:
				format1.append(row)
				
	print("Building bigrams and trigrams")
	bigram = gensim.models.Phrases(format1, min_count=5, threshold=100)
	trigram = gensim.models.Phrases(bigram[format1], threshold=100)
	bigram_mod = gensim.models.phrases.Phraser(bigram)
	trigram_mod = gensim.models.phrases.Phraser(trigram)

	print("Processing text")
	for i in range(len(format1)):
		format1[i] = word_utility.remove_stopwords(format1[i])
		format1[i] = bigram_mod[format1[i]]
		format1[i] = trigram_mod[format1[i]]
		format1[i] = word_utility.lemmatize(format1[i])
	
	print("Building LDA model with Mallet")
	id2word = corpora.Dictionary(format1)
	texts = format1
	corpus = [id2word.doc2bow(text) for text in texts]
	lda_model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=7, id2word=id2word)
	lda_model = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(lda_model)
	pprint(lda_model.print_topics())
	'''

	#testing model with 300 posts in test.csv
	with open("test.csv", newline = '') as f: #read csv file
		reader = csv.reader(f)
		#remove empty rows
		doc = []
		for row in reader: 
			if row != []:
				doc.append(row)

	#convert csv tokens to one string
	for i in range(len(doc)):
		doc[i] = " ".join(doc[i])

	lda_model = gensim.models.LdaModel.load("model4")
	#lda_model = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(lda_model)
	#pprint(lda_model.print_topics()

	topic0 = []
	topic1 = []
	topic2 = []
	topic3 = []
	topic4 = []
	topic5 = []
	topic6 = []
	for post in doc:
		topicnumber = get_topic(lda_model,post)
		print(topicnumber)
		if(topicnumber == 1):
			topic1.append([post])
		elif(topicnumber == 2):
			topic2.append([post])
		elif(topicnumber == 3):
			topic3.append([post])
		elif(topicnumber == 4):
			topic4.append([post])
		elif(topicnumber == 5):
			topic5.append([post])
		elif(topicnumber == 6):
			topic6.append([post])
		elif(topicnumber == 0):
			topic0.append([post])
		else:
			print("Error")
			exit()
	
	[print("topic0: ", topic) for topic in topic0]
	[print("topic1: ", topic) for topic in topic1]
	[print("topic2: ", topic) for topic in topic2]
	[print("topic3: ", topic) for topic in topic3]
	[print("topic4: ", topic) for topic in topic4]
	[print("topic5: ", topic) for topic in topic5]
	[print("topic6: ", topic) for topic in topic6]
	
	pprint(lda_model.print_topics())
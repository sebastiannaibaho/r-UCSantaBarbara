import word_utility
import csv

import gensim #pip install gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from pprint import pprint #pip install pprint
import pyLDAvis
import pyLDAvis.gensim
mallet_path = "mallet-2.0.8/bin/mallet"

if __name__ == '__main__':
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
	
	#lda_model = gensim.models.LdaModel.load("model")
	
	print("Building LDA model with Mallet")
	id2word = corpora.Dictionary(format1)
	texts = format1
	corpus = [id2word.doc2bow(text) for text in texts]
	lda_model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=10, id2word=id2word)
	lda_model.save("model")
	'''

	print("Building LDA model")
	id2word = corpora.Dictionary(format1)
	texts = format1
	corpus = [id2word.doc2bow(text) for text in texts]
	lda_model = gensim.models.ldamodel.LdaModel(corpus = corpus,id2word=id2word,num_topics=10,
		random_state=100,update_every=1,chunksize=1000,passes=10,alpha='auto',per_word_topics=True)
	pprint(lda_model.print_topics())
	doc_lda = lda_model[corpus]
	lda_model.save("model")

	'''

	print("Computing Coherence Score and Perplexity")
	coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=id2word, coherence='c_v')
	coherence_lda = coherence_model_lda.get_coherence()
	#print('\nPerplexity: ', lda_model.log_perplexity(corpus))
	print('Coherence Score: ', coherence_lda)

	'''

	def compute_coherence_values(dictionary, corpus, texts, start=4, stop=20, step=2):
		coherence_values = []
		model_list = []
		for num_topics in range(start,stop,step):
			print("Computing using %d topics" %num_topics)
			model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)
			model_list.append(model)
			coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
			cv = coherencemodel.get_coherence()
			coherence_values.append(cv)
			print("Num Topics =", num_topics, " has Coherence Value of", round(cv, 4))
		return model_list, coherence_values

	print("Computing coherence values")
	model_list, coherence_values = compute_coherence_values(id2word,corpus,texts)
	print("Done")
	count = 4
	for cv in coherence_values:
		print("Num Topics = ", count, " has Coherence Value of", round(cv, 4))
		count = count + 2

	'''


	lda_model = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(lda_model) #convert Mallet to ldaModel for pyLDAvis
	print("Preparing visual data") #this takes like 10 minutes
	vis_data = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
	print("Saving")
	pyLDAvis.save_html(vis_data,"visualizedLDA.html")
	

	'''
	This is using Mallet model with 30000 posts
	Not ideal

	Num Topics = 4  has Coherence Value of 0.4981
	Num Topics = 6  has Coherence Value of 0.5315
	Num Topics = 8  has Coherence Value of 0.5109
	Num Topics = 10  has Coherence Value of 0.53
	Num Topics = 12  has Coherence Value of 0.5241
	Num Topics = 14  has Coherence Value of 0.5354
	Num Topics = 16  has Coherence Value of 0.5241
	Num Topics = 18  has Coherence Value of 0.5223
	'''

	
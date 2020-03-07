import word_utility
import csv
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from pprint import pprint
import pyLDAvis
import pyLDAvis.gensim

mallet_path = "mallet-2.0.8/bin/mallet"

#Set to True to build with mallet lda model
#Set to False to build with gensim lda model
BUILD_WITH_MALLET = True

#number of topics for the lda model
NUM_TOPICS = 4

#name of file to save lda model and visual data 
SAVE_FILE = "model4_optimized"
VIS_DATA_SAVE_FILE = "visualizedLDA4_optimized.html"

def compute_coherence_values(dictionary, corpus, texts, start=NUM_TOPICS, stop=9, step=1):
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
	
def compute_alpha_values(dictionary, corpus, texts, start=40, stop=110, step=10):
	coherence_values = []
	for alpha in range (start,stop,step):
		print("Computing using", NUM_TOPICS, "topics and alpha =",alpha)
		model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=NUM_TOPICS, id2word=id2word, alpha = alpha)
		coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
		cv = coherencemodel.get_coherence()
		coherence_values.append(cv)
		print("Model with alpha =", alpha, " has Coherence Value of", round(cv, 4))
	return coherence_values

if __name__ == '__main__':
	with open("subreddit_data.csv", newline = '') as f: #read csv file
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

	id2word = corpora.Dictionary(format1)
	texts = format1
	corpus = [id2word.doc2bow(text) for text in texts]

	if BUILD_WITH_MALLET:
		print("Building LDA model with Mallet")
		lda_model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=NUM_TOPICS, id2word=id2word,alpha = 90, optimize_interval=10)
		lda_model = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(lda_model) #convert Mallet to ldaModel 
		pprint(lda_model.print_topics())
		lda_model.save(SAVE_FILE)
	else: 
		print("Building LDA model with gensim")
		lda_model = gensim.models.ldamodel.LdaModel(corpus = corpus,id2word=id2word,num_topics=NUM_TOPICS,
			random_state=100,update_every=1,chunksize=1000,passes=10,alpha='auto',per_word_topics=True)
		pprint(lda_model.print_topics())
		doc_lda = lda_model[corpus]
		lda_model.save(SAVE_FILE)
	
	print("Computing Coherence Score and Perplexity")
	coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=id2word, coherence='c_v')
	coherence_lda = coherence_model_lda.get_coherence()
	if not BUILD_WITH_MALLET: 
		print('\nPerplexity: ', lda_model.log_perplexity(corpus))
	print('Coherence Score: ', coherence_lda)
	
	print("Computing coherence values with more topic numbers")
	model_list, coherence_values = compute_coherence_values(id2word,corpus,texts)
	print("Done")
	count = NUM_TOPICS
	for cv in coherence_values:
		print("Num Topics = ", count, " has Coherence Value of", round(cv, 4))
		count = count + 1
	
	print("Computing coherence value with more alpha values")
	coherence_values_alpha = compute_alpha_values(id2word,corpus,texts)
	print("Done")
	count = 40
	for cv in coherence_values_alpha:
		print("Alpha=", count, " has Coherence Value of", round(cv, 4))
		count = count + 10
	
	
	print("Preparing visual data")
	vis_data = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
	print("Saving")
	pyLDAvis.save_html(vis_data,VIS_DATA_SAVE_FILE)
	
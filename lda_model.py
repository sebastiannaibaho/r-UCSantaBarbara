import word_utility
import csv

import gensim #pip install gensim
import gensim.corpora as corpora
from pprint import pprint #pip install pprint
import pyLDAvis
import pyLDAvis.gensim

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

print("Building LDA model")
id2word = corpora.Dictionary(format1)
texts = format1
corpus = [id2word.doc2bow(text) for text in texts]
lda_model = gensim.models.ldamodel.LdaModel(corpus = corpus,id2word=id2word,num_topics=20,
	random_state=100,update_every=1,chunksize=100,passes=10,alpha='auto',per_word_topics=True)
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]
lda_model.save("model")

print("Preparing visual data") #this takes like 10 minutes
vis_data = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
print("Saving")
pyLDAvis.save_html(vis_data,"visualizedLDA.html")

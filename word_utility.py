import nltk #pip install nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

#remove stopwords
#PRECONDITION: Accepts a tokenized array of strings
#POSTCONDITION: Returns the input with stopwords removed
def remove_stopwords(tokenized_sentence):
	sw = set(stopwords.words('english'))
	for word in tokenized_sentence:
		if word not in sw:
			tokenized_sentence.remove(word)
	return tokenized_sentence

#lemmatize words
#PRECONDITION: Accepts a tokenized array of strings
#POSTCONDITION: Returns the lemmatized version of input
def lemmatize(tokenized_sentence):
	pos_tagged_sentence = nltk.pos_tag(tokenized_sentence)
	temp = []
	lmtzr = WordNetLemmatizer()
	for word,tag in pos_tagged_sentence:
		wntag = tag.lower()
		if wntag[0] == 'j':
			wntag = 'a'
		wntag = wntag[0] if wntag[0] in ['a','r','n','v'] else None
		temp.append(lmtzr.lemmatize(word,wntag) if wntag else word)
	return temp
 

'''
#count words and put into dict
d = {}
for row in format4:
	for word in row:
		if word in d:
			d[word] = d[word] + 1;
		else:
			d[word] = 1;

for key, value in sorted(d.items(), key=lambda item: item[1]):
    print("%s: %s" % (key, value))
 '''

import word_utility
import gensim
import re

def format_text(content):
    # links, and single quote
    remove = [r'\((.*?)\)\[(.*?)\]', r'\[(.*?)\]\((.*?)\)',
              r'(https?://)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=;]*)',
              '&amp;#(.*?);', "['\u2019]"]
    for r in remove:
        content = re.sub(r, '', content)

    content = content.replace('&amp', '&') 

    # get rid of everything except letters and numbers and ampersand (for now?)
    content = re.sub(r'[^\w&]+', ' ', content)

    # remove emojis and other languages
    content = re.sub(r'[^\x00-\x7f]', r'', content)

    return content

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
#POSTCONDITION: returns the topic distribution of the post
def get_topic(model, id2word, post):
	post = format_text(post).strip()
	
	doc = []
	doc.append([post])
	doc[0] = doc[0][0].split(" ")
	doc[0] = word_utility.remove_stopwords(doc[0])
	doc[0] = word_utility.lemmatize(doc[0])

	bow = [id2word.doc2bow(text) for text in doc]
	doc_topic_distribution = model.get_document_topics(bow[0])

	return doc_topic_distribution

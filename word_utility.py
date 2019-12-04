import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import gensim


def __sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


# makes lowercase and extracts tokens from the document
# PRECONDITION: The document array
# POSTCONDITION: Returns a tokenized array of strings
def tokenize(posts):
    return list(__sent_to_words(posts))


# remove stopwords
# PRECONDITION: Accepts a tokenized array of strings
# POSTCONDITION: Returns the input with stopwords removed
def remove_stopwords(tokenized_sentence):
    stop_words = stopwords.words('english')
    stop_words.extend(['im', 'ill', 'ive', 'really', 'doesnt', 'havnt', 'also'])  # idk you can get rid of this or add more
    sw = set(stop_words)

    temp = []
    for word in tokenized_sentence:
        if word not in sw:
            temp.append(word)
    return temp


# lemmatize words
# PRECONDITION: Accepts a tokenized array of strings
# POSTCONDITION: Returns the lemmatized version of input
def lemmatize(tokenized_sentence):
    pos_tagged_sentence = nltk.pos_tag(tokenized_sentence)
    temp = []
    lmtzr = WordNetLemmatizer()
    for word, tag in pos_tagged_sentence:
        wntag = tag.lower()
        if wntag[0] == 'j':
            wntag = 'a'
        wntag = wntag[0] if wntag[0] in ['a', 'r', 'n', 'v'] else None
        temp.append(lmtzr.lemmatize(word, wntag) if wntag else word)
    return temp

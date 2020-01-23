import pickle
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import chi2
from nltk.stem import WordNetLemmatizer

df = pd.read_pickle("output_df.pkl")
df['Content'] = df['Content'].fillna("")


# Stemming and Lemmatization
wnl = WordNetLemmatizer()
nrows = len(df)
lemmatized_text_list = []

for row in range(0, nrows):
    # Create an empty list containing lemmatized words
    lemmatized_list = []

    # Save the text and its words into an object
    text_words = df.iloc[row]['Content'].split(" ")
    #print(df.iloc[row]['Content'].split(" "))

    # Iterate through every word to lemmatize
    for word in text_words:
        lemmatized_list.append(wnl.lemmatize(word, pos="v"))

    # Join the list
    lemmatized_text = " ".join(lemmatized_list)

    # Append to the list containing the texts
    lemmatized_text_list.append(lemmatized_text)
df['Content_Parsed'] = lemmatized_text_list
df['Content_Parsed'] = df['Content_Parsed'].map(lambda x: x.lower())  # makes dataframe case insensitive

# Stop words
stop_words = list(stopwords.words('english'))
add_stop_words = ['us', 'etc', 'thank', 'thanks', 'like', 'anyone', 'everyone']
stop_words.extend(add_stop_words)
for stop_word in stop_words:
    regex_stopword = r"\b" + stop_word + r"\b"
    df['Content_Parsed'] = df['Content_Parsed'].str.replace(regex_stopword, '')


# let's try subsetting the dataframe with only posts with flairs already
df_sorted = pd.DataFrame({'Title': [], 'Content': [], 'Category': [], 'Content_Parsed': []})
i = 0
for row in range(0, nrows):
    if df.iloc[row]['Category'] is not None:
        df_sorted.loc[i] = df.iloc[row]
        i += 1
#print(df_sorted['Content_Parsed'])

# Label coding
"""
category_codes = {  # alphabetical order
    'Academic Life': 0,
    'Course Questions': 1,
    'Discussion': 2,
    'Employment': 3,
    'General Question': 4,
    'Humor': 5,
    'Incoming Students': 6,
    'IV/Goleta/SB': 7,
    'Meta': 8,
    'News': 9,
    'Social Life': 10,
}
"""
category_codes = {}
categories = list(set(df_sorted['Category']))
print(categories)
for i in range(0, len(categories)):
    category_codes.update({categories[i] : i})

# Category mapping
df_sorted['Category_Code'] = df_sorted['Category']

df_sorted = df_sorted.replace({'Category_Code': category_codes})
#print(df_sorted.head())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(df_sorted['Content_Parsed'],
                                                    df_sorted['Category_Code'],
                                                    test_size=0.01,  # low because of small sample size (for now)
                                                    random_state=8)


# Text representation (TF-IDF Vectors)
# Parameter election
ngram_range = (1, 2)
min_df = 10
max_df = 1.
max_features = 300
tfidf = TfidfVectorizer(encoding='utf-8',
                        ngram_range=ngram_range,
                        stop_words=None,
                        lowercase=False,
                        max_df=max_df,
                        min_df=min_df,
                        max_features=max_features,
                        norm='l2',
                        sublinear_tf=True)

features_train = tfidf.fit_transform(X_train).toarray()
labels_train = y_train
print(features_train.shape)

features_test = tfidf.transform(X_test).toarray()
labels_test = y_test
print(features_test.shape)
from sklearn.feature_selection import chi2
import numpy as np

for Product, category_id in sorted(category_codes.items()):
    features_chi2 = chi2(features_train, labels_train == category_id)
    indices = np.argsort(features_chi2[0])
    feature_names = np.array(tfidf.get_feature_names())[indices]
    unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
    bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
    print("# '{}' category:".format(Product))
    print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-5:])))
    print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-2:])))
    print("")

# Save files for later
# X_train
with open('Pickles/X_train.pickle', 'wb+') as output:
    pickle.dump(X_train, output)

# X_test
with open('Pickles/X_test.pickle', 'wb+') as output:
    pickle.dump(X_test, output)

# y_train
with open('Pickles/y_train.pickle', 'wb+') as output:
    pickle.dump(y_train, output)

# y_test
with open('Pickles/y_test.pickle', 'wb+') as output:
    pickle.dump(y_test, output)

# df
with open('Pickles/df.pickle', 'wb+') as output:
    pickle.dump(df, output)

# features_train
with open('Pickles/features_train.pickle', 'wb+') as output:
    pickle.dump(features_train, output)

# labels_train
with open('Pickles/labels_train.pickle', 'wb+') as output:
    pickle.dump(labels_train, output)

# features_test
with open('Pickles/features_test.pickle', 'wb+') as output:
    pickle.dump(features_test, output)

# labels_test
with open('Pickles/labels_test.pickle', 'wb+') as output:
    pickle.dump(labels_test, output)

# TF-IDF object
with open('Pickles/tfidf.pickle', 'wb+') as output:
    pickle.dump(tfidf, output)
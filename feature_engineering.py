import pickle
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import chi2
from nltk.stem import WordNetLemmatizer

df = pd.read_csv("output_df.csv", sep=';-', names=['Title', 'Content', 'Category'], engine='python')
df['Content'] = df['Content'].fillna("")


# Stemming and Lemmatization
wnl = WordNetLemmatizer()
nrows = len(df)
lemmatized_text_list = []

for row in range(0, nrows):
    # Create an empty list containing lemmatized words
    lemmatized_list = []

    # Save the text and its words into an object
    text_words = df.loc[row]['Content'].split(" ")

    # Iterate through every word to lemmatize
    for word in text_words:
        lemmatized_list.append(wnl.lemmatize(word, pos="v"))

    # Join the list
    lemmatized_text = " ".join(lemmatized_list)

    # Append to the list containing the texts
    lemmatized_text_list.append(lemmatized_text)
df['Content_Parsed'] = lemmatized_text_list


# Stop words
stop_words = list(stopwords.words('english'))
for stop_word in stop_words:

    regex_stopword = r"\b" + stop_word + r"\b"
    df['Content_Parsed'] = df['Content_Parsed'].str.replace(regex_stopword, '')


# let's try subsetting the dataframe with only posts with flairs already
df_sorted = pd.DataFrame({'Title': [], 'Content': [], 'Category': [], 'Content_Parsed': []})
i = 0
for row in range(0, nrows):
    if df.loc[row]['Category'] != "None":
        df_sorted.loc[i] = df.loc[row]
        i += 1


# Label coding
category_codes = {  # alphabetical order
    'Academic Life': 0,
    'Discussion': 1,
    'Employment': 2,
    'General Question': 3,
    'Humor': 4,
    'IV/Goleta/SB': 5,
    'Meta': 6,
    'News': 7,
    'Social Life': 8
}

# Category mapping
df_sorted['Category_Code'] = df_sorted['Category']
df_sorted = df_sorted.replace({'Category_Code': category_codes})
print(df_sorted.head())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(df_sorted['Content_Parsed'],
                                                    df_sorted['Category_Code'],
                                                    test_size=0.05,  # low because of small sample size (for now)
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

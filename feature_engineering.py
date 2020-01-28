import pickle
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import chi2
from nltk.stem import WordNetLemmatizer
import get_data

#df = get_data.get_data(10000, debug=True)
df = pd.read_json('dataframe.json', dtype=str)

# let's try subsetting the dataframe with only posts with flairs already
df_sorted = pd.DataFrame({'Title': [], 'Content': [], 'Id': [], 'Category': []})
i = 0
for row in range(0, len(df)):
    if df.iloc[row]['Category'] != 'None':
        df_sorted.loc[i] = df.iloc[row]
        i += 1

print(df_sorted.head())

# Label coding
category_codes = {}
categories = list(set(df_sorted['Category']))
[category_codes.update({categories[i]: i}) for i in range(0, len(categories))]
df_sorted['Category_Code'] = df_sorted['Category']
df_sorted = df_sorted.replace({'Category_Code': category_codes})
#print(df_sorted.head())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(df_sorted['Content'],
                                                    df_sorted['Category_Code'],
                                                    test_size=0.01,  # low because of small sample size (for now)
                                                    random_state=8)


# Text representation (TF-IDF Vectors)
# Parameter election
ngram_range = (1, 2)
min_df = 0.01
max_df = 0.5
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
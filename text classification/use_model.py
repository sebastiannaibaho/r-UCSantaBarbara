import pickle
import pandas as pd

import numpy as np

from Data.Functions.post_preprocessor import preprocess_posts as preprocess
from Data.Functions.word_utility import word_utility as word_utility
from Data.Functions.Post_Scraper import get_posts as get_posts

# SVM
path_svm = 'Models/best_rfc.pickle'
with open(path_svm, 'rb') as data:
    svc_model = pickle.load(data)

path_tfidf = 'Models/Pickles/tfidf.pickle'
with open(path_tfidf, 'rb') as data:
    tfidf = pickle.load(data)

category_codes = {
    'Humor': 0,
    'Social Life': 1,
    'News': 2,
    'Discussion': 3,
    'Meta': 4,
    'Incoming Students': 5,
    'General Question': 6,
    'Course Questions': 7,
    'Academic Life': 8,
    'Employment': 9,
    'IV/Goleta/SB': 10,
    'None': 11
}


def get_category_name(category_id):
    for category, id_ in category_codes.items():
        if id_ == category_id:
            return category


def predict_from_features(features):
    # Obtain the highest probability of the predictions for each article
    predictions_proba = svc_model.predict_proba(features).max(axis=1)

    # Predict using the input model
    predictions_pre = svc_model.predict(features)

    # Replace prediction with 6 if associated cond. probability less than threshold
    predictions = []

    for prob, cat in zip(predictions_proba, predictions_pre):
        if prob > .15:
            predictions.append(cat)
        else:
            predictions.append(11)

    # Return result
    categories = [get_category_name(x) for x in predictions]

    return categories


def create_features_from_df(post):
    print(post[0]['title'])
    print(post[0]['selftext'])
    print('\n\n')
    post, num_deleted = preprocess(post)

    df = pd.DataFrame(post, columns=post[0].keys())
    df['Content'] = word_utility(df['Content'])

    features = tfidf.transform(df).toarray()
    return features


# Get the scraped dataframes
df_features = [get_posts(10)[0][1]]

# Create features
features = create_features_from_df(df_features)

# Predict
predictions = predict_from_features(features)
print(predictions)

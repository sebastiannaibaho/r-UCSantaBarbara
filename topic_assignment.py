from Data.get_data import get_processed
import pandas as pd
import csv
import feature_engineering
from pprint import pprint #pip install pprint

with open('Data/AddedFlairs/unigrams.txt') as u:
    unigrams = u.read().splitlines()

topic_keys = ['Academic Life',
              'Course Questions',
              'Discussion',
              'Employment',
              'General Question',
              'Humor',
              'IV/Goleta/SB',
              'Incoming Students',
              'Meta',
              'News',
              'Social Life']

df_file = 'UCSantaBarbara_1580367940'
original = get_processed(df_file, read=True)
doc = pd.DataFrame(original)
print(len(doc))


def get_topic(point_dict, i):
    max_points = 0
    best_topic = ''
    for k, v in point_dict.items():
        #print(k + " has points " + str(v))
        if v > max_points:
            best_topic = k
            max_points = v
    if max_points > 0:
        doc.iloc[i]['Category'] = best_topic


# main_dict == {topic1: {unigram1: point value, unigram2: point value, ...}, topic2: ...}
# 1 point for first 5 words, 2 points for next 5, ... , 5 points for last 5 words in unigrams per topic
#   ratchet af i know but idk how to get/use the tfidf values yet
main_dict = {}
for i in range(0, len(topic_keys)):
    unigram_keys = {}
    for i in range(0, len(topic_keys)):
        unigram_keys = feature_engineering.get_unigrams(topic_keys[i])
        main_dict[topic_keys[i]] = unigram_keys

list_values = list(main_dict.values())

for m in range(0, len(doc)):
    point_dict = {}
    for j in range(0, len(topic_keys)):
        point_dict[topic_keys[j]] = 0
    if m % 1000 == 0:
        print('\r%d' % m, end='')
    for word in doc.iloc[m]['Content']:
        for k in range(0, len(topic_keys)):
            lst = list(list_values[k].keys())
            point = 0
            for unigram in lst:
                #print(unigram)
                if word == unigram:
                    point += list_values[k].get(word)
            point_dict[topic_keys[k]] += point
    get_topic(point_dict, m)


print('HERE')
print(len(doc[doc['Category'] != 'None']))

for i in range(0, len(original)):
    if original['Category'][i] == 'None':
        original.iloc[i]['Category'] = doc['Category'][i]

original.to_json('Data/AddedFlairs/' + df_file + 'ExtraFlairs.json')

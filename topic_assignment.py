import Data.Functions.word_utility as word_utility
import csv
import feature_engineering
from pprint import pprint #pip install pprint


# Topic assignment using Text Classification and ratchet algorithm


with open('unigrams.txt') as u:
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

# testing model with 300 posts in test.csv

with open("test.csv", newline='') as f:  # read csv file
    reader = csv.reader(f)
    # remove empty rows
    doc = []
    for row in reader:
        if row:
            doc.append(row)
    # convert csv tokens to one string
    for i in range(len(doc)):
        doc[i] = " ".join(doc[i])
    #pprint(doc)
# doc2 is 'refined' version of doc
doc2 = word_utility.word_utility(doc)
for i in range(0, len(doc2)):
    doc2[i] = " ".join(doc2[i])


def get_topic(point_dict):
    max_points = 0
    best_topic = ''
    for k, v in point_dict.items():
        print(k + " has points " + str(v))
        if v > max_points:
            best_topic = k
            max_points = v
        elif v == max_points:
            best_topic += ", " + k
    if max_points > 0:
        print(best_topic + ': ', end='')
    else:
        print('No match: ', end='')


def model():
    main_dict = {}
    for i in range(0, len(topic_keys)):
        unigram_keys = feature_engineering.get_unigrams(topic_keys[i])
        main_dict[topic_keys[i]] = unigram_keys

    list_values = list(main_dict.values())

    for m in range(0, len(doc2)):
        point_dict = {}
        for j in range(0, len(topic_keys)):
            point_dict[topic_keys[j]] = 0
        for word in doc2[m].split():
            for k in range(0, len(topic_keys)):
                lst = list(list_values[k].keys())
                point = 0
                for unigram in lst:
                    if word == unigram:
                        point += list_values[k].get(word)
                point_dict[topic_keys[k]] += point
        get_topic(point_dict)
        print(doc[m])
    return


print('')
model()

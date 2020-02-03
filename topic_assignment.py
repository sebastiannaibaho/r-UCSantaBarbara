import Data.Functions.word_utility as word_utility
import csv
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
        if row != []:
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
        #print(k + " has points " + str(v))
        if v > max_points:
            best_topic = k
            max_points = v
        elif v == max_points:
            best_topic += ", " + k
    if max_points > 0:
        print(best_topic + ': ', end='')
    else:
        print('No match: ', end='')


# main_dict == {topic1: {unigram1: point value, unigram2: point value, ...}, topic2: ...}
# 1 point for first 5 words, 2 points for next 5, ... , 5 points for last 5 words in unigrams per topic
#   ratchet af i know but idk how to get/use the tfidf values yet
def model():
    main_dict = {}
    for i in range(0, len(topic_keys)):
        unigram_keys = {}
        for j in range(0, len(unigrams) // len(topic_keys)):
            unigram_keys[(unigrams[i * 25 + j])] = (j // 5) + 1
        main_dict[topic_keys[i]] = unigram_keys

    list_values = list(main_dict.values())

    for m in range(0, len(doc2)):
        point_dict = {}
        for j in range(0, len(topic_keys)):
            point_dict[topic_keys[j]] = 0
        for word in doc2[m].split():
            #print(word)
            for k in range(0, len(topic_keys)):
                lst = list(list_values[k].keys())
                point = 0
                for unigram in lst:
                    #print(unigram)
                    if word == unigram:
                        point += list_values[k].get(word)
                point_dict[topic_keys[k]] += point
        get_topic(point_dict)
        print(doc[m])
    return


print('')
model()

import csv
import json
import math
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

#import spacy

# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from nltk.corpus import stopwords
stop_words = stopwords.words('english')
#stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

# If you put -1 for num_posts, then the program will run until the FIRST_POST_UTC time which is defaulted to beginning
# of the subreddit. Not too bad with USE_REDDIT_API set to False
NUM_POSTS = 15000

OUTPUT_FILE = "output.csv"

# The amount of posts received for each request to pushshift, max is 1000
POSTS_PER_REQUEST = 1000


def get_posts_from_url(url):
    response = urllib.request.urlopen(url)
    web_content = response.read()
    return json.loads(web_content)['data']


def valid_post(content):
    deleted_terms = ['None', '[deleted]', '[removed]', '']  # the empty string gets rid of image posts
    return content not in deleted_terms


def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


def format_text(content):
    try:
        remove = ['\'', "\\(.*\\)\\[.*\\]", "\\[.*\\]\\(.*\\)", "https?://[a-zA-Z0-9\\./\\?\\-]+"]

        for r in remove:
            content = re.sub(r, '', content)
        content = re.sub('\s+', ' ', content)

        emoji_pattern = re.compile("["
                                  u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        content = emoji_pattern.sub(r'', content)

        return content
    except UnicodeEncodeError:
        return ""


def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


def print_posts_with_pushshift(input, fn):
    count = 0
    ps = []
    for p in input:
        if 'selftext' in p:
            ps.append(format_text(p['selftext']))
        else:
            count += 1

    ps = list(sent_to_words(ps))
    wr = csv.writer(fn)

    for p in ps:
        try:
            wr.writerow(p)
        except UnicodeEncodeError:
            count += 1

    return count


# The max can only be 1000, posts_per_request should not be used for remainder of code
# this shouldn't really matter but idk seems better to do this
size_per_request = POSTS_PER_REQUEST if POSTS_PER_REQUEST < 1000 else 1000

PS_URL = 'https://api.pushshift.io/reddit/search/submission/?subreddit=UCSantaBarbara&sort=desc&sort_type=created_utc'
FIRST_POST_UTC = '1305484091'  # Utc time of very first post, I just changed sort to "asc" to get this
                               # you can change this to any other value to get posts up to this point
CURRENT_TIME_UTC = math.floor((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())
# this is the first post we want to start at (currently set to now)
last_date = f'&before={CURRENT_TIME_UTC}'
# last_date = "&before=SOME_UTC_TIME"

count = 0
posts = []
# Because we can only make a max request of 1000 posts at a time, we have to loop through each batch of posts
while (FIRST_POST_UTC not in last_date) and (NUM_POSTS == -1 or count < NUM_POSTS):
    request_size = size_per_request if NUM_POSTS < 0 or NUM_POSTS - count > size_per_request else NUM_POSTS - count

    posts += get_posts_from_url(PS_URL + last_date + '%20&size=' + str(request_size))

    count += request_size
    print('Requested %d posts from pushshift.\n' % count)

    last_date = '&before=' + str(posts[-1]['created_utc'])


f = open(OUTPUT_FILE, 'w')
num_deleted = print_posts_with_pushshift(posts, f)
f.close()

if num_deleted:
    print('%d posts were deleted.' % num_deleted)
print('Displayed %d posts' % (len(posts) - num_deleted))

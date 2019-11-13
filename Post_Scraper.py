import json
import math
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
import praw
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#
# Using the reddit api gets us comments, but is really slow. I only have it getting the top level comments (which
# defeats the purpose pretty much) if we really wanted to we could also get replies to comments for as many levels
# as needed, well see
#
# If we print to a file then we'd have to figure out what to do with emojis (right now im just not including this
# posts), however these posts are shown when printed to screen
#
# You can change FIRST_POST_UTC or CURRENT_TIME_UTC to select the time period you want to request from (line 132:)
#

USE_REDDIT_API = False  # true will use the api and also include comments
PRINT_TO_FILE = True  # false will print info to screen
CREATE_CSV = True  # have true for writing csv files (using pushshift)

# If you put -1 for num_posts, then the program will run until the FIRST_POST_UTC time which is defaulted to beginning
# of the subreddit. Not too bad with USE_REDDIT_API set to False
NUM_POSTS = 1000

OUTPUT_FILE = "output.csv"  # change to .csv
OUTPUT_LINE_WIDTH = 120
FORMAT_TEXT = True  # makes the lines not exceed OUTPUT_LINE_WIDTH
VISUALS = True  # true if you want to create/display visuals

# The amount of posts received for each request to pushshift, max is 1000
POSTS_PER_REQUEST = 1000


def get_posts_from_url(url):
    response = urllib.request.urlopen(url)
    web_content = response.read()
    return json.loads(web_content)['data']


def valid_post(content):
    deleted_terms = ['None', '[deleted]', '[removed]', '']  # the empty string gets rid of image posts
    return content not in deleted_terms


def format_text(content, width):  # limits the line width, tail recursion l8r?
    if not FORMAT_TEXT:
        return content

    content = re.sub('\n', ' ', content)
    content = re.sub(' +', ' ', content)
    if len(content) <= width:
        return content

    i = 0
    for i in range(width, -1, -1):
        if content[i] == ' ':
            break
    # if word (links for example) are longer than width just do max amount:
    i = i if i > 0 else width
    return content[0:i] + '\n' + format_text(content[(i + 1):], width)


def fuck_emojis(fn, str, input):
    # if you try to print out emojis to a file then things go wrong and you can change the encoding but then
    # like newlines dont work and i don't want to deal with it
    try:
        if len(input) == 4:  # posts
            fn(str % (input[0], input[1], input[2], format_text(input[3], OUTPUT_LINE_WIDTH)))
        elif len(input) == 3:  # .csv writing
            fn(str % (input[0], format_text_csv(input[1]), input[2]))
        else:  # comments
            fn(str % (input[0], input[1], re.sub('\n', '\n   ', format_text(input[2], OUTPUT_LINE_WIDTH - 3))))
        return 0
    except UnicodeEncodeError:
        print('Removed Post Because of Emoji issues')
    return 1


REDDIT = praw.Reddit(client_id='QDezWGnW8PleqQ',
                     client_secret='jxB-T64tt0qSJXDi-UTLTvyQiLg',
                     password='es3UWhEw',  # TODO: delete when pushing to git
                     redirect_uri='http://localhost:8080',
                     user_agent='AutoTagger by /u/UCSB_bot',
                     username='UCSB_Bot')


def print_posts_with_api(ps, fn):
    ids = [f't3_{p["id"]}' for p in ps]

    deleted = 0
    submissions = []

    for i in range(0, math.ceil(len(ids) / 1000)):
        lower = i * 1000
        upper = lower + 1000 if lower + 1000 < len(ids) else len(ids)
        print('Loading posts %d - %d from api' % (lower + 1, upper))
        submissions += REDDIT.info(ids[lower:upper])  # you can request 1000 at a time
    print()

    for submission in submissions:
        if valid_post(submission.selftext):
            did_not_print = fuck_emojis(fn, '"%s" by %s (%d):\n%s\n', [submission.title, submission.author,
                                                                       submission.score, submission.selftext])
            deleted += did_not_print
            if not did_not_print:
                submission.comment_sort = 'new'
                for comment in submission.comments:
                    if valid_post(comment.body):
                        fuck_emojis(fn, '%s (%d):\n   %s\n', [comment.author, comment.score, comment.body])
                fn('-------------------------------------\n')
        else:
            deleted += 1

    return deleted


def print_posts_with_pushshift(ps, fn):
    deleted = 0

    for p in ps:
        if valid_post(p['selftext']):
            if CREATE_CSV:
                if p['link_flair_richtext']:
                    did_not_print = fuck_emojis(fn, '"%s";-%s;-%s\n', [p['title'], p['selftext'], p['link_flair_text']])
                else:
                    did_not_print = fuck_emojis(fn, '"%s";-%s;-%s\n', [p['title'], p['selftext'], None])
                deleted += did_not_print
            else:
                did_not_print = fuck_emojis(fn, '"%s" by %s (%d):\n%s\n', [p['title'], p['author'], p['score'],
                                                                       p['selftext']])
                deleted += did_not_print
            if not did_not_print and not CREATE_CSV:
                fn('--------------------------------------\n')
        else:
            deleted += 1

    return deleted


def format_text_csv(content):  # formatting for .csv file
    content = content.replace('\n', '')  # delete existing new lines so everything is on one line
    return content


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

if PRINT_TO_FILE:
    f = open(OUTPUT_FILE, 'w')  # okay i changed this to write but i'm not sure if you wanted to keep append maybe we
                                 # just change it for what we want to use?  -Edward
if USE_REDDIT_API:
    num_deleted = print_posts_with_api(posts, f.write if PRINT_TO_FILE else print)
else:
    num_deleted = print_posts_with_pushshift(posts, f.write if PRINT_TO_FILE else print)

if VISUALS:
    df = pd.read_csv(OUTPUT_FILE, sep=';-', names=['Title', 'Content', 'Category'])
    #print(df['Title'].size)
    sns.countplot(x='Category', data=df)
    plt.show()

if PRINT_TO_FILE:
    f.close()

if num_deleted:
    print('%d posts were deleted.' % num_deleted)
print('Displayed %d posts' % (len(posts) - num_deleted))
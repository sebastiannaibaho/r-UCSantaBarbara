import urllib
import json
import math
from datetime import datetime
import nltk.corpus  # for some reason you need this ??? the urllib.request won't work without

# ################################################################################## #
# Call: get_posts() to get posts from pushshift                                      #
# posts, last_date = get_posts(num_posts, debug=False, last_date=CURRENT_BY_DEFAULT) #
# or: posts = get_posts(num_posts, debug=False, last_date=CURRENT_BY_DEFAULT)[0]     #
#                                                                                    #
# Call: get_comments() to get the comments for the post                              #
#                                                                                    #
# ################################################################################## #

PS_URL = 'https://api.pushshift.io/reddit/search/submission/?subreddit=UCSantaBarbara&sort=desc&sort_type=created_utc'

# The amount of posts received for each request to pushshift, max is 1000
POSTS_PER_REQUEST = 1000

# The max can only be 1000, posts_per_request should not be used for remainder of code
# this shouldn't really matter but idk seems better to do this
SIZE_PER_REQUEST = POSTS_PER_REQUEST if POSTS_PER_REQUEST < 1000 else 1000

current_time_utc = math.floor((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())
# this is the first post we want to start at (currently set to now)


def __get_posts_from_url(url):
    response = urllib.request.urlopen(url)
    web_content = response.read()
    return json.loads(web_content)['data']


# If you put -1 for num_posts, then the program will run until the FIRST_POST_UTC time which is defaulted to beginning
# of the subreddit.
def get_posts(num_posts, debug=False, last_date=current_time_utc, first_date=1305484091):
    # first_date is defaulted to the Utc time of very first post
    # last_date = "&before=SOME_UTC_TIME"

    count = 0
    posts = []
    # Because we can only make a max request of 1000 posts at a time, we have to loop through each batch of posts
    while (first_date < last_date) and (num_posts == -1 or count < num_posts):
        request_size = SIZE_PER_REQUEST if (num_posts == -1 or num_posts - count > SIZE_PER_REQUEST) else num_posts - count
        next_posts = __get_posts_from_url(PS_URL + '&before=' + str(last_date + 1) + '%20&size=' + str(request_size))

        last_date = next_posts[-1]['created_utc']
        if last_date < first_date:
            for i in range(0, len(next_posts)):
                if next_posts[i]['created_utc'] < first_date:
                    break
            next_posts = next_posts[0:i]

        count += len(next_posts)
        if debug:
            print('\rRequested %d posts from pushshift.' % count, end='')
        posts += next_posts

    if debug:
        print()

    return posts, last_date


def get_comments(ids, top_level_only=True, debug=False):
    # if you set sort by score = False then it is utc descending by default
    ps = 'https://api.pushshift.io/reddit/comment/search/?subreddit=UCSantaBarbara&link_id='

    comments = []
    for i in range(0, len(ids), 500):  # i think i read somewhere on the api that its a 500 max?
        j = i + 500 if len(ids) - i > 500 else len(ids)

        id_link = ','.join(ids[i:j])
        comments.extend(__get_posts_from_url(ps + id_link + '&size=500'))

        if debug:
            print('\rRequested %d comments from pushshift.' % j, end='')

    if debug:
        print()

    output = [[] for i in range(len(ids))]

    for comment in comments:
        i = ids.index(comment['link_id'][3:])
        if (not top_level_only) or (comment['link_id'] == comment['parent_id']):
            output[i].append(comment)

    return output

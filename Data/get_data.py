import Post_Scraper
import word_utility
import post_preprocessor
import pandas as pd
import os

# returns a data frame of:
# Title (as on the post)
# title + posts + comments processed and lemmatized and all
# post id
# flair

# subreddits = ['UCSantaBarbara', 'ucla', 'UCSC', 'USC', 'UCDavis', 'UCI', 'UCSD', 'berkeley', 'CalPoly', 'SBCC']


def get_raw(num_posts, top_level_only=False, debug=False, subreddit='UCSantaBarbara'):
    posts, ld = Post_Scraper.get_posts(num_posts, debug=debug, subreddit=subreddit)
    comments = Post_Scraper.get_comments([p['id'] for p in posts], top_level_only=top_level_only, debug=debug,
                                         subreddit=subreddit)

    if debug:
        num_comments = 0
        problems = 0
        for c in posts:
            try:
                if c['num_comments'] > 0:
                    num_comments += 1
            except IndexError:
                problems += 1
                print('problem with' + c['title'] + ' ' + c['id'])

        print("Problems: " + str(problems))
        print("Number of posts with comments (get_data): %d." % num_comments)

    result = []
    problems = 0
    for i in range(0, len(posts)):
        try:
            cat = posts[i]['link_flair_richtext'][0]['t']
        except (KeyError, IndexError):
            cat = 'None'

        try:
            result.append({
                'title': posts[i]['title'],
                'selftext': posts[i]['selftext'],
                'comments': [c['body'] for c in comments[i]] if (comments and len(comments[i])) else [],
                'category': cat,
                'id': posts[i]['id'],
                'created_utc': posts[i]['created_utc']
            })
        except KeyError:
            problems += 1

    print("Problems (posts w/o selftext): %d" % problems)
    result = list_to_df(result)

    result.to_json('Raw/' + subreddit + '_' + str(posts[0]['created_utc']) + '.json')


def get_processed(df_file, debug=False, read=False, write=False):
    if read:
        return pd.read_json('Processed/' + df_file, dtype=str)

    df = pd.read_json('Raw/' + df_file, dtype=str)

    if debug:
        print("loaded: %s." % df_file)

    result, num_deleted = post_preprocessor.preprocess_posts(df)
    result = list_to_df(result)

    if debug: print("calling utility")
    result['Content'] = word_utility.word_utility(result['Content'])

    if debug:
        print("writing to file.")

    if write:
        result.to_json('Processed/' + df_file)

    if debug:
        print('Number of deleted posts: %d.' % num_deleted)

    return result


def list_to_df(arr):
    variables = arr[0].keys()
    return pd.DataFrame(arr, columns=variables)


'''
for s in subreddits:
    print("Getting subreddit: %s." % s)
    get_raw(-1, debug=True, subreddit=s)
'''
'''
files = os.listdir("Raw")
print(files)
[get_processed(f, debug=True, write=True) for f in files]
'''

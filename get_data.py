import Post_Scraper
import word_utility
import post_preprocessor
import pandas as pd

# returns a data frame of:
# Title (as on the post)
# title + posts + comments processed and lemmatized and all
# post id
# flair


def get_data(num_posts, top_level_only=False, debug=False, filename=''):
    posts, ld = Post_Scraper.get_posts(num_posts, debug=debug)
    comments = Post_Scraper.get_comments([p['id'] for p in posts], top_level_only=top_level_only, debug=debug)

    if debug:
        num_comments = 0
        for c in posts:
            if c['num_comments'] > 0:
                num_comments += 1
        print("Number of posts with comments (get_data): %d." % num_comments)

    result, num_deleted = post_preprocessor.preprocess_posts(posts, comments)
    result = list_to_df(result)
    result['Content'] = word_utility.word_utility(result['Content'])

    if filename:
        result.to_json(filename)

    if debug:
        print('Number of deleted posts: %d.' % num_deleted)

    return result


def list_to_df(arr):
    variables = arr[0].keys()
    return pd.DataFrame(arr, columns=variables)

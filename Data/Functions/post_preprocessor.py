import re
import pandas as pd

# ########################################################### #
# Call: preprocess_posts to get the valid and formatted posts #
# eg.   posts, num_deleted = preprocess_posts(posts)          #
# ########################################################### #


# i hope images are the only thing w/o text
def __is_image(post):
    return post['selftext'] == ''


# verify that the post has content
def __valid_post(content):
    deleted_terms = ['none', '[deleted]', '[removed]', ' ']
    return content not in deleted_terms


# remove unnecessary things in the post
def __format_text(content):
    # links, and single quote
    remove = [r'\((.*?)\)\[(.*?)\]', r'\[(.*?)\]\((.*?)\)',
              r'(https?://)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=;]*)',
              '&amp;#(.*?);', "['\u2019]"]
    for r in remove:
        content = re.sub(r, '', content)

    content = content.replace('&amp', '&')  # idk what to do about ampersands because if they are used in place of 'and'
                                            # then that is a stopward and should be removed, but they may be used as in
                                            # 'l&s' for letters and science

    # get rid of everything except letters and numbers and ampersand (for now?)
    content = re.sub(r'[^\w&]+', ' ', content)

    # remove emojis and other languages
    content = re.sub(r'[^\x00-\x7f]', r'', content)

    return content


# removes bad posts and applies the format_text function
def preprocess_posts(posts, comments=None):  # comments is an array of just the body of text
    num_deleted = 0
    n22_deleted = 0
    result = []

    for i in range(len(posts)):
        if i % 1000 == 0:
            print("\rprocessed %d posts." % i, end='')

        if isinstance(posts, pd.DataFrame):
            # if passing in data frame
            post = posts.iloc[i]
            comment = ' '.join(post['comments'])
        else:
            # if passing in data directly from pushshift
            post = posts[i]
            comment = ' '.join(c['body'] for c in comments[i]) if (comments and len(comments[i])) else ''

        try:
            if __is_image(post):
                post['category'] = 'Image'

            if __valid_post(post['selftext']) and __valid_post(__format_text(post['selftext'])):
                try:
                    cat = post['link_flair_richtext'][0]['t']
                except (KeyError, IndexError):
                    cat = 'None'

                result.append({
                    'Title': post['title'],
                    # I'm just adding the title in front of the text:
                    'Content': __format_text(post['title'] + ' ' + post['selftext'] + ' ' + comment),
                    'Id': post['id'],
                    'Category': cat
                })
            else:
                num_deleted += 1
        except KeyError:
            n22_deleted += 1

    print("num_deleted: %d, n22_deleted: %d." % (num_deleted, n22_deleted))
    return result, num_deleted

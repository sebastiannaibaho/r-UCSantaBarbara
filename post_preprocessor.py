import re

# ########################################################### #
# Call: preprocess_posts to get the valid and formatted posts #
# eg.   posts, num_deleted = preprocess_posts(posts)          #
# ########################################################### #


# verify that the post has content
def __valid_post(content):
    deleted_terms = ['none', '[deleted]', '[removed]', '', ' ']
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
    result = []

    for i in range(len(posts)):

        post = posts[i]

        comment = comments[i] if comments else ""

        if __valid_post(post['selftext']) and __valid_post(__format_text(post['selftext'])):
            # I'm just adding the title in front of the text
            result.append(__format_text(post['title'] + ' ' + post['selftext'] + ' ' + comment))
        else:
            num_deleted += 1

    return result, num_deleted



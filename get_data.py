import Post_Scraper
import word_utility
import post_preprocessor

posts, ld = Post_Scraper.get_posts(-1, debug=True)
comments = Post_Scraper.get_comments([p['id'] for p in posts], top_level_only=False, debug=True)

result, num_deleted = post_preprocessor.preprocess_posts(posts, comments)
output = word_utility.word_utility(result)

print('Writing csv file...')
with open('posts_comments.csv', 'w') as f:
    for post in output:
        line = ','.join(post)
        f.write(line + '\n')

print('Number of deleted posts: %d.' % num_deleted)
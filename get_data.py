import Post_Scraper
import word_utility
import post_preprocessor
import time

posts, ld = Post_Scraper.get_posts(-1, True)
comments = []

for i in range(len(posts)):
    comment = ""

    if i != 0 and i % 20 == 0:
        result, num_deleted = post_preprocessor.preprocess_posts(posts[(i - 20):i], comments)
        output = word_utility.word_utility(result)
        comments = []

        with open('posts_comments.csv', 'a') as f:
            for o in output:
                for j in range(len(o)):
                    f.write("%s" % o[j])
                    if j != len(o) - 1:
                        f.write(',')
                f.write("\n")

        time.sleep(3)

    for c in Post_Scraper.get_comments(posts[i]["id"], True):
        comment += c["body"]
    comments.append(comment)

    print("\rGetting comment %d" % (i + 1), end="")
print()
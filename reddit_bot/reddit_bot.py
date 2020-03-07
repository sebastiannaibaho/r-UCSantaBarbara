import praw
import time
import bot_use_lda
import gensim

#sensitive info is censored here
CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
USERNAME = 'username'
PASSWORD = 'password'

SUBREDDIT = "Datasciencetest"

#global instances of lda model
MODEL = ""

#dictionary for correlating topic numbers with flairs
d = {
    0:"General", #General
    1:"IV/Social", #Academic
    2: "Academic", #Discussion
    3: "Discussion" #IV/Social
}

def main():
    reddit = praw.Reddit(user_agent='Flair Bot',
                        client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        username= USERNAME, password=PASSWORD)
    
    subreddit = reddit.subreddit(SUBREDDIT)

    #Load component for model
    global MODEL
    MODEL = gensim.models.LdaModel.load("model4_optimized")
    starttime = time.time()
    #endlessly receive stream of new submissions
    print("Waiting for new posts...")
    for submission in subreddit.stream.submissions():
        #only process posts that are created after script is started
        if submission.created_utc < starttime:
            continue
        process_submission(submission)

def process_submission(submission):
    if(submission.link_flair_text == None and submission.is_self):
        post = submission.title + " " + submission.selftext
        post = post.lower()
        post = post.strip()

        topic_distributions = bot_use_lda.get_topic(MODEL,MODEL.id2word,post)
        topic = bot_use_lda.get_top_topic(topic_distributions)
        flair = d[topic[0]]
        print("\nPost:\n[", post, "]\nwith topic distributions:")
        print(topic_distributions)
        print("flaired with", flair)
        submission.mod.flair(text=flair)

if __name__ == '__main__':
    main()
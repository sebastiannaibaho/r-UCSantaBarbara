#Testing code for the reddit bot

import praw
import time
import bot_use_lda
import gensim
import pickle

#we might want to hide this info somehow if we're uploading all our code on github
CLIENT_ID = 'w9kubT5JEFbjRg'
CLIENT_SECRET = 'ZkXMOhZQWpcjsTpz0G8LajiVAOU'
USERNAME = 'BotTestQwerty'
PASSWORD = 'Bluebear55'

#global instances of lda model and corpus
MODEL = ""
ID2WORD = ""

def main():
    reddit = praw.Reddit(user_agent='Test bot',
                        client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        username= USERNAME, password=PASSWORD)
    
    subreddit = reddit.subreddit('Datasciencetest')

    #Load components for model
    global MODEL, ID2WORD
    MODEL = gensim.models.LdaModel.load("model4")
    ID2WORD = pickle.load(open("id2word","rb"))

    starttime = time.time()
    #endlessly receive stream of new submissions
    print("waiting for new posts")
    for submission in subreddit.stream.submissions():
        #only process posts that are created after script is started
        if submission.created_utc < starttime:
            continue
        process_submission(submission)

def process_submission(submission):
    #Filler flair for now
    FLAIR = 'Academic Life'
    if(submission.link_flair_text == None):
        #TODO:
        #Need to process post into either lda or text classifcation model
        #and assign appropriate flair

        post = submission.title + " " + submission.selftext
        post = post.lower()
        post = post.strip()
        topic = bot_use_lda.get_topic(MODEL,ID2WORD,post)
        print(topic)
        #submission.mod.flair(text=FLAIR)

if __name__ == '__main__':
    main()
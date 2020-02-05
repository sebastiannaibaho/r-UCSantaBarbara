#Testing code for the reddit bot

import praw
import time

CLIENT_ID = 'w9kubT5JEFbjRg'
CLIENT_SECRET = 'ZkXMOhZQWpcjsTpz0G8LajiVAOU'
USERNAME = 'BotTestQwerty'
PASSWORD = 'Bluebear55'

def main():
    reddit = praw.Reddit(user_agent='Test bot',
                        client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        username= USERNAME, password=PASSWORD)
    
    subreddit = reddit.subreddit('Datasciencetest')

    starttime = time.time()
    #endlessly receive stream of new submissions
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
        submission.mod.flair(text=FLAIR)

if __name__ == '__main__':
    main()
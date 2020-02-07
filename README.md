# 2/6/2020 Meeting

### Things to do:
* ~~Scrape all flaired posts to train a topic model so that each flair will have its own group of keywords~~
* How to get a text classification model? (What Python library can do this?)
* Potential already-existing library of words for topics?
* ~~MAYBE: scrape data from other UC subreddits to improve our models~~
* ~~Scrape flaired posts from other UC subreddits~~

### Text classification approach:
* Use tf-idf to score each post, ranking the flairs from most relevant to least relevant
* Assign the most relevant flair to that post

### Topic modeling approach:
* Overlap some topics in order to improve the coherence score
* Look up other ways to improve the coherence score

### Reddit bot:
* Keep working on getting it to work
* Auto-flairing with praw

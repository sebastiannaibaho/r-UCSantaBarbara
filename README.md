# 1/21/2020 Meeting

### Things to do:

* Scrape all flaired posts to train a topic model so that each flair will have its own group of keywords (completed)
* How to get a text classification model? (What Python library can do this?)
* Potential already-existing library of words for topics?

### Text classification approach:
* Use tf-idf to score each post, ranking the flairs from most relevant to least relevant
* Assign the most relevant flair to that post

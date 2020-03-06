# UCSB Subreddit Topic Modeling Algorithm

## **Abstract**
This project uses an unsupervised machine learning model to categorize posts in the UCSB subreddit. We then created a bot which automatically flairs new posts within the appropriate topic. We extract Reddit post data through [pushshift.io](https://pushshift.io/). The data was trained on [gensim’s LDA Mallet model wrapper](https://radimrehurek.com/gensim/models/wrappers/ldamallet.html). Visualizations were done in [pyLDAvis](https://pyldavis.readthedocs.io/en/latest/). We experimented with several other models (LDA, tf-idf, biterm, GSDMM) and determined that the Mallet model was most accurate. 

## **Motivation**


## **Methodology**


## **Abstract**


## **Key Results**


## **Summary**


## **Future Work**

### Touch-Ups
* Use the Mallet model to make the TF-IDF model more accurate
* (1) Mallet model assigns a post to a number
* (2) Depending on the number assigned to that post, run the post through TF-IDF and eliminate irrelevant topics when running it

# UCSB Subreddit Topic Modeling Algorithm

## **Abstract**
This project uses an unsupervised machine learning model to categorize posts in the UCSB subreddit. We then created a bot which automatically flairs new posts within the appropriate topic. We extract Reddit post data through [pushshift.io](https://pushshift.io/). The data was trained on [gensim’s LDA Mallet model wrapper](https://radimrehurek.com/gensim/models/wrappers/ldamallet.html). Visualizations were done in [pyLDAvis](https://pyldavis.readthedocs.io/en/latest/). We experimented with several other models (LDA, tf-idf, biterm, GSDMM) and determined that the Mallet model was most accurate. 

## **Motivation**


## **Methodology**
### Data Collection
Posts were collected through pushshift.io. We considered only text posts and omitted link posts and image posts. Posts were cleaned by removing punctuation, special characters, and emojis and converting all letters to lowercase. The data was then tokenized and saved into a .csv file. The final data looked like the following:
|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|
|syllabus     |for    |pstat  |and|pstat |does|anyone|have|the          |syllabus|for   |these|two|classes|this|quarter|
|environmental|studies|looking|to |change|my  |major |to  |environmental|studies |anyone|have |any|advice |or  |input  |on|the|major|


## **Key Results**


## **Summary**


## **Future Work**

### Touch-Ups
* Use the Mallet model to make the TF-IDF model more accurate
* (1) Mallet model assigns a post to a number
* (2) Depending on the number assigned to that post, run the post through TF-IDF and eliminate irrelevant topics when running it

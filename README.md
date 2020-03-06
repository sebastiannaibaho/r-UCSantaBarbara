# UCSB Subreddit Topic Modeling Algorithm

## **Abstract**
This project uses an unsupervised machine learning model to categorize posts in the UCSB subreddit. We then created a bot which automatically flairs new posts within the appropriate topic. We extract Reddit post data through [pushshift.io](https://pushshift.io/). The data was trained on [gensim’s LDA Mallet model wrapper](https://radimrehurek.com/gensim/models/wrappers/ldamallet.html). Visualizations were done in [pyLDAvis](https://pyldavis.readthedocs.io/en/latest/). We experimented with several other models (LDA, tf-idf, biterm, GSDMM) and determined that the Mallet model was most accurate. 

## **Motivation**
Reddit is a popular social news platform that allows communities to discuss and vote on content that users submit. Our school’s subreddit, /r/UCSantaBarbara, is cluttered and unorganized. Currently more than 15,000 thousand members are on the UCSB subreddit and numerous posts are being added daily. Realizing that our school’s subreddit has the potential to be much more resourceful than it currently is, we decided that it would be helpful to create a model to organize its posts. 
![UCSB Subreddit](/markdown-assets/ucsb_subreddit.png)

## **Methodology**
### Data Collection
Posts were collected through pushshift.io. We considered only text posts and omitted link posts and image posts. Posts were cleaned by removing punctuation, special characters, and emojis and converting all letters to lowercase. The data was then tokenized and saved into a .csv file. The final data looked like the following:
| syllabus      | for     | pstat   | and  | pstat    | does | anyone | have | the           | syllabus | for    | these | two | classes | this  | quarter |        |     |       |    |     |      |     |      |    |      |     |        |    |     |    |       |      |     |         |      |      |      |          |    |        |    |      |    |      |       |     |      |        |     |      |     |    |     |    |    |       |    |    |     |    |     |        |          |      |     |     |      |    |     |       |    |       |    |        |      |      |     |    |      |      |      |     |         |         |      |     |     |     |      |    |     |
|---------------|---------|---------|------|----------|------|--------|------|---------------|----------|--------|-------|-----|---------|-------|---------|--------|-----|-------|----|-----|------|-----|------|----|------|-----|--------|----|-----|----|-------|------|-----|---------|------|------|------|----------|----|--------|----|------|----|------|-------|-----|------|--------|-----|------|-----|----|-----|----|----|-------|----|----|-----|----|-----|--------|----------|------|-----|-----|------|----|-----|-------|----|-------|----|--------|------|------|-----|----|------|------|------|-----|---------|---------|------|-----|-----|-----|------|----|-----|
| is            | gold    | dumb    | or   | am       | dumb | im     | at   | units         | right    | now    | which | is  | fine    | just  | wanna   | step   | my  | game  | up | and | know | its | late | as | hell | but | wanted | to | see | if | there | were | any | classes | that | were | open | whenever | do | search | on | gold | it | says | class | has | like | spaces | but | when | try | to | add | it | it | tells | me | to | add | to | the | active | waitlist | like | huh | why | does | it | say | there | is | space | if | theres | wait | list | any | of | yall | also | know | any | general | classes | that | its | not | too | late | to | add |
| environmental | studies | looking | to   | change   | my   | major  | to   | environmental | studies  | anyone | have  | any | advice  | or    | input   | on     | the | major |    |     |      |     |      |    |      |     |        |    |     |    |       |      |     |         |      |      |      |          |    |        |    |      |    |      |       |     |      |        |     |      |     |    |     |    |    |       |    |    |     |    |     |        |          |      |     |     |      |    |     |       |    |       |    |        |      |      |     |    |      |      |      |     |         |         |      |     |     |     |      |    |     |
| pstat         | or      | pstat   | with | pedersen | or   | pstat  | with | duncan        | which    | of     | the   | two | classes | would | be      | easier |     |       |    |     |      |     |      |    |      |     |        |    |     |    |       |      |     |         |      |      |      |          |    |        |    |      |    |      |       |     |      |        |     |      |     |    |     |    |    |       |    |    |     |    |     |        |          |      |     |     |      |    |     |       |    |       |    |        |      |      |     |    |      |      |      |     |         |         |      |     |     |     |      |    |     |
| soc           | anyone  | have    | pdf  | of       | the  | book   |      |               |          |        |       |     |         |       |         |        |     |       |    |     |      |     |      |    |      |     |        |    |     |    |       |      |     |         |      |      |      |          |    |        |    |      |    |      |       |     |      |        |     |      |     |    |     |    |    |       |    |    |     |    |     |        |          |      |     |     |      |    |     |       |    |       |    |        |      |      |     |    |      |      |      |     |         |         |      |     |     |     |      |    |     |


## **Key Results**


## **Summary**


## **Future Work**

### Touch-Ups
* Use the Mallet model to make the TF-IDF model more accurate
* (1) Mallet model assigns a post to a number
* (2) Depending on the number assigned to that post, run the post through TF-IDF and eliminate irrelevant topics when running it

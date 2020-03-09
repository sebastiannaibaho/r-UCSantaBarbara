# ucsb-subreddit-topic-modeling

## **Abstract**
This project uses an unsupervised machine learning model to categorize posts in the UCSB subreddit. We then created a bot which automatically flairs new posts within the appropriate topic. We extract Reddit post data through [pushshift.io](https://pushshift.io/). The data was trained on [gensim’s LDA Mallet model wrapper](https://radimrehurek.com/gensim/models/wrappers/ldamallet.html). Visualizations were done in [pyLDAvis](https://pyldavis.readthedocs.io/en/latest/). We experimented with several other models (tf-idf, biterm, GSDMM, text classification) and determined that the Mallet model was most accurate. 

## **Motivation**
Reddit is a popular social news platform that allows communities to discuss and vote on content that users submit. Our school’s subreddit, [/r/UCSantaBarbara](https://www.reddit.com/r/UCSantaBarbara/), is cluttered and unorganized. Currently more than 15,000 thousand members are on the UCSB subreddit and numerous posts are being added daily. Realizing that our school’s subreddit has the potential to be much more resourceful than it currently is, we decided that it would be helpful to create a model to organize its posts. 
![UCSB Subreddit](/markdown-assets/ucsb_subreddit.png)

## **Methodology**
### Data Collection
Posts were collected through pushshift.io. We considered only text posts and omitted link posts and image posts. Posts were cleaned by removing punctuation, special characters, and emojis and converting all letters to lowercase. The data was then tokenized and saved into a .csv file. This was done for all posts (n=31307). Here is a snippet of what the final data looked like:
| syllabus      | for     | pstat   | and  | pstat    | does | anyone | have | the           | syllabus | for    | these | two | classes | this  | quarter |        |     |       |    |     |      |     |      |    |      |     |        |    |     |    |       |      |     |         |      |      |      |          |    |        |    |      |    |      |       |     |      |        |     |      |     |    |     |    |    |       |    |    |     |    |     |        |          |      |     |     |      |    |     |       |    |       |    |        |      |      |     |    |      |      |      |     |         |         |      |     |     |     |      |    |     |
|---------------|---------|---------|------|----------|------|--------|------|---------------|----------|--------|-------|-----|---------|-------|---------|--------|-----|-------|----|-----|------|-----|------|----|------|-----|--------|----|-----|----|-------|------|-----|---------|------|------|------|----------|----|--------|----|------|----|------|-------|-----|------|--------|-----|------|-----|----|-----|----|----|-------|----|----|-----|----|-----|--------|----------|------|-----|-----|------|----|-----|-------|----|-------|----|--------|------|------|-----|----|------|------|------|-----|---------|---------|------|-----|-----|-----|------|----|-----|
| is            | gold    | dumb    | or   | am       | dumb | im     | at   | units         | right    | now    | which | is  | fine    | just  | wanna   | step   | my  | game  | up | and | know | its | late | as | hell | but | wanted | to | see | if | there | were | any | classes | that | were | open | whenever | do | search | on | gold | it | says | class | has | like | spaces | but | when | try | to | add | it | it | tells | me | to | add | to | the | active | waitlist | like | huh | why | does | it | say | there | is | space | if | theres | wait | list | any | of | yall | also | know | any | general | classes | that | its | not | too | late | to | add |
| environmental | studies | looking | to   | change   | my   | major  | to   | environmental | studies  | anyone | have  | any | advice  | or    | input   | on     | the | major |    |     |      |     |      |    |      |     |        |    |     |    |       |      |     |         |      |      |      |          |    |        |    |      |    |      |       |     |      |        |     |      |     |    |     |    |    |       |    |    |     |    |     |        |          |      |     |     |      |    |     |       |    |       |    |        |      |      |     |    |      |      |      |     |         |         |      |     |     |     |      |    |     |
| pstat         | or      | pstat   | with | pedersen | or   | pstat  | with | duncan        | which    | of     | the   | two | classes | would | be      | easier |     |       |    |     |      |     |      |    |      |     |        |    |     |    |       |      |     |         |      |      |      |          |    |        |    |      |    |      |       |     |      |        |     |      |     |    |     |    |    |       |    |    |     |    |     |        |          |      |     |     |      |    |     |       |    |       |    |        |      |      |     |    |      |      |      |     |         |         |      |     |     |     |      |    |     |
| soc           | anyone  | have    | pdf  | of       | the  | book   |      |               |          |        |       |     |         |       |         |        |     |       |    |     |      |     |      |    |      |     |        |    |     |    |       |      |     |         |      |      |      |          |    |        |    |      |    |      |       |     |      |        |     |      |     |    |     |    |    |       |    |    |     |    |     |        |          |      |     |     |      |    |     |       |    |       |    |        |      |      |     |    |      |      |      |     |         |         |      |     |     |     |      |    |     |

A large obstacle to our project was the lack of labelled data sets. From the following graph only approximately 500 posts are flaired. We had to primarily rely on models that did not require labelled sets.
![UCSB Subreddit Flair Distributions](/markdown-assets/flair_distributions.png)

### Latent Dirichlet Allocation
Post data was further processed in the following order:
1. Removal of stopwords 
  >Removal of unnecessary words that add no meaning (e.g the, a, we)
2. Formation of bigrams and trigrams 
  >Grouping of common two word and three word phrases
3. Lemmatization 
  >The reduction of words into their root form so they can analyzed the equally (e.g running, runs, ran all convert to run)

Stopword removal and lemmatization was done through [nltk](https://www.nltk.org) and bigram and trigram creation through [gensim](https://radimrehurek.com/gensim/models/phrases.html).

### Optimizing the model
#### Number of Topics
Optimal topic amounts were chosen using coherence score. We chose 4 total topic clusters rather than 7 as topics were unnecessarily subdivided into categories that were too narrow.

![Number topics against coherence score](/markdown-assets/topic_coherence.png)

#### Optimal alpha value
Once deciding on a topic number of 4, we tested various alpha values for the model and determined that alpha=90 was ideal as it yielded the highest coherence value. The alpha value determines document-topic density. The higher the alpha value, documents are composed of more topics. 

![Alpha value against coherence score](/markdown-assets/alpha_coherence.png)

### Building Final Model
Now that we have determined the optimal number of topics and alpha value, we build our model. We use Mallet's built in hyperparameter optimization to constantly adjust alpha and beta parameters as the model is trained.

```python
lda_model = gensim.models.wrappers.LdaMallet(mallet_path, 
                                             corpus=corpus, 
                                             num_topics=4, 
                                             id2word=id2word,
                                             alpha=90, 
                                             optimize_interval=10)
```

### Clustering
Clustering visual data was done in pyLDAvis. On the left, the circles represent each topic cluster, with the size of the circle representing how prevalent that topic is. How close the circles are show how related certain topics are. Each topic cluster is labelled with how we flaired them for the viewer's convenience.
![Mallet LDA Visualized](/markdown-assets/visualizedLDA4_optimized.png)
For an interactive version, open the .html file [here](https://github.com/sebastiannaibaho/r-UCSantaBarbara/blob/separate-function-branch/markdown-assets/visualizedLDA4_optimized.html)

## **The Reddit Bot**
The Reddit bot uses [praw](https://praw.readthedocs.io/en/latest/) to automatically retrieve new submissions to the subreddit in realtime. Each post is then processed the same way as our LDA model. The model is able to determine the most likely topic cluster the post fits in and the bot flairs the post on the site accordingly. 

## **Summary**
Our goal for this project was to categorize posts in the UCSB subreddit and flair them in real time. We trained our model and determined optimal topic numbers and alpha parameters by maximizing coherence values. We then built a Reddit bot that can independently detect new posts and flair them appropriately according to our model. 

## **Key Results**
1. We were able to determine the ideal number of topic clusters and value of hyperparamters for our model. Mallet was able to further refine these parameters while the model was being trained. Our final model had a coherence value of 0.584 with 4 topic clusters. Through internal testing, the accuracy of our model to correctly flair a post into the correct category is approximately 70%. 

2. Data visualization allowed us to determine salient terms in each topic and how close certain topics were to each other. This allowed us to see which words most contributed to which topic. For example, "iv" was extremely useful in categorizing the IV/Social category and words such as "midterm" and "class" gave a high probability for the Academic cluster.

3. We developed a Reddit Bot which can autonomously flair posts in real time by analyzing a post's title and text with respect to our trained LDA model.

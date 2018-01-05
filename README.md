# Tweets analysis using NLP

An interesting technical story and findings when trying to analyze the tweets of hashtag "#news".
And in the process observed how hashtags affect the performance of word2vec, wordlouds visualization. And hashtags are not completely bad either. Hashtags can be used for categorizing the tweets or as labels. This project clearly explains why:


## Data Gathering

Source: Twitter Streaming API.
Module: Used the tweepy module to gather stremaing data from twitter API.    
Filter Terms:  "#news" and language: "en".    

Data saved to JSON files in: "./Data/raw/*.json".    

## Common preprocessing

Preprocess all the tweets in the JSON files present in the ./data/raw/.

Script: ./script/tweets_common_preprocess.py
Module: re, string, nltk, tweet_preprocessor etc
Source: ./data/raw/*.json
Save To: ./data/clean/data.csv

Does common preprocessing to tweets:
  1. remove URL's
  2. remove pucntuations (NOT hash tags '#')
  3. remove emoji's
  4. remove smiley's
  5. remove mentions's     
  6. remove retweets (duplicates only) (store original tweet)
  7. remove RESERVE words: RT etc
  8. remove duplicate tweets. In case if it's a retweet, make sure to only include the original tweet. Also make sure the original tweet is not already included.
  8. retain hashtags
  9. retain numbers
  10. Extract date and tweet ID.


NOTE: Different analysis requires different preprocessing. Some of the preprocessing has been done in analysis scripts. For ex: removal of stopwords, pos filtering, removal of hashtags etc.


*** TODO: Need to create multiple output files instead of one single data.csv file in ./data/clean
This way we can use spark in distributed fashion and work on multiple files in parallel.
Most of the tasks done in this project: word2vec, wordcount, hashtag, preprocessing, pos tagging
etc., can be implemented using spark. Yet to include (remove html tags: not necessary, just a precaution) ***




## Analysis Phase

This project includes three different analysis:

1. Analysis of Words/n-grams
2. Analysis on hashtags
3. Analysis on word Clusters using word2vec

NOTE: All the analysis scripts are present in the ./scripts/*.ipynb. They are all jupyeter notebooks. Also included HTML files in "./doc/" folder



## Analysis of Words/ngrams (Word Count Analysis.ipynb):

[Analysis Notebook](https://htmlpreview.github.io/?https://raw.githubusercontent.com/chandan-u/twitter_analysis_using_nlp/master/doc/Word%20Count%20Analysis.html)

An analysis of words in the tweets using word count and word clouds

### Types of analysis performed:
1. word count-wordcloud including hashtags, one for each unigrams and bigrams
2. word count-wordcloud excluding hashtags, one for each unigrams and bigrams
3. word count-wordcloud using POS Tagging (Adjectives, Verbs, Nouns), only unigrams

for all unigram ananlysis: stopwords have been removed
for all bigrams analysis: stopwords have been retained (to maintain the nautre of hmm).


### Observaton/Conclusion

1. The word cloud generated by just pos tags is completely different from the word cloud generated by all the words present.

2. First word cloud analysis with hashtags present has a lot of noise (#alamalki, # tech etc). They don'nt provide any interesting or new information.

3. The second word cloud analysis with hashtags removed has interesting keywords. Also the bigrams are more descriptive than the unigrams The following example explains clearly:                    
 *Ex: US_BANKER bigrams is more informative for visualization than us, banker as seperate unigrams in the   wordcloud. The bigrams clearly show that the tweets are talking about US_BANKERS*

4. The third wordClould Analysis using the POS TAGS (Adjectives, verbs and Nouns) seem to provide different sort of information than the first two wordcloud analysis tasks. (As you can see most of the terms in this are, "-"ve sentiment verbs such as "hanging", "stabbed", "dbett", "save" etc...). I guess this word cloud is more usefull for analyzing the overall sentiments in the news.

5. An interesting method to try would be, is to use tf-idf for each tweet and extract top 3 topics from each tweet and then visualize a word cloud on the frequency of these topics across documents.





## Word Similarity/Clusters analysis using Word2vec (/scripts/Similar words cluster analysis using gensim.ipynb):


Objective was to find word clusters using word2vec and Observe patterns in clustering

[Analysis Notebook](http://htmlpreview.github.io/?https://raw.githubusercontent.com/chandan-u/twitter_analysis_using_nlp/master/doc/Similar%20words%20cluster%20analysis%20using%20gensim.html)


### Types of Analysis: (Analyize similarities to word "cold" and see how well its clustering the words)
1. Simple word2vec trained with window size 5
2. Word2vec trained with window size 3: To get rid of irregular similarites
  (Expected to remove irregularities in similarities: EX: israel - cold is similar)
  (Did not work as expected)
3. Word2vec trained with hashtags removed in the corpus (Removed irregularities Israel not similar to cold anymore)

### Observaton

** word2vec similarity for "cold" has caputred all the related words such as "recordshattering" etc. Some interesting irregularites are present though:**

1. I wonder why florida is here on the top?
     there is  a valid tweet abt florida in the data:

     *"(Reuters) - A rare winter storm hit the U.S. Southeast on Wednesday,
      bringing Florida's capital its first snow in three decades"*

2. Why is Israel vector closer with cold ?

     a. The reason is simple: These two are not related to cold. But some of Israel channels reported the news and have, included #israel in the tweet for publicity. It is just that.

     b. In some cases, the tweets include daily news summary of all the headlines. In which case you can expect different news ,to be in the same sentence. But word2vec will fail over such a dataset.

     c. EX: *#israel #ynet #news broadcast by #emetnewspress s korea offers to talk with north on olympics cooperation,2018-01-02 06*


### WorkAround/Solution

1. One work around is we reduce the window size of the word2vec training algorithm from five to three.

2. We can also try removing the hashtags which seem to create the noise.


### Conclusion

As you can clearly see word2vec works better / clusters the words better when the hashtags are remvoed.

It seems like for clustering related words, hashtags are noise for the task. It may have other uses though

And reducing the window size, didnt help remove the noise in the similiarties.

```
model.wv.most_similar("cold", topn=30)
[('brutal', 0.9845326542854309),
 ('snaps', 0.9833786487579346),
 ('extreme', 0.9825105667114258),
 ('maintain', 0.9795016050338745),
 ('reached', 0.9790675044059753),
 ('temperatures', 0.9762852191925049),
 ('fa\xe2\x80\xa6', 0.9556857347488403),
 ('arctic', 0.9514330625534058),
 ('snap', 0.9511594772338867),
 ('weather', 0.9390607476234436),
 ('raw', 0.9373143911361694),
 ('bitter', 0.9243055582046509),
 ('braves', 0.9214819669723511),
 ('yes', 0.9203097820281982),
 ('recordshattering', 0.9084766507148743),
 ('cap', 0.902690589427948),
 ('f\xe2\x80\xa6', 0.8993377685546875),
 ('wave', 0.8973126411437988),
 ('inevitable', 0.8808591961860657),
 ('areas', 0.8786516785621643),
 ('levels', 0.8773680329322815),
 ('much', 0.8640298843383789),
 ('reaches', 0.8627901077270508),
 ('prepare', 0.86165452003479),
 ('war', 0.8576942682266235),
 ('blast', 0.8489212989807129),
 ('mean', 0.8452771902084351),
 ('there\xe2\x80\xa6', 0.8448013067245483),
 ('georgia', 0.842862606048584),
 ('florida', 0.8415167331695557)]
 ```


No more israel in words closer to cold :)

TODO: The above analysis can be expanded to cluster tweets itself by averaging document vectors using word vectors.


## HashTag Analysis + topic Analysis

 [Analysis Notebook](http://htmlpreview.github.io/?https://raw.githubusercontent.com/chandan-u/twitter_analysis_using_nlp/master/doc/Hashtag%20Analysis.html)

 This script analyzes hashtags alone occured in the tweets

 This could give us a general overview of topics that are occuring in the news

 Types of analysis performed:

  1. Word count - Word Cloud of hashtags -
  2. Topic analysis across time (Similar to topic evolution)


### Word count - Word Cloud of hashtags

From the above chart we could clearly see the various hot topics in twitter asociated with #news. It would intresting to see if word2vec captures these semantically. Also hashtags can be used for categorizing tweets as you can clearly see why below:


1. music/celebrities: ilovehiphop, rapartist, celebritygossip, trump
2. countries/places: iran, india, usa, canada, sydney, china, shanghai, uk, nigeria
3. trading/markets: bitcoin, forex, money
4. tech: cryptocurrency, blockchain, google, iot

### Topic Evolution with time:


!["Topic Evolution with time"](https://github.com/chandan-u/twitter_analysis_using_nlp/blob/master/doc/img/Topic_evolution_with_time.png)

As you can see in the above plot, the word "four" has more importance across the entire time period. So I looked back into the data to see why and found some tweets:

1. #news #spain #spain horror four injured as car mounts pavement in busy street
2. mumbai bandh live updates five including four cops injured in protests hospitalised
3. eurusd hits highest level in four months poised to test 2017 high #forex #eurusd #fx #news

and many more.


TODO: The above code can be expanded just to handle hashtags/ or just selected pos tags.




## AIRFLOW DAGS:

Inlcuded Appache Airflow DAGs which can be used to schedule the grabbers which collet the streaming data.

It can be used for pipelining

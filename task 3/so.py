#!/usr/bin/env python
# coding: utf-8

# This doc will walk through Three stages of studying stackflow tags data set.
# 
#  **1. First stage: Data cleaning**
# 
# As we notice there are columns that contain html mark ups, we want to make sure that it is taken care of and cleaned up
# 
#  **2. Second Stage: Feature engineering**
# 
# Apply methods to engineer features from cleaned text data
#  
# **3. Third Stage: Classification modeling**
# 
# Using engineered features to build predictive models

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import nltk # natural language processing
import re # regular expression
from bs4 import BeautifulSoup #scraping HTML
from nltk.corpus import stopwords
import seaborn as sns # visualization
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from string import punctuation




# nltk workspace

stop = set(stopwords.words('english'))

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory


# Any results you write to the current directory are saved as output.


# In[2]:


# read in raw data sets
biology = pd.read_csv("biology.csv")
cooking = pd.read_csv("cooking.csv")
crypto = pd.read_csv("crypto.csv")
diy = pd.read_csv("diy.csv")
robotics = pd.read_csv("robotics.csv")
travel = pd.read_csv("travel.csv")
test = pd.read_csv("test.csv")


# In[3]:


## Concatenate datasets
#raw = pd.concat([biology,cooking,crypto,diy,robotics,travel],axis = 0, ignore_index =True)
raw = test


# In[4]:


# Simple Statistics
print("This dataset has in total {} rows.".format(raw.shape[0]))
#print("out of which, {} rows come from train dataset and {} rows come from test dataset.".format(raw[raw['source']=='train'].shape[0],raw[raw['source']=='test'].shape[0]))


# # **Stage 1: Data Cleaning**

# Content column is a little bit messy since it's embedded in HTML. cleaning it up before applying any natural language processing tactics will facilitates our analysis moving forward. Beautifulsoup is a python package that helps dealing with HTML. The primary goal of this exercise is to:
# 
# 
#  - Getting the clean text data;
#  - Extract potentially important information from HTML tags. 
# 
#  
# **Tags we want to pay attention to:**
# 
#  1. The emphasize class: strong, em, i, li
#  2. The header class: h1, h2, h3
#  3. Link 

# In[5]:


def parse_content(s):
    emphasize = []
    header = []
    link = []
    content = ""
    soup = BeautifulSoup(s,'html.parser')
    content = soup.get_text()
    return pd.Series({'content_parsed':content})


# In[6]:


# Apply parse_content onto dataframe.
raw = pd.concat([raw,raw['content'].apply(parse_content)],axis = 1)


# In[7]:


test[1:5]


# ## Stage 2: A dive into the tags##
# 
# Before we predict the tags, we want to study and understand the tags. Two initial thoughts are:
# 
#  - Studying the distribution of word counts 
#  - Studying the distribution of semantics counts

# In[8]:


## Study the tags Word count distribution
#raw['tags'] = raw['tags'].apply(lambda x: x.split(" "))
#raw['tags_wc'] = raw['tags'].apply(len)
#sns.barplot(x='tags_wc',y='tags_wc',data=raw,estimator=lambda x: len(x),palette='Blues')


# In[9]:


##study the tags: semantic structure
#raw['tags_token'] = raw['tags'].apply(str).apply(nltk.word_tokenize)
#raw['tags_pos'] = raw['tags'].apply(nltk.pos_tag)


# In[10]:


# What is the distribution of different semantics?
#semantics = pd.DataFrame({'semantics' : [pair[1] for col in raw['tags_pos'].tolist() for pair in col]})
#semantics['count'] = 1
#fig,axs = plt.subplots()
#sns.barplot(x='semantics',y='count',data=semantics,estimator=lambda x: len(x),palette=sns.cubehelix_palette(8, start=.5, rot=-.75),ax=axs)
#axs.set_title('semantic distribution')
#axs.set_ylabel('frequency')


# As what we would expect, The semantic strongly skewed towards **nouns** (NN,NNS,JJ).

# ## **Naïve Try : Rule based Algorithm** ##
# 
# The first Iteration is very brute. We are going to count the frequencies(but here "adjusted" frequencies - TF-IDF), the highest the score one word get, the more likely it's going to be included in the tags.
# 
# How many words are we going to include? Since the number of words a tag can have has an upper bound 5, we are going to include 5 words.

# In[11]:

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)
#Building NLTK pipelines
def td_idf_matrix(dataset):
    dataset['all_text'] = dataset['title'] + dataset['content_parsed'] 
    dataset['all_text'] = dataset['all_text'].apply(lambda x: str.lower(x).replace('\n',' '))
    mydoclist = [strip_punctuation(doc) for doc in dataset['all_text'].tolist()]
    count_vectorizer = CountVectorizer(stop_words='english',lowercase=True,analyzer='word')
    term_freq_matrix = count_vectorizer.fit_transform(mydoclist)
    tfidf = TfidfTransformer(norm="l2")
    tfidf.fit(term_freq_matrix)
    tf_idf_matrix = tfidf.transform(term_freq_matrix)
    pos_to_word = dict([[v,k] for k,v in count_vectorizer.vocabulary_.items()])
    return tf_idf_matrix, pos_to_word

tf_idf_matrix, pos_to_word = td_idf_matrix(raw)


# In[12]:



def importance_list_row(sparse_row,n_importance):
    importance_list = [0]*n_importance
    for i in range(0,n_importance): 
        ind =  sparse_row.indices[sparse_row.data.argmax(axis=0)] if sparse_row.nnz else 0
        importance_list[i] = pos_to_word[ind]
        sparse_row[0,ind] = 0
    return importance_list


def importance_list(sparse_matrix,n_importance):
    n_row = sparse_matrix.shape[0]
    importance_lists = [0]*n_row
    for row in range(0,n_row):
        importance_lists[row] = importance_list_row(sparse_matrix[row],n_importance)
    return importance_lists   


# In[13]:


#n_importance = 2
#predict = importance_list(tf_idf_matrix,n_importance)
#predict_vs_actual = pd.DataFrame({'predict':predict})
#predict_vs_actual['predict'] = predict_vs_actual['predict'].apply(lambda x: "".join(chr+" ") for char in x)
#predict_vs_actual[0:50]


# The result from our naive approach is quite nasty. For the next iteration, I will work on improving it.
# 
# One idea stems from the semantic distribution. The majority of tags are nouns and adjectives. therefore I'm going to tag my content and parse out words by their semantics and only focus on the **noun and the adjectives**.

# In[14]:


#tokenize and tag texts. 
lemmatizer = nltk.stem.WordNetLemmatizer()
raw['all_text'] = raw['all_text'].apply(strip_punctuation)
raw['text_token'] = raw['all_text'].apply(nltk.word_tokenize)
raw['text_token'] = raw['all_text'].apply(nltk.word_tokenize)
raw['text_token'] = raw['text_token'].apply(lambda x:[lemmatizer.lemmatize(t) for t in x])
raw['text_pos'] = raw['text_token'].apply(nltk.pos_tag)
raw['text_nouns'] = raw['text_pos'].apply(lambda x: [pair[0] for pair in x if pair[1] in ("NN","NNS","JJ")])


# In[15]:


raw['text_bigram'] = raw['text_pos'].apply(nltk.bigrams)
raw['text_bigram'] = raw['text_bigram'].apply(list)


# In[16]:




# In[17]:


raw[0:5]


# In[18]:


def findPair(l):
    result = []
    for pair in l:
        if pair[1][1] in ('NN','NNS') and pair[0][1] in ('NN','NNS','JJ'):
            result.append(pair[0][0]+" "+pair[1][0])
    return result
raw['word_pair'] = raw['text_bigram'].apply(findPair)


# This seems to look much better. Let's give it a try.

# In[19]:


mydoclist = raw['text_nouns'].apply(" ".join).tolist()
#mydoclist[0:5]
count_vectorizer = CountVectorizer(stop_words='english',lowercase=True,analyzer='word',ngram_range=(1,1))
term_freq_matrix = count_vectorizer.fit_transform(mydoclist)
tfidf = TfidfTransformer(norm="l2")
tfidf.fit(term_freq_matrix)
tf_idf_matrix = tfidf.transform(term_freq_matrix)
pos_to_word = dict([[v,k] for k,v in count_vectorizer.vocabulary_.items()])


# In[20]:


n_importance = 3
predict = importance_list(tf_idf_matrix,n_importance)
predict_vs_actual = pd.DataFrame({'tags':predict,'id':raw['id']})
predict_vs_actual['tags'] = predict_vs_actual['tags'].apply(" ".join)


# In[21]:


predict_vs_actual[0:100]


# In[22]:


predict_vs_actual.to_csv("predicted.csv",index=False)


# # **Stage Two: Feature Engineering(TBD)**
# 
# When people are posting on stack flow, they often have a **problem** to **solve**. So in the texts, what comes the most important would be the **noun** followed by the **verb**.
# 
# As we are predicting unseen topics, supervised learning might not be deemed as useful here. For the first iteration I'm going to take a naïve approach - by building up a very simple, **rule based** algorithm.  
# 
# A natural thought lands on frequency - But we also don't want to look at term frequency since we don't want our result overshadowed by high frequent but meaningless stop words. TF-IDF comes in handy.
# 
# Also - from my years of experiences in writing irritatingly stupid questions on stack flow,  writing the core question in the title as well as in the content will increase the odds of getting your question answers. reversely, **if a keyword shows up both on titles and on content, it might be the one we are looking for**.
# 
# Other considerations - we may want to study the tag a little bit to understand how many words people normally tend to include in the tag(the word count distribution of the tags) and whether their is evident semantic structure to the tags. 

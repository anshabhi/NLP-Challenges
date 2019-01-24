from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier

import numpy

n=int(input())
train = [input() for i in range(n)]
input()
test = [input() for i in range(n)] 



text_clf=Pipeline([('vect',CountVectorizer()),
                   ('tfidf',TfidfTransformer()),
                   ('clf',SGDClassifier())])

y=numpy.arange(n)


text_clf.fit (train,y)


result=text_clf.predict(test)

for i in result:
    print(i+1)


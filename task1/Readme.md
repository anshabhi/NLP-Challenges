## Problem Statement 1

Guess the Flipkart Query: Check if the input search string provided by the user contains any of the keys as substring.


### Solution Approach

The step by step implementation is:

* Clean the input by converting eveything to small letters, remove stopwords and punctuations, and squishing any extra space that may have appeared as result of above.

* It is checked if the input string contains any one of the 20 keys directly. If its true, then a score of 100 is assigned to that key for the string.

* Now, it is checked if the input string contains any of the substring of keys. 10 points are awarded for every such occurence.

* The value with maximum score as a result of above operations is given out as the output.

The detailed solution is available [here](task1/submission1.r)

***

## Problem Statement 2

Implement core Data Science techniques to find the most probable replacement for ---- in the input string.

### Solution Approach

The step by step implementation is:

* Read the corpus.txt file, and make a random sample from its first 2000 lines, as the corpus for our prediction model.

* Clean the random sample by converting everything to lowercase, removing punctuations, numbers and multiple whitespaces.

* Make a Term Document Matrix (TDM) from `tm` package from corpus resulting from above operations.

* Read the input, obtain substrings by taking `----` as the pattern.

* Obtain the last word of each of these substrings. We will use only this word for prediction.

* Now, we will begin the actual prediction process.

* First, we check if the prediction word and possible answers exist in our model or not

* If they don't exist, we simply take a random probability, <0.2 for that keyword to be a possible solution. Its restricted to 0.2, so that it doesn't interfere with genuine cases

* If they exist, correlation between the 2 is calculated, and stored in a vector.

* We finally print the keyword with maximum correlation as our final answer.


Further Improvements possible:

We only used 1-gram for this prediction model. The model can be easily ported 2grams and more, which might result in better accuracy.


The detailed solution is available [here](task1/submission1.r)
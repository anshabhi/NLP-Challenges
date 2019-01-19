# To be or what to be, that is the question
Submission #2

[Hackerrank Submission](https://www.hackerrank.com/challenges/to-be-what/submissions/code/96280726)

This program implements core Data Science techniques to find the most probable replacement for ---- in the input string.

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


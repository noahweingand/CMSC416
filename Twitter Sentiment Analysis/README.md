# Twitter Sentiment Analysis
## Description
A Python program that extracts the sentiment of a tweet. This application uses 2-way polarity to determine if a tweet is either positive or negative. 
The application uses training data that includes tweets and their sentiment. We use this training data to build unigrams to see which words are more associated
with a particular sentiment. These discriminative words become features in a decision list that is then used to determine the sentiment of the tweets in the test data. The training and testing data are given in this repository.

## Using application
Run in terminal or via cmd-line with Python 3.

```bash
python3 sentiment.py sentiment-train.txt sentiment-test.txt my-model.txt > my-sentiment-answers.txt
```

## Using the scorer
scorer.py is a program to compare results to the key of the data were testing the application with. 
It calculates a confusion matrix and accuracy. The test key is given in the repository as well.

Run in terminal or via cmd-line with Python 3.
```bash
python3 scorer.py my-sentiment-answers.txt sentiment-test-key.txt
```


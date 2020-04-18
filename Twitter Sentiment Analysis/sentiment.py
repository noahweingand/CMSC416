# ###########################################################################################################
# File Name: sentiment.py
# Author: Noah Weingand
# Course Information: CMSC 416 - Assignment 4 - Dr. Bridget McInnes
# Date Started: April 11 2020
# Date Due: April 14 2020
# ###########################################################################################################
#
# PROGRAM DESCRIPTION:
# sentiment.py is a sentiment classifier program that marks tweets as either positive or negative based off a decision
# list built off training data. It takes in 2 required command line properties: a training file that has tweets
# and their actual handtagged sentiment and then a test file that has tweets with no assigned sentiment that the
# program will predict
#
# IMPLEMENTATION:
# Decision List
#
# FEATURES:
# Just a bag of words (unigrams in corpus) for now. I chose 'angela' and 'merkel' for identifying a negative sentiment.
# I chose 'amazon', 'prime', 'ac/dc', 'tomorrow', '-', 'on', and 'http://t' for a positive sentiment.
#
# ACCURACY OF PROGRAM: 
# 70.259 %
#
# CONFUSION MATRIX (from scorer.py):
#
#                               predicted positive      predicted negative
# 
#    actually positive                  152                      8
#
#    actually negative                  11                       61
#     
#
# PROGRAM EXAMPLE:
# INPUT: python3 sentiment.py sentiment-train.txt sentiment-test.txt my-model.txt > my-sentiment-answers.txt
# OUTPUT: the tweet's instance ID (to identify the tweet) and the sentiment the program predicted
# EX: <answer instance="620979391984566272" sentiment="positive"/>
#
# ###########################################################################################################

import sys #for file handling
import re #regex
import math #for calculating log likelihood
import operator #for sorting decision list

wordBag = {} #bag of words (unigrams) to keep track of their count and sentiment from training file
decisionList = {} #initial decision list that's not sorted by log likelihood
results = {} #dictionary of instance tweet from test data and the predicted sentiment

def main():
    trainText = sys.argv[1] #training text file
    testText = sys.argv[2] #text to be analyzed
    model = open("my-model.txt", "w+") #open model to print decision list
    trainText = open(trainText, "r") #open the training text to be read
    testText = open(testText, "r") #open the text we wanna analyze to be read
    trainCorpus = trainText.read().lower() #read in text and convert all letters to lowercase

    #remove unnecessary strings from training data
    trainCorpus = re.sub('</context>',' ',trainCorpus)
    trainCorpus = re.sub('<corpus lang="en">','',trainCorpus)
    trainCorpus = re.sub('<lexelt item="sentiment">','',trainCorpus)
    trainCorpus = re.sub('</lexelt>','',trainCorpus)
    trainCorpus = re.sub('</corpus>','',trainCorpus)
    #remove punctuation and parenthesis
    trainCorpus = trainCorpus.replace("(", " ")
    trainCorpus = trainCorpus.replace(")", " ")
    trainCorpus = trainCorpus.replace("!", " ")
    trainCorpus = trainCorpus.replace(".", " ")
    trainCorpus = trainCorpus.replace(",", " ")

    trainCorpus = trainCorpus.split("</instance>") #break corpus up into tokens every '</instance>'

    #collect training data
    for i in trainCorpus: #for each tweet in training corpus
        trainEntry = i.split("<context>") #separate tweet and instance / sentiment
        sentiment = re.split('=', trainEntry[0]) #splits up instance to get sentiment
        if len(sentiment) > 3: #checks for actual training instance and not empty space in data
            sentiment = sentiment[3] #get sentiment from training data
            if "p" in sentiment:
                sentiment = "positive"
            if "n" in sentiment:
                sentiment = "negative"
        if len(trainEntry) > 1:
            tweet = trainEntry[1] #get tweet
            tweet = re.split('\s+', tweet) #get unigrams from tweet
            for word in tweet: #count # of times each word appears in all of tweet
                if word == '': #checks for errors on empty space
                    continue
                if word not in wordBag:
                    wordBag[word] = {} 
                    if sentiment not in wordBag[word]:
                        wordBag[word][sentiment] = 0
                if word in wordBag:
                    if sentiment not in wordBag[word]:
                        wordBag[word][sentiment] = 1
                    if sentiment in wordBag[word]:
                        wordBag[word][sentiment] = wordBag[word][sentiment] + 1

    #make features
    negFeatureList = {"angela" : 0, "merkel" : 0}
    posFeatureList = {"http://t" : 0, "-" : 0, "on" : 0, "amazon" : 0, "prime" : 0, "ac/dc" : 0, "tomorrow" : 0}
    #make model
    for word in negFeatureList:
        freqPos = wordBag[word]["positive"]
        freqNeg = wordBag[word]["negative"]
        ll = abs(math.log10(freqNeg / (freqPos + 0.000000001))) #calculate log likelihood of each negative feature
        negFeatureList[word] = ll
    for word in posFeatureList:
        freqPos = wordBag[word]["positive"]
        freqNeg = wordBag[word]["negative"]
        ll = abs(math.log10(freqPos / (freqNeg + 0.000000001))) #calculate log likelihood of each negative feature
        posFeatureList[word] = ll
    #print model
    for feature in negFeatureList:
        ll = negFeatureList[feature]
        model.write("Feature: " + feature + " | " + "Sentiment: " + "negative" + " | " + "LL: {}\n".format(ll))
    for feature in posFeatureList:
        ll = posFeatureList[feature]
        model.write("Feature: " + feature + " | " + "Sentiment: " + "positive" + " | " + "LL: {}\n".format(ll))
    model.close()
#---------------------------------CLASSIFYING BELOW THIS-------------------------------------------------------------
    #build decision list from model
    unsortedDL = open("my-model.txt",'r')
    unsortedDL = unsortedDL.read()
    #clean my-model.txt
    unsortedDL = re.sub('Feature: ','',unsortedDL)
    unsortedDL = re.sub('Sentiment: ','',unsortedDL)
    unsortedDL = re.sub('LL: ','',unsortedDL)
    unsortedDL = unsortedDL.split("\n")
    unsortedDL.remove("")
    for line in unsortedDL:
        line = line.split(" | ")
        feature = line[0]
        if line[1]:
            sentiment = line[1]
        if line[2]:
            ll = float(line[2])
        decisionList[feature] = (ll, sentiment)
    
    newSortedDL = {} #new decision list sorted by log likelihood
    sortedDL = sorted(decisionList.items(), key=operator.itemgetter(1),reverse=True)
    temp = sortedDL[0]
    i = 0
    for x in range(len(sortedDL)): #parsing sorted DL list to rebuild DL dictionary sorted by log likelihood
        temp = sortedDL[x]
        single = temp[0]
        single = single.replace("'","")
        newSortedDL[single] = temp[1]
    
    #classify the sentiment of test tweets
    testCorpus = testText.read().lower()
    testCorpus = re.sub('</context>',' ',testCorpus)
    testCorpus = re.sub('<corpus lang="en">','',testCorpus)
    testCorpus = re.sub('<lexelt item="sentiment">','',testCorpus)
    testCorpus = re.sub('</lexelt>','',testCorpus)
    testCorpus = re.sub('</corpus>','',testCorpus)
    #remove punctuation and parenthesis
    testCorpus = testCorpus.replace("(", " ")
    testCorpus = testCorpus.replace(")", " ")
    testCorpus = testCorpus.replace("!", " ")
    testCorpus = testCorpus.replace(".", " ")
    testCorpus = testCorpus.replace(",", " ")
    testCorpus = testCorpus.split("</instance>")

    #for each tweet instance in test corpus
    for i in testCorpus:
        testEntry = i.split("<context>")
        instance = re.split('=', testEntry[0])
        if len(instance) > 1:
            instance = instance[1]
            instance = instance.replace(">","")
            instance = instance.replace("\"","")
            instance = instance.replace("\n","")
        if len(testEntry) > 1:
            tweet = testEntry[1]
            tweet = re.split('\s+', tweet)
            for word in tweet:
                if word == '':
                    continue
                if word in newSortedDL: #if word is feature in decision list
                    results[instance] = newSortedDL[word][1] #set it equal to the sentiment of the feature in the DL 
                    break
                else:
                    results[instance] = "positive" #otherwise, just make it positive, since it's more likely to be positive

    #print program results (predicted sentiment of tweet)
    for instance in results:
        sentiment = results[instance]
        print("<answer instance=\""+instance+"\" sentiment=\"" + sentiment + "\"/>")
            
    #close file handling
    trainText.close()
    testText.close()
main()
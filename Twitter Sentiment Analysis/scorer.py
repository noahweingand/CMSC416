# ###########################################################################################################
# File Name: scorer.py
# Author: Noah Weingand
# Course Information: CMSC 416 - Assignment 4 - Dr. Bridget McInnes
# Date Started: April 11 2020
# Date Due: April 14 2020
# ###########################################################################################################
#
# Program Description:
# scorer.py calculates the accuracy of sentiment.py by comparing the program's results with a handtagged test key
# It prints the accuracy and dictionary (confusion matrix)
#
# Program Example:
# INPUT: python3 scorer.py my-sentiment-answers.txt sentiment-test-key.txt
# OUTPUT: a matrix telling you the score of the sentiment you predicted (rows) and the sentiment it was (columns)
#
# Example:
#               Positive      Negative
#
#       Positive    100         15
#        
#       Negative    4           32          
# ###########################################################################################################

import sys
import re

answerDict = {} #to keep track of instance and sentiment.py's predicted sentiment
keyDict = {} #to keep track of instance and test key's actual sentiment
results = {} #confusion matrix to view accuracy

def main():
    answers = sys.argv[1] #predicted answers from sentiment.py
    key = sys.argv[2] #answers from test key
    
    answerFile = open(answers, 'r')
    keyFile = open(key, 'r')
    answerCorpus = answerFile.read()
    keyCorpus = keyFile.read()

    #build answerDict from predicted answer corpus
    answerCorpus = answerCorpus.split("\n")
    for answer in answerCorpus:
        answer = answer.replace("\"","")
        answer = answer.replace("<answer instance=","")
        answer = answer.replace("sentiment=","")
        answer = answer.split()
        if len(answer) > 1:
            instance = str(answer[0])
            if "p" in answer[1]:
                answerDict[instance] = 1 #binary positive
            if "n" in answer[1]:
                answerDict[instance] = 0 #binary negative
        continue
    
    #build keyDict from test key corpus
    keyCorpus = keyCorpus.split("\n")
    for answer in keyCorpus:
        answer = answer.replace("\"","")
        answer = answer.replace("<answer instance=","")
        answer = answer.replace("sentiment=","")
        answer = answer.split()
        if len(answer) > 1:
            instance = str(answer[0])
            #print(instance)
            if "p" in answer[1]:
                keyDict[instance] = 1
            if "n" in answer[1]:
                keyDict[instance] = 0
        continue

    posPosCount = 0 #keeping count of instance if positive in key and answer
    negNegCount = 0 #keeping count of instance if negative in key and answer
    posNegCount = 0 #keeping count of instance if positive in key but negative in answer
    negPosCount = 0 #keeping count of instance if negative in key but positive in answer
    for i in keyDict:
        if keyDict[i] == 0:
            if answerDict[i] == 0:
                negNegCount = negNegCount + 1
        if keyDict[i] == 1:
            if answerDict[i] == 1:
                posPosCount = posPosCount + 1
        if keyDict[i] == 1:
            if answerDict[i] == 0:
                posNegCount = posNegCount + 1
        if keyDict[i] == 0:
            if answerDict[i] == 1:
                negPosCount = negPosCount + 1
    results = {
        "key positive" : {"predicted positive":posPosCount, "predicted negative":posNegCount},
        "key negative" : {"predicted negative":negNegCount, "predicted positive":negPosCount}
    }
    print(results)
    totalResults = 232
    accuracy = (posPosCount + negNegCount) / totalResults * 100
    print("Accuracy of sentiment.py: {}".format(accuracy))
    
    answerFile.close()
    keyFile.close()
main()
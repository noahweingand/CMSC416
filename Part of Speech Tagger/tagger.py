# ##################################################################
# File Name: tagger.py
# Author: Noah Weingand
# Course Information: CMSC 416 - Assignment 3 - Dr. Bridget McInnes
# Date Started: Feb 29 2020
# Date Due: Mar 8 2020
# ##################################################################
# Chosen Equation for Frequency Calculation:
# Frequency of a given tag: P(tag_i | word_i) * P(tag_i | previousTag_i)
# 
# Accuracy of tagger.py: 84.5329 %
#
# Program Description:
# This program tags parts of speech based on a training text with words already tagged. I use Bayes Rule,
# Markov's Assumption, and Markov's Chain Rule to estimate probabilities of a tag given the previous tag.
#
# Program Example:
# INPUT: python3 tagger.py pos-train.text pos-test.txt > pos-test-with-tags.txt
# OUTPUT: a file that has words tagged in a format of 'word/tag'
#
# ##################################################################

import sys #for file handling
import re #regex

wordTagDict = {} #nested dict to keep track of a tagged word with its respective tag and how many times they occured 
wordDict = {} #dict for words in training data and how many times they occur
lastTagDict = {} #nested dict to keep track of the tag you're on with the tag you just saw and how many times that specific order occured
tagDict = {} #dict for tags in training data and how many times they occur

def main():
    trainingDataFilePath = sys.argv[1] 
    text2BeTaggedFilePath = sys.argv[2] 
    file1 = open(trainingDataFilePath, "r") 
    file2 = open(text2BeTaggedFilePath, "r") 
    taggedText = file1.read() 
    text2BeTagged = file2.read() 
    taggedText = cleanText(taggedText) 
    text2BeTagged = cleanText(text2BeTagged) 
    buildWordTagDict(taggedText) #builds the word and its associated tags dictionary with frequencies as values
    buildWordFreq(taggedText) #builds the word dictionary with the amount of times that word occurs in corpus as the values
    buildTagDict(taggedText) #builds the tag dictionary with the amount of times that tag occurs in corpus as the values
    buildLastTagDict(taggedText) #builds the tag dictionary and its associated last tags dictionary with frequencies as values
    tagText(text2BeTagged) #tags the text based off the training data
    file1.close()  
    file2.close() 

def cleanText(input):
    input = re.sub(r'\s+', ' ', input) #replace white space with a single space
    input = re.sub("[\[\]]", '', input) #replace all brackets with empty space
    return input

def buildWordTagDict(input):
    tokenLines = [token for token in input.split(" ") if token != ""] #create tokens by separating on single spaces
    #print(tokenLines)
    for line in tokenLines:
        token = line.rsplit("/", 1) #split each token on forward slash to get the word and its tag
        wordKey = token[0] #the word
        tagKey = token[1] #the word's tag
        if wordKey not in wordTagDict: #check if the word is NOT in the dictionary
            wordTagDict[wordKey] = {} #if it's not, add a dictionary for that word
            if tagKey not in wordTagDict[wordKey]: #check if a tag is NOT associated with that word
                wordTagDict[wordKey][tagKey] = 0 # set it equal to 0 since it doesn't occur
        if wordKey in wordTagDict: #check if the word is in the dictionary
            if tagKey in wordTagDict[wordKey]: #check if the tag is associated with that word
                wordTagDict[wordKey][tagKey] = wordTagDict[wordKey][tagKey] + 1 # if it is, increment it by one
            if tagKey not in wordTagDict[wordKey]: #check if there is NOT a tag associated that word
                wordTagDict[wordKey][tagKey] = 1 #if there's not a tag associated with that word, then we've seen it once
    #print(wordTagDict)

def buildWordFreq(input):
    tokenLines = [token for token in input.split(" ") if token != ""] #create tokens by separating on single spaces
    for line in tokenLines:
        token = line.rsplit("/",1) #split on the forward slash to break the word/tag into word,tag
        wordKey = token[0] #get the word
        if wordKey not in wordDict: #if the word is NOT in the dictionary
            wordDict[wordKey] = 0 #set it equal to 0 since it doesn't occur
        if wordKey in wordDict: #if the word IS in the dictionary
            wordDict[wordKey] = wordDict[wordKey] + 1 #increment the frequency by 1
    #print(wordDict)

def buildLastTagDict(input):
    text = [line for line in input.split(" ") if line != ""]
    lastTag = '.' #use last tag as a . since we treat the first tag in the corpus as right after a new sentence (AKA a start tag)
    for line in text:
        token = line.rsplit("/",1) #split on the forward slash to break the word/tag into word,tag
        currTag = token[1] #get the tag
        #print(currTag)
        if currTag not in lastTagDict: #if the current tag is NOT in the dictionary
            lastTagDict[currTag] = {} #create a nested dictionary
            if lastTag not in lastTagDict[currTag]: #if the last tag does NOT already occur before the current tag
                lastTagDict[currTag][lastTag] = 0 
        if currTag in lastTagDict: #if the current tag IS in the dictionary
            if lastTag in lastTagDict[currTag]: #if the last tag DOES already occur before the current tag
                lastTagDict[currTag][lastTag] = lastTagDict[currTag][lastTag] + 1 #increment the frequency by 1
            if lastTag not in lastTagDict[currTag]: #if the last tag does NOT already occur before the current tag
                lastTagDict[currTag][lastTag] = 1 #set it to one, since it NOW does
        lastTag = currTag #update the last tag as the tag we just visited
    #print(lastTagDict)

def buildTagDict(input):
    text = [line for line in input.split(" ") if line != ""]
    for line in text:
        token = line.rsplit("/",1) #split on the forward slash to break the word/tag into word,tag
        tag = token[1] #get tag
        if tag not in tagDict: #if tag is NOT in the dictionary
            tagDict[tag] = 0 #set it equal to zero since it doesn't occur
        if tag in tagDict: #if tag IS in dictionary
            tagDict[tag] = tagDict[tag] + 1 #increment by one since we just saw it occur
    #print(tagDict)  

def tagText(input):
    text = [line for line in input.rsplit(" ") if line != ""]
    #totalCount = 0
    #notInCount = 0
    #print(text)
    lastTag = '.' #use last tag as a . since we treat the first tag in the corpus as right after a new sentence (AKA a start tag)
    for line in text: 
        #totalCount = totalCount + 1
        if line not in wordDict: #if the word is NOT in the word dictionary
            #notInCount = notInCount + 1
            print(line + "/NNP") #assign it a tag of proper noun
        if line in wordDict: #if the word IS in the word dict
            #print("currLine: " + line)
            possibleTags = wordTagDict[line] #get the possible tags associated with that word
            finalProb = 0 
            for currTag in possibleTags: #for each possible tag
                #print(currTag)
                numerator1 = wordTagDict[line][currTag] #get f(current tag, current word)
                denominator1 = wordDict[line] #get f(current word)
                if currTag in lastTagDict: #if the current tag IS in the last tag dictionary
                    if lastTag not in lastTagDict[currTag]: #if this last tag is NOT appearing before the current tag
                        numerator2 = 0 #set to zero since we know it won't be likely
                    #print(currTag)
                    #print(lastTag)
                    else: 
                        numerator2 = lastTagDict[currTag][lastTag] #get f(current tag, last tag)
                else:
                    numerator2 = 0 #set to zero if current tag isn't in the dictionary
                denominator2 = tagDict[lastTag] #get f(last tag)
                wordTagProb = numerator1 / denominator1 #get P(current tag | current word)
                lastTagProb = numerator2 / denominator2 #get P(current tag | last tag)
                currProb = wordTagProb * lastTagProb #get total probability of possible tag
                if currProb > finalProb: #if this possible tag's probability is greater than a previous possible tag's probability
                    finalProb = currProb #set the final probability to the current
                    chosenTag = currTag #update the tag we want to chose
                    lastTag = chosenTag #update the last tag as the tag we just chose
            print(line + "/" + chosenTag) #print the word we're tagging and the chosen tag
#     #totalCount = str(totalCount)
#     #notInCount = str(notInCount)
#     #print("Total count: " + totalCount)
#     #print("Not in Count: " + notInCount)
main()
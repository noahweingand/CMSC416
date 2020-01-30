# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# File Name: eliza.py
# Author: Noah Weingand
# Course Info: CMSC 416 - Spring 2020
# Date Started: January 23, 2020
# Date Due: January 30, 2020
#
# SOURCES
# -------
# 1. Example of Eliza on the web: http://psych.fullerton.edu/mbirnbaum/psych101/Eliza.htm
# 2. Example of Therapist questions: https://www.psychologytoday.com/us/blog/how-do-life/201406/probing-questions-you-should-ask-yourself
# 3. Python API: https://docs.python.org/3/howto/regex.html
#
# HOW IT WORKS?
# -------------
# The program starts by having the user input their name and storing it for reference. If at any moment, after the name is received, the user enters 'bye',
# the program will quit. After entering their name, Eliza will ask a user how they are. The user enters a response and that response is lowercased to limit
# errors in capitalization. The response is sent to the getResponse method where it will look for a match in the response list. After a match is found,
# it randomly chooses a reply from the responses associated with the regex it matched. The match groups are then passed to a reflect method to stage them
# either as a question or in the second-person. The reflect method returns the reflected words to the getResponse method which formats the reflected words 
# with the randomly selected response the regex matcher found. Then it prints a formatted reply. The user will reply back and the algorithm repeats until
# a user ends it.

#imports
import re #regex
import random #for randomizing Eliza's reply
import time #for sleep function

# begin print heading
print("-----------------------------------------E L I Z A---------------------------------------------")
print("Hello, my name is Eliza. I am a Rogerian psychotherapist and I am here to help you. ")
print("Talk to me in gramatically correct English. When you are finished with me, respond with 'bye'.")
print("-----------------------------------------------------------------------------------------------")
# end print heading

# SETUP
playing = True #flag variable controlling when to end the game
name = input("Eliza: what is your name? ") #have the user input their name
print("Eliza: Hello " + name + ", how are you today? ") #display name and initiate conversation

# dictionary for reflections so we can flip the statement into a question (works like a hash map)
# kept it brief since points aren't taken off for tense or mis-conjugated scenarios
reflections = {
    "am":"are",
    "i":"you",
    "are":"am",
    "you":"i",
    "my":"your"
}

#reflects a statement the user entered so that it can be said as if it were a question or in second-person
#input: each string after the regex match from the user's input 
#output: a reflected reply
#---------------------------------------------------------------------------------------------------------------------------------
def reflect(lexemes):
    tokens = lexemes.split() #split the user's input by whitespace into a list of strings
    for index, currToken in enumerate(tokens): #enumerate makes the split list of tokens countable so it can be used in a for loop
        if currToken in reflections: #if the token is found in the reflections dictonary
            tokens[index] = reflections[currToken] #make that token the reflected
    space = ' ' #space for between response in response list and reflected user reply
    return space.join(tokens) #returns a string of the parsed tokens with the corrected reflections

# list of responses Eliza will say using a regex pattern, triggering a list of responses
# References Source 2
responseList = [
    [r'i am (.*)', #this catches for a person describing their feelings, whereabouts, current state, etc.
        ["Why are you {0}?",
          "Do you have an idea of why you are {0}?",
          "Why are you {0}, " + name + "?"]],
    [r'i\'?m (.*)', #same as above, just a contraction
        ["Why are you {0}?",
         "Do you know why you are {0}?"]],
    [r'i feel (.*)', ["Why do you feel {0}?"]], #catches for how one is feeling
    [r'i think(.*)?', ["Why do you think {0}?", "Have you ever thought the opposite?"]], #catches for what a user is thinking. Could be their opinion or a description.
    [r'i don\'?t know(.*)?', #if a user doesn't know the answer or is being lazy, it keeps the conversation going
        ["Why is that?",
         "You have to know something, even if it seems minuscule. Why don't you know?"]],      
    [r'i (.*)', #keeps the conversation going by asking them why
        ["How so?", 
         "Why is that?", 
         "How's that?", 
         "Do you know why you {0}?", 
         "Why {0}?"]],
    [r'because? i am(.*)', #same as I am
        ["Why are you {0}?",
         "Can you prove you {0}?",
         "Do you have an idea of why you {0}?"]],
    [r'because? i\'?m? (.*)', #same as i am contraction
        ["Why are you {0}?",
         "Can you prove you {0}?",
         "Do you have an idea of why you {0}?"]],
    [r'because (.*)', ["How do you know that {0}?"]], #general because to keep conversation going after they give reasoning to something Eliza asked them
    [r'they (.*)', ["How do you know that {0}?", "Tell me more about them?"]], #when the user is referencing other people, it asks about them
    [r'that (.*)', ["Where did this come from?"]], #for when a user is giving explanation to what something might mean
    [r'why (.*)\?', ["Couldn't I ask you that?"]], #when the user asks it a question, rebuttals with a question
    [r'how (.*)\?', ["Couldn't I ask you that?"]], #same as before
    [r'no(\s?)(.*)?', ["Why not?", "Why not, " + name + "?"]], #for when the user is being negative, or answers a question with no
    [r'yes(\s?)(.*)?', #for when a user answers a question yes
        ["Why is that, " + name + "?", 
         "Why is that?", 
         "Why?", 
         "Have you ever thought the opposite?"]], 
    [r'she (.*)?', ["Tell me more about her.", #If a user references a woman-identifying person, it can ask questions concerning that person
                    "Do you interact with women a lot?", 
                    "How involved is she in your life?", 
                    "How does she affect you?"]],
    [r'he (.*)?', ["Tell me more about him.", #same as above but from a man-identifying perspective
                   "Do you interact with men a lot?", 
                   "How involved is he in your life?", 
                   "How does he affect you?"]],  
    [r'okay(.*)?', ["Don't be so reserved. What else can we talk about?"]], #for if the user gives a lazy or brief response of okay
    [r'quit', ["If you're trying to exit the program, please type 'bye'."]], #if the user is trying to stop the program or forgot how to
    [r'exit', ["If you're trying to exit the program, please type 'bye'."]], #same as above
    [r'stop', #same as above, except it includes if the user is trying to stop Eliza from talking about something it doesn't like.
        ["Stop what? If you mean the program, please type 'bye'. If you mean this topic, let us change it. Tell me about someone in your life."]],
    [r'(.*)', ["Tell me more!", #catches anything, purpose is to not let the conversation die
               "Why?",
               "Why might this be?",
               "Do you think this is normal?",
               "What else can you tell me?", 
               "Do you think this infers anything about you?",
               "I don't think I understand. Can you tell me more?"]]
]

#parses a regex pattern associated with responses and randomly chooses a response for the base of the reply
#input: user's input from terminal or the cmd line
#output: a reply the user will read from Eliza
#references Source 3
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def getResponse(userInput):
    for aRegex, responses in responseList: #for each regex and list of responses, associated with that regex, in the response list
        aMatch = re.match(aRegex, userInput.rstrip(".,;!")) #select a match by stripping the user's input of punctuation and checking each regex pattern
        if aMatch: #if a match exists
            response = random.choice(responses) #choose a random response from the responses
            return response.format(*[reflect(group) for group in aMatch.groups()]) 
            # ^This^ returns the response. first we get a tuple of the reply via groups() and check each string to see if it needs to be reflected.
            # After, it appends the reflected statement to the response randomly chosen from the response list.

#Traffic logic
while playing: #while the game is being played
    userInput = input().lower() #take user's input and make it lowercase
    if userInput == "bye": #if the user enters bye
        print("Your machine will self-destruct in 3...") 
        time.sleep(.5) #pause the program for a half second
        print("2...")
        time.sleep(.5)
        print("1...")
        time.sleep(1)
        print("Just kidding! 😂😂😂")
        print("Goodbye, " + name + "!")
        playing = False #stop game 
        break #exit while loop to stop Eliza from continuing
    print ("Eliza: " + getResponse(userInput)) #prints Eliza's reply
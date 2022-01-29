# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 00:09:38 2022

@author: ajipp

Wordle Solver

"""

# =============================================================================
# General Setup
# =============================================================================

import pandas as pd
import string

dictionary = open("D:\Coding Folder\Dictionary\Dictionary.txt")
rawDict = dictionary.read()
words = rawDict.split()

# =============================================================================
# Determining which words/letters are best to start with
# =============================================================================

# since we're dealing with wordle, we only give a shit about 5 letter words that
# 1. don't have numbers/special characters, and that are 2. lower case, for simplicity 

fiveLetters = []

for word in words:
    if len(word) == 5 and word.isalpha() == True:
        fiveLetters.append(word.lower())


# now to count instances of letters

alphabet = list(string.ascii_lowercase)

def countLetters(fl):
    lc = []
    for letter in alphabet:
        total = sum(w.count(letter) for w in fl)
        lc.append(total)
        
    return lc    

letterCounts = countLetters(fiveLetters)
  
letterData = pd.DataFrame(list(zip(alphabet, letterCounts)),
                  columns = ['Letter', 'Instances'])

# this deals with the upcoming scores; I don't like duplicates

def getUniqueLetters(fl):
    ul = []
    for w in fl:
        ul.append(list(set(w)))
    
    return ul

uniqueLetters = getUniqueLetters(fiveLetters)


# turns out a, e, s, i, and o are the most popular letters, in that order
# looks like aesir, raise, etc. are probably your best starting words
# lets run a test to formalize that conjecture...

def findScore(w, ld):
    score = 0
    for letter in range(0, len(w)):
        score = score + ld['Instances'][ord(w[letter])-97]
    return score

def getScore(ul, fl, ld):
    ws = []
    
    for i in range(len(fl)):
        ws.append(findScore(ul[i], ld))
    return ws

wordScore = getScore(uniqueLetters, fiveLetters, letterData)
    
def getPossible(fl, ws):
    pw = pd.DataFrame(list(zip(fl, ws)), columns = ['Word', 'Score'])
    
    return pw
    
possibleWords = getPossible(fiveLetters, wordScore)
resetDict = possibleWords.copy(deep = True)

# =============================================================================
# Actually playing the game
# =============================================================================

# We need a way of inputting words, but first, a quick way to split strings

def convertToList(string):
    lst = []
    lst[:0] = string
    return lst

# Guess function

def guess(g, res):
    letters = convertToList(g)
    checks = convertToList(res)
    dummy = []
    for l in g:
        dummy.append(g.count(l))
    count = dummy
    guessData = pd.DataFrame(list(zip(letters, checks, dummy, count)), 
                             columns = ['Letters', 'Checks', 'Dummy', 'Count'])
    guessData['Checks'] = guessData['Checks'].astype(int)
    guessData['Dummy'] = guessData['Dummy'].astype(int)
    guessData['Count'] = guessData['Count'].astype(int)
    
    for i in range(5):
        if guessData['Checks'][i] == 0:
            guessData['Count'][i] = guessData['Count'][i] - 1
    
    
    return guessData

# Check function

def check(data):
    for i in range(len(data)):
        if data['Checks'][i] == 1:  # drop words that don't have correct letter in that place
            for word in possibleWords['Word']:
                if data['Letters'][i] not in word:
                    possibleWords.drop(possibleWords.index[possibleWords['Word'] == word], inplace=True)
                else:
                    if i != word.index(data['Letters'][i]):
                        possibleWords.drop(possibleWords.index[possibleWords['Word'] == word], inplace=True)
        elif data['Checks'][i] == 0:  # drop words that have a non-letter
            for word in possibleWords['Word']:
                if data['Letters'][i] in word:
                    possibleWords.drop(possibleWords.index[possibleWords['Word'] == word], inplace=True)
        elif data['Checks'][i] == 2: # drop words with correct letter not in that place
            for word in possibleWords['Word']:
                if data['Letters'][i] in word[i]:
                    possibleWords.drop(possibleWords.index[possibleWords['Word'] == word], inplace = True)
                elif data['Letters'][i] not in word:
                    possibleWords.drop(possibleWords.index[possibleWords['Word'] == word], inplace=True)

    return possibleWords
            

# Checks for Niche Cases of Duplicates
           
def nicheCheck(data):
    for i in range(len(data)):
        for word in possibleWords['Word']:
            if data['Letters'][i] == word[i] and data['Count'][i] > word.count(word[i]):
                possibleWords.drop(possibleWords.index[possibleWords['Word'] == word], inplace = True)
    
    return possibleWords
                

# One Small Function for Uniqueness of 'Checks' Values

def isUnique(vals):
    check = vals.to_numpy()
    return (check[0] == check).all()

# Finally, the Game

def main():
    attempt = input("Please input your guess: ")
    outcome = input("Please input the result of your guess: 0 means miss, 1 means hit, 2 means in word: ")
    check(guess(attempt, outcome))
    nicheCheck(guess(attempt, outcome))
    letterCounts = countLetters(possibleWords['Word'])
    letterData = pd.DataFrame(list(zip(alphabet, letterCounts)),
                      columns = ['Letter', 'Instances'])
    uniqueLetters = getUniqueLetters(possibleWords['Word'])
    wordScore = getScore(uniqueLetters, possibleWords['Word'], letterData)
    possibleWords['Score'] = wordScore
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    

#!/usr/bin/env python3
import re
import os
import sys
import json
import random
import requests
import platform
from colorama import Fore, Style
from prettytable import PrettyTable

# setup colours
err = Fore.LIGHTRED_EX + "[X]" + Style.RESET_ALL
okay = Fore.LIGHTGREEN_EX + "[+]" + Style.RESET_ALL
info = Fore.LIGHTYELLOW_EX + "[!]" + Style.RESET_ALL

# init. some globals
userDiff = []
userGuessed = []
randomNumber = 0 
url = 'https://japanesenumberconverter.com/converter/'
availDiffs = ['easy', 'medium', 'hard', 'extreme', 'fluent']

# clear the screen
def clear():
    if platform.system == 'Linux':
        os.system('clear')
    else:
        os.system('cls')

# generate a random number; ranging by level: easy 1-100 \\ medium 100-1000 \\ hard 1000-10k \\ extreme 10k-100k \\ fluent 100k-maxint.
def chooseDiff():
    while True:
        try:
            print('\n' + okay, 'welcome to the japanese number trainer!')
            print(okay, 'please select a difficulty:\n')
            # generate table for diffs.
            difficultyTable = PrettyTable(['easy', 'medium', 'hard', 'extreme', 'fluent'])
            difficultyTable.add_row(['1-100', '100-1k', '1k-10k', '10k-100k', '100k-999m'])
            print(difficultyTable)
            userChoice = input('\n\r>>> ')
            if userChoice.lower() in availDiffs:
                userDiff.append(userChoice)
                userDiffChoice = ' '.join(userDiff)
                print('\n' + info, 'you selected:' + Fore.LIGHTYELLOW_EX, '{}'.format(userDiffChoice))
                break
            else:
                clear()
                print('\n' + err, 'error. please select one of the following options:' + Fore.LIGHTYELLOW_EX, 'easy, medium, hard, extreme, fluent' + Style.RESET_ALL)
        except KeyboardInterrupt:
            print('\n\n' + info, 'caught user interrupt.' + Fore.LIGHTRED_EX, 'exiting' + Style.RESET_ALL + '...')
            sys.exit(1) 

# generate a number with two arguments
def generateNumber(i, j):
    global randomNumber 
    randomNumber = random.randint(i, j)
    print(okay, 'your new number is:' + Fore.LIGHTYELLOW_EX, '{}'.format(randomNumber) + Style.RESET_ALL)

# with the generator function created, remember the range of the userDiff and generate according to that
def generateFromDiff():
    if userDiff[0] == 'easy': # 1-100
        i = 1 
        j = 100
        generateNumber(i, j)
    elif userDiff[0] == 'medium': # 100-1000
        i = 100
        j = 1000
        generateNumber(i, j)
    elif userDiff[0] == 'hard': # 1000-10000
        i = 1000
        j = 10000
        generateNumber(i, j)
    elif userDiff[0] == 'extreme': # 10000-100000
        i = 10000
        j = 100000
        generateNumber(i, j)
    elif userDiff[0] == 'fluent': # 100000-999999999
        i = 100000
        j = 999999999 # the site is limited to this
        generateNumber(i, j)

# string digit checker
def checkString(string):
    return bool(re.search(r'\d', string)) # check if there's a decimal in the user string, return True if there is

# validate user guess
def userGuess():
    print(okay, 'what would' + Fore.LIGHTYELLOW_EX, '{}'.format(randomNumber), Style.RESET_ALL + 
          'be in japanese? (you can enter in' + Fore.LIGHTYELLOW_EX, 'hiragana' + Style.RESET_ALL + ',', 
          Fore.LIGHTYELLOW_EX + 'kanji' + Style.RESET_ALL + ',', 'or' + Fore.LIGHTYELLOW_EX, 'romanji' + Style.RESET_ALL + '!)')
    while True:
        try:
            userInput = input('\n\r>>> ')
            string = userInput
            if checkString(string) == False:
                userGuessed.append(userInput)
                userValidate = ' '.join(userGuessed)
                print('\n' + info, 'you supplied:' + Fore.LIGHTYELLOW_EX, '{}'.format(userValidate), Style.RESET_ALL)
                break
            else:
                print('\n' + err, 'please only input alphabetical characters. no digits.')
        except KeyboardInterrupt:
            print('\n\n' + info, 'caught user interrupt.' + Fore.LIGHTRED_EX, 'exiting' + Style.RESET_ALL + '...')
            sys.exit(1) 

# compare with the value on the website
def compareValues():
    request = requests.post(url, data={'convert_number' : randomNumber}) 
    response = json.loads(request.text.encode('utf8'))
    # print('[+] {}'.format(response['hiragana']))
    # print('[+] {}'.format(response['kanji']))
    # print('[+] {}'.format(response['romanji']).replace('Romanji: ', ''))
    # create a table for better viewing 
    table = PrettyTable(['hiragana', 'kanji', 'romanji'])
    table.add_row([response['hiragana'].replace('Hiragana: ', ''), response['kanji'].replace('Kanji: ', ''), response['romanji'].replace('Romanji: ', '')])
    # check to see if the user got the value right
    # make these dictionary keys prettier and more usable; if needed
    kanji = response['kanji'].replace('Kanji: ', '')
    romanji = response['romanji'].replace('Romanji: ', '')
    hiragana = response['hiragana'].replace('Hiragana: ', '')

    if userGuessed[0] == romanji or userGuessed[0] == hiragana or userGuessed[0] == kanji:
        print(okay, 'you got it right!\n')
        print(table)
    else:
        print(err, 'sorry! please try again.')
        print(info, Fore.LIGHTYELLOW_EX + '{}'.format(randomNumber), Style.RESET_ALL + 'in japanese is:\n')
        print(table)
 
if __name__ == '__main__':
    clear()
    chooseDiff()
    generateFromDiff()
    userGuess()
    compareValues()

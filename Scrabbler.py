#!/usr/bin/python

import pickle
from itertools import combinations


class Scrabbler:

    def __init__(self):
        self.hand_letters = ""
        self.board_letters = ""
        self.wordDict = {}
        self.all_letters = ""
        self.word_list = set()

    def permute(self):
        self.word_list = set()
        self.all_letters = self.hand_letters + self.board_letters
        self.all_letters = sorted(self.all_letters)
        for i in range(1, len(self.all_letters) + 1):
            for word in combinations(self.all_letters, i):
                if
                if ''.join(word) in self.wordDict:
                    for real_word in self.wordDict[''.join(word)]:
                        if self.board_letters in real_word:
                            self.word_list.add(real_word)

    def init_scrabbler(self):
        print("Welcome to Scrabbler!")
        print("Given an arbitrary set of letters to be played and a sequence of letters on the board,")
        print("Scrabbler search for all possible word combinations according to the dictionary of your choice.")
        print("Which dictionary would you like to use? For sowpods,enter 1. ")
        dictionary = input("For twl06, enter 2. For english, enter 3.\n")
        while True:
            if dictionary == '1':
                self.wordDict = pickle.load(open("dicts/sowpods.pick", 'rb'))
                break
            elif dictionary == '2':
                self.wordDict = pickle.load(open("dicts/twl106.pick", 'rb'))
                break
            elif dictionary == '3':
                self.wordDict = pickle.load(open("dicts/english.pick", 'rb'))
                break
            else:
                dictionary = input("The only valid inputs are 1,2,3. Try again:\n")

        while True:
            self.hand_letters = input("Input the letters in your hand, \
                                Use a forward slash for blanks '/'. Ex: dei/bp:\n")
            print("Input the letter sequence you wish to put your tiles around. Leave blank if you just want to find ")
            self.board_letters = input("word combinations from the letters in your hand:\n")
            self.permute()
            print("Word List:")
            for word in self.word_list:
                print(word)
            input()

if __name__ == '__main__':
    scrabbler = Scrabbler()
    scrabbler.init_scrabbler()

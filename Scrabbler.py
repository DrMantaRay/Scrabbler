#!/usr/bin/python

import pickle
from itertools import combinations


# Class that finds possible words given tiles in hand and on the board

class WordFinder:
    # initializes various useful variables
    def __init__(self):
        self.hand_letters = ""
        self.board_letters = ""
        self.wordDict = {}
        self.all_letters = ""
        self.word_list = set()

    # permutes the entered word and finds possible words
    def permute(self):
        alpha_list = "abcdefghijklmnopqrstuvwxyz"
        self.word_list = set()
        self.all_letters = self.hand_letters + self.board_letters
        self.all_letters = sorted(self.all_letters)
        for i in range(1, len(self.all_letters) + 1):
            for word in combinations(self.all_letters, i):
                if '/' in word:
                    num_blanks = word.count('/')
                    for filler in combinations(num_blanks*alpha_list, num_blanks):
                        filled_word = ''.join(sorted(self.blank_replace(''.join(word), filler)))
                        if filled_word in self.wordDict:
                            for real_word in self.wordDict[filled_word]:
                                if self.board_letters in real_word:
                                    self.word_list.add(real_word)

                elif ''.join(word) in self.wordDict:
                    for real_word in self.wordDict[''.join(word)]:
                        if self.board_letters in real_word:
                            self.word_list.add(real_word)

    # helper function that replaces blanks with a substring
    def blank_replace(self, string, substring):
        return_string = []
        i = 0
        for char in string:
            if char == '/':
                return_string.append(substring[i])
                i += 1
            else:
                return_string.append(char)
        return ''.join(return_string)

    # the ui for word finder
    def init(self):
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
            self.hand_letters = \
                input("Input the letters in your hand,Use a forward slash for blanks '/'. Example: dei/bp...\n")
            print("Input the letter sequence you wish to put your tiles around. Leave blank if you just want to find ")
            self.board_letters = input("word combinations from the letters in your hand...\n")
            self.permute()
            print("Word List:")
            for word in sorted(self.word_list):
                print(word)
            input("Press enter to start over")


def main():
    word_finder = WordFinder()
    word_finder.init()

if __name__ == '__main__':
    main()

#!/usr/bin/python

import gamefiles
import settings
from bot import Bot


class PlayGame:
    def __init__(self):
        self.board = None
        self.turn = 0

    def play(self):
        print("Welcome to Scrabble!")
        num_players = int(input("Enter the number of total players:"))
        num_ai = int(input("Enter the number of computer players:"))
        self.choose_game(1, num_players, num_ai)
        while True:
            player_num = self.turn % num_players
            print("*: TW, +: DW, $: DL, #: TL")
            print("There are " + str(len(self.board.tile_list)) + " tiles left. It is turn " + str(self.turn) + ".")
            print("It is player " + str(player_num) + "'s turn.")
            score_string = "Scoreboard: | "
            i = 0
            for player in self.board.players:
                score_string = score_string + "Player " + str(i) + ": " + str(player.score) + " | "
                i += 1
            print(score_string)
            print(self.board)
            if self.board.players[player_num].machine is True:
                Bot.play(self.board, player_num)
                self.turn += 1

            else:
                while True:
                    print("Your letters are: " + str(self.board.players[player_num].letter_vals(self.board.tile_dict))+ "\n")
                    pass_turn = False
                    letters_swapped = False

                    while True:
                        print("Type the word you wish to play.")
                        word = input("To pass, type an exclamation mark (!). To swap, type a tilde (~): \n")
                        if word.isalpha():
                            word = str(word)
                            if self.board.dict_check(word):
                                break
                            else:
                                print("That word is not in the dictionary. Try again.")
                                continue
                        elif word == '!':
                            pass_turn = True
                            break
                        elif word == '~':

                            if len(self.board.tile_list) == 0:
                                print("There are no letters left to swap! \n")
                                continue

                            while True:
                                swap_letters = input("Type the letters you wish to swap. To cancel type (~): \n")
                                res = self.board.swap_tiles(self.board.players[player_num], swap_letters)
                                print(self.board.players[player_num].get_letters())
                                if res == 0:
                                    print("There are not enough remaining letters to do the swap. Please try again.")
                                    continue
                                elif res == 1 \
                                        and len(swap_letters) > 0:
                                    letters_swapped = True
                                    break
                                elif swap_letters == "~":
                                    break
                                else:
                                    print("Please enter letters from your hand.")

                            if letters_swapped is True:
                                pass_turn = True
                                break
                        else:
                            print("That word is invalid! \n")

                    if pass_turn is True:
                        self.turn += 1
                        break

                    while True:
                        x = input("Enter the x coordinate of the first letter of the word: \n")
                        if x.isdigit():
                            x = int(x)
                            if 0 < x < 15:
                                break
                        print("Please enter a valid number between 1 and 14")

                    while True:
                        y = input("Enter the y coordinate of the first letter of the word: \n")
                        if y.isdigit():
                            y = int(y)
                            if 0 < y < 15:
                                break
                        print("Please enter a valid number between 1 and 14")
                    
                    while True:
                        orientation = input("Enter the orientation of the word: h for horizontal and v for vertical: \n")
                        if orientation == 'h' or orientation == 'v':
                            break
                        else:
                            print("Please enter a valid orientation, either h or v")

                    score = self.board.play_word(self.board.players[player_num], word, x, y, orientation)
                    if score > 0:
                        self.turn += 1
                        input("The move \"" + word + "\" scored " + str(score) + " points. Press 'enter' to continue.\n")
                        self.board.fill_tiles(self.board.players[player_num])
                        break
                    else:
                        print("That is not a valid play. Try again! \n")

    def choose_game(self, number, num_players, num_ai):
        if number == 1:
            self.board = gamefiles.Board("boards/WordsWithFriends.txt", "dicts/sowpods.pick", num_players)
            self.board.load_tiles(settings.words_with_friends_dict)
            for i in range(num_players - num_ai, num_players):
                self.board.players[i].machine = True
            for player in self.board.players:
                self.board.fill_tiles(player)


def main():
    game = PlayGame()
    game.play()

if __name__ == '__main__':
    main()

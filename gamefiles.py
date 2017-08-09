import csv
import settings
import pickle
import random

# Class for the game board
class Board:
    # Initializes game board, as well as well loading the BoardTiles into a 2D array
    def __init__(self, boardfile, word_dict_path, num_players):
        self.height = 15
        self.width = 15
        self.board_array = [[None for i in range(self.width)] for j in range(self.width)]
        self.num_players = num_players
        self.players = [Player() for i in range(num_players)]
        self.tile_list = []
        self.tile_dict = {}
        self.out_of_letters = 0
        self.first_turn = True
        self.word_dict = pickle.load(open(word_dict_path, 'rb'))

        for player in self.players:
            self.fill_tiles(player)

        y_pos = 0
        with open(boardfile, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in csvreader:
                x_pos = 0
                for item in row:
                    self.board_array[x_pos][y_pos] = BoardTile(x_pos, y_pos, item)
                    x_pos += 1
                y_pos += 1

    # Fills a players tiles if there are still tiles left
    def fill_tiles(self, player):
        while len(player.get_letters()) < 7:
            if not self.tile_list:
                self.out_of_letters = 1
                break
            else:
                player.add_letter(self.tile_list.pop()[0])

    @staticmethod
    def contains(small, big):
        for i in range(len(big) - len(small) + 1):
            for j in range(len(small)):
                if big[i + j] != small[j]:
                    break
            else:
                return i, i + len(small)
        return False

    def swap_tiles(self, player, tiles):
        if len(tiles) > len(self.tile_list):
            return 0
        if self.contains(tiles, player.get_letters()):
            player.remove_letters(tiles)
            self.fill_tiles(player)
            self.add_tiles(tiles)
            return 1
        else:
            return -1

    # Plays a word, and updates the player's score. Returns -1 if the word played is invalid and 1 if successful
    def play_word(self, player, word, x_pos, y_pos, orientation):
        score = 0
        tiles = set()
        if self.check_word(player, word, x_pos, y_pos, orientation) and self.dict_check(word):
            if orientation == 'v':
                for y in range(y_pos, y_pos + len(word)):
                    if not self.board_array[y][x_pos].is_alpha():
                        if word[y-y_pos] in player.get_letters():
                            player.remove_letters(word[y-y_pos])
                        else:
                            player.remove_letters('/')
                    self.board_array[y][x_pos].set_letter(word[y-y_pos])
                    tiles.add(self.board_array[y][x_pos])
                for y in range(y_pos, y_pos + len(word)):
                    if self.board_array[y][x_pos].multiplier is False:
                        continue
                    cross_word = self.get_word_at_xy(x_pos, y, 'h', word[y-y_pos])
                    if len(cross_word[0]) > 1:
                        score += self.score(cross_word[1], cross_word[2], cross_word[0], 'h')
                        for x_cor in range(cross_word[1], len(word) + cross_word[1]):
                            tiles.add(self.board_array[y][x_cor])
                score += self.score(x_pos, y_pos, word, orientation)
            elif orientation == 'h':
                for x in range(x_pos, x_pos + len(word)):
                    if not self.board_array[y_pos][x].is_alpha():
                        if word[x-x_pos] in player.get_letters():
                            player.remove_letters(word[x-x_pos])
                        else:
                            player.remove_letters('/')
                    self.board_array[y_pos][x].set_letter(word[x-x_pos])
                    tiles.add(self.board_array[y_pos][x])
                for x in range(x_pos, x_pos + len(word)):
                    if self.board_array[y_pos][x].multiplier is False:
                        continue
                    cross_word = self.get_word_at_xy(x, y_pos, 'v', word[x-x_pos])
                    if len(cross_word[0]) > 1:
                        score += self.score(cross_word[1], cross_word[2], cross_word[0], 'v')
                        for y_cor in range(cross_word[1], len(word) + cross_word[1]):
                            tiles.add(self.board_array[y_cor][x])
                score += self.score(x_pos, y_pos, word, orientation)
            self.first_turn = False
            for tile in tiles:
                tile.multiplier = False
            player.increment_score(score)
            if type(score) is int:
                return score
            else:
                return -1
        else:
            return -1

    # Checks to see if a proposed word is adjacent to an already played word
    def check_adjacency(self, word, x_pos, y_pos, orientation):
        if orientation == 'h':
            for x in range(max(x_pos-1,0), min(x_pos +len(word)+1, self.width)):
                for y in range(max(y_pos-1, 0), min(y_pos +1, self.height)):
                    if self.board_array[y][x].is_alpha() is True:
                        return True
        elif orientation == 'v':
            for x in range(max(x_pos-1,0), min(x_pos + 1, self.width)):
                for y in range(max(y_pos-1, 0), min(y_pos + len(word) + 1, self.height)):
                    if self.board_array[y][x].is_alpha() is True:
                        return True
        return False

    # Checks to see if the proposed word fits on the board and if the player has the correct letters to play it
    def check_word(self, player, word, x_pos, y_pos, orientation):
        star_tile = False
        remaining_letter_list = list(player.get_letters())
        blanks = 0

        # Checks to see if the move is adjacent to tiles already plays if it is not the first turn
        if self.check_adjacency(word, x_pos, y_pos, orientation) is False and self.first_turn is False:
            return False

        # Keeps track of remaining blank tiles, if any
        for letter in remaining_letter_list:
            if letter == '/':
                blanks += 1
        if orientation == 'h':
            if x_pos + len(word) > self.height:
                return False
            for x in range(x_pos, x_pos + len(word)):
                if self.board_array[y_pos][x].is_filled():
                    if self.board_array[y_pos][x].is_alpha():
                        if self.board_array[y_pos][x].get_letter() != word[x-x_pos]:
                            return False
                    elif self.board_array[y_pos][x].get_letter() == '@':
                        star_tile = True
                    else:
                        if word[x-x_pos] in remaining_letter_list:
                            remaining_letter_list.remove(word[x-x_pos])
                        elif blanks > 0:
                            blanks += (-1)
                            remaining_letter_list.remove('/')
                        else:
                            return False
                else:
                    if word[x-x_pos] in remaining_letter_list:
                        remaining_letter_list.remove(word[x-x_pos])
                    elif blanks > 0:
                        blanks += (-1)
                        remaining_letter_list.remove('/')
                    else:
                        return False
                cross_word = self.get_word_at_xy(x, y_pos, 'v', word[x-x_pos])
                if len(cross_word[0]) > 1:
                    if not self.dict_check(cross_word[0]):
                        return False

        if orientation == 'v':
            if y_pos + len(word) > self.width:
                return False
            for y in range(y_pos, y_pos + len(word)):
                if self.board_array[y][x_pos].is_filled():
                    if self.board_array[y][x_pos].is_alpha():
                        if self.board_array[y][x_pos].get_letter() != word[y-y_pos]:
                            return False
                    elif self.board_array[y][x_pos].get_letter() == '@':
                        star_tile = True
                    else:
                        if word[y-y_pos] in remaining_letter_list:
                            remaining_letter_list.remove(word[y-y_pos])
                        elif blanks > 0:
                            blanks += (-1)
                            remaining_letter_list.remove('/')
                        else:
                            return False
                else:
                    if word[y-y_pos] in remaining_letter_list:
                        remaining_letter_list.remove(word[y-y_pos])
                    elif blanks > 0:
                        blanks += (-1)
                        remaining_letter_list.remove('/')
                    else:
                        return False
                cross_word = self.get_word_at_xy(x_pos, y, 'v', word[y-y_pos])
                if len(cross_word[0]) > 1:
                    if not self.dict_check(cross_word[0]):
                        return False
        if len(remaining_letter_list) == len(player.get_letters()):
            return False
        if self.first_turn is True:
            if star_tile is False:
                return False
        return True

    # Checks to make sure a word is in the dictionary being used.
    def dict_check(self, word):
        word_sorted = ''.join(sorted(word))
        if word_sorted in self.word_dict:
            if word in self.word_dict[word_sorted]:
                return True
        return False

    # Returns a score for a word. Note that this function only calculates score along one dimension, i.e. one word at
    # time.
    def score(self, x_pos, y_pos, word, orientation):
        multiplier = 1
        return_score = 0
        tiles = []
        if orientation == 'h':
            for x in range(x_pos, x_pos + len(word)):
                tiles.append(self.board_array[y_pos][x])
        elif orientation == 'v':
            for y in range(y_pos, y_pos + len(word)):
                tiles.append(self.board_array[y][x_pos])

        for tile in tiles:
            if tile.multiplier is True:
                if tile.special == '*':
                    multiplier *= 3
                    return_score += self.tile_dict[tile.get_letter()][1]
                elif tile.special == '$':
                    return_score += 2 * self.tile_dict[tile.get_letter()][1]
                elif tile.special == '+':
                    multiplier *= 2
                    return_score += self.tile_dict[tile.get_letter()][1]
                elif tile.special == '#':
                    return_score += 3 * self.tile_dict[tile.get_letter()][1]
                else:
                    return_score += self.tile_dict[tile.get_letter()][1]
            else:
                return_score += self.tile_dict[tile.get_letter()][1]
        return multiplier * return_score

    # Returns possible words going through a specific location on the board. Useful for finding extra words
    # formed from laying down tiles
    def get_word_at_xy(self, x_pos, y_pos, orientation, letter):
        word = letter
        x = x_pos
        y = y_pos
        if orientation == 'v':
            while y + 1 < self.height and self.board_array[y + 1][x].is_alpha():
                word = word + self.board_array[y + 1][x].get_letter()
                y += 1
            y = y_pos
            while y - 1 > 0 and self.board_array[y - 1][x].is_alpha():
                word = self.board_array[y - 1][x].get_letter() + word
                y += (-1)
            return word, x_pos, y
        elif orientation == 'h':
            while x + 1 < self.width and self.board_array[y][x + 1].is_alpha():
                word = word + self.board_array[y][x + 1].get_letter()
                x += 1
            x = x_pos
            while x - 1 > 0 and self.board_array[y][x - 1].is_alpha():
                word = self.board_array[y][x - 1].get_letter() + word
                x += (-1)
            return word, x, y_pos

    # Loads a tile configuration
    def load_tiles(self, dict):
        self.tile_dict = dict
        self.tile_list = settings.form_word_list(self.tile_dict)

    def add_tiles(self, tiles):
        for tile in tiles:
            self.tile_list.append((tile, self.tile_dict[tile][1]))
        random.shuffle(self.tile_list)

    # Resets the boardd
    def reset(self):
        self.tile_list = settings.form_word_list(self.tile_dict)

    def change_player_type(self, player_number, type):
        if type == "machine":
            self.player[player_number].machine = True
        elif type == "human":
            self.player[player_number].machine = False
        else:
            print("The only two player types are human or machine")

    # Prints the board with coordinates
    def __str__(self):
        i = 0
        line_print = ""
        for row in self.board_array:
            for column in row:
                line_print = line_print + " " + str(column)
            line_print = line_print + " " + str(i) + "\n"
            i += 1
        line_print += " 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4\n"
        return line_print


# Defines a tile on the board. Numerous helpful functions.
class BoardTile:
    def __init__(self, x , y, letter):
        self.char = ''
        self.x = x
        self.y = y
        self.letter = letter
        self.multiplier = True
        self.special = letter

    def __str__(self):
        return self.letter

    def set_letter(self, letter):
        self.letter = letter

    def get_letter(self):
        return self.letter

    def is_filled(self):
        return self.letter != "_"

    def is_empty(self):
        return self.letter == "_"

    def is_alpha(self):
        return self.letter.isalpha()


# Defines the Player class, which keeps track of letters held and the player score.
class Player:
    def __init__(self):
        self.score = 0
        self.letters = []
        self.machine = False

    def get_score(self):
        return self.score

    def increment_score(self, change):
        self.score += change

    def get_letters(self):
        return self.letters

    def remove_letters(self, letters):
        for letter in letters:
            self.letters.remove(letter)

    def add_letter(self, letter):
        self.letters.append(letter)

    def set_letters(self, letters):
        self.letters = letters

    def letter_vals(self, val_dict):
        return_list = []
        for letter in self.letters:
            return_list.append((letter, val_dict[letter][1]))
        return return_list

#Testing the Board
def main():
    board = Board("boards/WordsWithFriends.txt", "dicts/sowpods.pick", 2)
    board.load_tiles(settings.words_with_friends_dict)
    print(board)
    board.players[0].set_letters(['t', 'e', 'a', 'l', 'w'])
    print(board.play_word(board.players[0], "teal", 7, 7, 'v'))
    print(board)
    board.players[0].set_letters([ 'w', 'e', 'd', 't', 'e'])
    print(board.play_word(board.players[0], "wed", 7, 9, 'h'))
    print(board)
    board.players[0].set_letters(['f', 'e', '/', 't', 'e'])
    print(board.play_word(board.players[0], "few", 6, 8, 'h'))
    print(board.check_word(board.players[0], "few", 6, 8, 'h'))
    print(board)

if __name__ == '__main__':
    main()

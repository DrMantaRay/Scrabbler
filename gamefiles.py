import csv
import settings
import pickle

class Board:
    def __init__(self, boardfile, word_dict_path, num_players):
        self.height = 15
        self.width = 15
        self.board_array = [[None for i in range(self.width)] for j in range(self.width)]
        self.num_players = num_players
        self.players = [Player() for i in range(num_players)]
        self.tile_list = []
        self.tile_dict = {}
        self.out_of_letters = 0
        self.first_turn = 1
        self.word_dict = pickle.load(open(word_dict_path, 'rb'))

        for player in self.players:
            self.fill_tiles(player)

        x_pos = 0
        y_pos = 0
        with open(boardfile, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in csvreader:
                x_pos = 0
                for item in row:
                    self.board_array[x_pos][y_pos] = BoardTile(x_pos, y_pos, item)
                    x_pos += 1
                y_pos += 1

    def fill_tiles(self, player):
        while len(player.get_letters()) < 7:
            if not self.tile_list:
                self.out_of_letters = 1
                break
            else:
                player.add_letter(self.tile_list.pop())

    def play_word(self, player, word, x_pos, y_pos, orientation):
        remaining_letter_list = player.getletters()
        blanks = 0
        for letter in remaining_letter_list:
            if letter == '/':
                blanks += 1
        if orientation == 'v':
            assert(y_pos + len(word) <= self.height)
            for y in range(y_pos, y_pos + len(word)):
                if self.board_array[x_pos][y].isfilled():

                else:
                    self.board_array[x_pos][y].set_letter(word[y])
        if orientation == 'h':
            assert(x_pos + len(word) <= self.width)
            for x in range(x_pos, x_pos + len(word)):
                self.board_array[x][y_pos].set_letter(word[x])

    def word_check(self, word):
        word_sorted = sorted(word)
        if word_sorted in self.word_dict:
            if word in self.word_dict[word_sorted]:
                return True
        return False


    def get_word_at_xy(self, x_pos, y_pos, orientation):
        word = self.board_array[x_pos][y_pos].get_letter()
        x = x_pos
        y = y_pos
        if orientation == 'v':
            while y + 1 < self.board.height and self.board_array[x][y + 1].is_filled():
                word = word + self.board_array[x][y + 1].get_letter()
                y+=1
            y = y_pos
            while y - 1 > 0 and self.board_array[x][y - 1].is_filled():
                word = self.board_array[x][y - 1].get_letter() + word
                y+= (-1)
            return word
        elif orientation == 'h':
            while x + 1 < self.board.width and self.board_array[x + 1][y].is_filled():
                word = word + self.board_array[x + 1][y].get_letter()
                x+=1
            x = x_pos
            while x - 1 > 0 and self.board_array[x - 1][y].is_filled():
                word = self.board_array[x - 1][y].get_letter() + word
                x+= (-1)
            return word

    def load_tiles(self, dict):
        self.tile_dict = dict
        self.tile_list = settings.form_word_list(self.tile_dict)

    def reset(self):
        self.tile_list = settings.form_word_list(self.tile_dict)

    def __str__(self):
        line_print = "\n"
        for row in self.board_array:
            for column in row:
                if line_print == "":
                    line_print = str(column)
                else:
                    line_print = line_print + " " + str(column)
            line_print = line_print + "\n"
        return line_print


class BoardTile:
    def __init__(self, x , y, letter):
        self.char = ''
        self.x = x
        self.y = y
        self.letter = letter

    def __str__(self):
        return self.letter

    def set_letter(self, letter):
        self.letter = letter

    def get_letter(self):
        return self.letter

    def is_filled(self):
        return self.letter != ""

    def is_empty(self):
        return self.letter == ""

    def is_alpha(self):
        return self.letter.isalpha()
class Player:
    def __init__(self):
        self.score = 0
        self.letters = []

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

def main():
    board = Board("boards/WordsWithFriends.txt", 2)
    print(board)
    board.play_word(1, "hello", 0, 0, 'v')
    print(board)

if __name__ == '__main__':
    main()

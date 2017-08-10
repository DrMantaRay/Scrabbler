import scrabbler
import gamefiles
import settings


class Bot:

    @staticmethod
    def play(board, player_num):

        if board.first_turn is True:
            Bot.best_move_first_turn(board, board.players[player_num])
            return


    @staticmethod
    def best_move_first_turn(board, player):
        score = 0
        move = None
        word_finder = scrabbler.WordFinder()
        word_finder.wordDict = board.word_dict
        word_finder.hand_letters = "".join(player.get_letters())
        word_finder.permute()
        for x in range(board.width//2 - 6, board.width//2):
            for word in word_finder.word_list:
                if board.width//2 not in range(x, x + len(word)):
                    continue
                word_score = board.score(x, board.height//2, word, "h")
                if word_score > score:
                    score = word_score
                    move = (word, x, board.height//2, "h", score)
        if move is None:
            val = board.swap_tiles(player, player.get_letters())
            print("The player has chosen to swap tiles")
            return
        total_score = board.play_word(player, move[0], move[1], move[2], move[3])
        print(board)
        input("The move \"" + move[0] + "\" scored " + str(total_score) + " points. Press 'enter' to continue.\n")
        board.fill_tiles(player)

    def best_move(self, board, player):
        score = 0
        move = None
        word_finder = scrabbler.WordFinder()
        word_finder.wordDict = board.word_dict
        word_finder.hand_letters = "".join(player.get_letters())

        for x in range(0, board.width):
            for y in range(0, board.height):
                board_tiles = []
                if board.check_adjacency("aaaaaaa", x, y, "h") is True:
                    for x_cor in range(x, x + 7):
                        if board.board_array[x][y].is_alpha():
                            board_tiles.append(board.board_array[x][y].get_letter())
                    word_finder.board_letters = "".join(board_tiles)
                    word_finder.permute()
                    for word in word_finder.word_list:
                        if board.check_word(player, word, x, y, "h"):

                if board.check_adjacency("aaaaaaa", x, y, "v") is True:

    def best_future_move(self, board):
        pass

def main():
    board = gamefiles.Board("boards/WordsWithFriends.txt", "dicts/enable.pick", 2)
    board.load_tiles(settings.words_with_friends_dict)
    print(board)

if __name__ == '__main__':
    main()





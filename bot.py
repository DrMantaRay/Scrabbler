import scrabbler
import gamefiles
import settings


#The bot methods are contained in this class
class Bot:
    # wrapper for best_move_first_turn and best_move
    @staticmethod
    def play(board, player_num):

        if board.first_turn is True:
            Bot.best_move_first_turn(board, board.players[player_num])
            return
        else:
            (total_score, move) = Bot.best_move(board, board.players[player_num])
            if total_score == 0:
                print("The player has chosen to pass")
            elif total_score == -1:
                print("The player has chosen to swap tiles")
            else:
                print(board)
                input("The move \"" + move[0] + "\" scored " + str(total_score) + " points. Press 'enter' to continue.\n")
                board.fill_tiles(board.players[player_num])

    # Looks for the best move the first turn
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
            num_letters = min(len(player.get_letters()), len(board.tile_list))
            if num_letters == 0:
                print("The player has chosen to pass")
                return
            board.swap_tiles(player, player.get_letters()[0:num_letters])
            print("The player has chosen to swap tiles")
            return

        total_score = board.play_word(player, move[0], move[1], move[2], move[3])
        print(board)
        input("The move \"" + move[0] + "\" scored " + str(total_score) + " points. Press 'enter' to continue.\n")
        board.fill_tiles(player)

    # Looks for the best move after the first turn
    @staticmethod
    def best_move(board, player):
        score = 0
        move = None
        word_finder = scrabbler.WordFinder()
        word_finder.wordDict = board.word_dict
        word_finder.hand_letters = "".join(player.get_letters())

        for x in range(0, board.width):
            for y in range(0, board.height):
                if board.board_array[y][x].is_alpha():
                    continue
                board_tiles = []
                if board.check_adjacency("aaaaaaa", x, y, "h") is True:
                    for x_cor in range(x, x + 7):
                        if board.board_array[y][x].is_alpha():
                            board_tiles.append(board.board_array[y][x].get_letter())
                    word_finder.board_letters = "".join(board_tiles)
                    word_finder.permute()
                    for word in word_finder.word_list:
                        if board.check_word(player, word, x, y, "h"):
                            if board.score_all(x, y, word, "h") > score:
                                score = board.score_all(x, y, word, "h")
                                move = (word, x, y, "h")
                if board.check_adjacency("aaaaaaa", x, y, "v") is True:
                    for y_cor in range(y, y + 7):
                        if board.board_array[y][x].is_alpha():
                            board_tiles.append(board.board_array[y][x].get_letter())
                    word_finder.board_letters = "".join(board_tiles)
                    word_finder.permute()
                    for word in word_finder.word_list:
                        if board.check_word(player, word, x, y, "v"):
                            if board.score_all(x, y, word, "v") > score:
                                score = board.score_all(x, y, word, "v")
                                move = (word, x, y, "v")

        if move is None:
            num_letters = min(len(player.get_letters()), len(board.tile_list))
            if num_letters == 0:
                return (0, move)
            board.swap_tiles(player, player.get_letters()[0:num_letters])
            return (-1, move)
        total_score = board.play_word(player, move[0], move[1], move[2], move[3])

        return (total_score, move)


    def best_future_move(self, board):
        pass

# Scrabble Cheat program
def main():
    board = gamefiles.Board("boards/WordsWithFriends.txt", "dicts/enable.pick", 1)
    board.load_tiles(settings.words_with_friends_dict)
    l = []
    while len(board.tile_list) > 0:
        l.append(board.tile_list.pop()[0])
    def play_word(word, x, y , pos):
        if word =="denims":
            print(l)
        board.players[0].set_letters(list(l))
        score = board.play_word(board.players[0], word, x, y, pos)
        return

    play_word("yuch", 6, 7, "h")
    play_word("op",6,8,"h")
    play_word("sexed", 7, 9, "h")
    play_word("bi", 10, 8, "h")
    play_word("bate", 11, 7, "h")
    play_word("ut", 9, 10, "h")
    play_word("om", 13, 8, "h")
    play_word("lemurs", 14, 6, "v")
    play_word("litten", 5, 8, "v")
    play_word("stead", 4, 8, "v")
    play_word("pore", 3, 11, "v")
    play_word("ave", 10, 11, "h")
    play_word("ag",9,6,"h")
    play_word("equip",5,5,"h")
    play_word("cutter",5,1,"v")
    play_word("new",2,12,"v")
    play_word("jug",4,2,"h")
    play_word("flag", 7,0,"v")
    play_word("not", 3,3,"h")
    play_word("zed",12,10,"v")
    play_word("folky",7,0,"h")
    play_word("hoer",8,4,"h")
    play_word("oi",9,1,"h")
    play_word("aha",1,12,"v")
    play_word("vein", 11,11,"v")
    play_word("rhea", 13, 11, "v")
    play_word("fair", 10,3,"h")
    print(board.score_all(0,0,"denims","h"))
    play_word("denims",0,0,"h")
    play_word("vids",0,14,"v")
    print(board)
    board.players[0].set_letters(list("w"))
    Bot.play(board, 0)

if __name__ == '__main__':
    main()





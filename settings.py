# settings for scrabble

import random

words_with_friends_dict = \
    {'/': (2, 0), 'a': (9, 1), 'b': (2, 4), 'c': (2, 4), 'd': (5, 2), 'e': (13, 1), 'f': (2, 4),
     'g': (3, 3), 'h': (4, 3), 'i': (8, 1), 'j': (1, 10), 'k': (1, 5), 'l': (4,2), 'm': (2, 4), 'n': (5, 2),
     'o': (8, 1), 'p': (2, 4), 'q': (1, 10), 'r': (6, 1), 's': (5, 1), 't': (7, 1), 'u': (4, 2), 'v': (2, 5),
     'w': (2, 4), 'x': (1, 8), 'y': (2, 3), 'z': (1, 10)}


def form_word_list(word_dict):
    return_array = []
    for word in word_dict:
        for freq in range(0, word_dict[word][0]):
            return_array.append((word, word_dict[word][1]))
    random.shuffle(return_array)
    return return_array




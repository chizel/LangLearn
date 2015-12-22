#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re


class Crossword():
    def __init__(self, words, size_r=30, size_c=30):
        self.words = self.sort_words_by_length(words)
        # number of rows
        self.size_r = size_r
        # number of columns
        self.size_c = size_c

        self.check_words()
        self.__init_field__()
        return

    def check_words(self):
        for word in self.words:
            if not re.match('^[a-z]+$', word):
                raise TypeError(word + ' contains wrong characters!')

    def __init_field__(self):
        '''generate empty crossword field by size size_r, size_c'''
        self.field = []
        li = ['' for _ in range(self.size_c)]
        for i in range(self.size_r):
            self.field.append(li[:])
        return

    def print_field(self):
        for line in self.field:
            s = ''
            for cell in line:
                if cell:
                    s += cell
                else:
                    s += '*'
            print(s)
        return

    def sort_words_by_length(self, words):
        return sorted(words, key=len, reverse=True)

    def write_word_to_field(self, word, r0, c0, axis):
        '''Write word to the field.

        '*' in a cell means you can't write a symbol to this cell
        (start and end of a word).

        Axis must be 'v' (vertical) or 'h' (horizontal).
        '''
        word_len = len(word)

        if axis == 'h':
            if c0 + word_len > self.size_c:
                raise TypeError('You are crossed field\'s bounds!')

            # write '*' before the start of the word
            if c0 > 0:
                self.field[r0][c0 - 1] = '*'

            for i in range(word_len):
                self.field[r0][c0 + i] = word[i]
                # add character to list of characters
                self.chars[word[i]].add((r0, c0 + i))

            # write '*' after the end of the word
            if c0 + i + 1 < self.size_c:
                self.field[r0][c0 + i + 1] = '*'

        elif axis == 'v':
            if r0 + word_len > self.size_r:
                raise TypeError('You are crossed field\'s bounds!')

            # write '*' before the start of the word
            if r0 > 0:
                self.field[r0 - 1][c0] = '*'

            for i in range(word_len):
                self.field[r0 + i][c0] = word[i]
                # add character to list of characters
                self.chars[word[i]].add((r0 + i, c0))

            # write '*' after the end of the word
            if r0 + i + 1 < self.size_r:
                self.field[r0 + i + 1][c0] = '*'
        else:
            raise TypeError('Wrong axis argument! Must be "h" or "v"!')
        return

    def place_word(self, word):
        word_len = len(word)

        def check_column(word, char_pos, row_id, column_id):
            # row index where first word's letter will be placed
            #1  d<====
            #2brother
            #3  g
            start_row = row_id - char_pos

            # Does word will cross field's borders
            if start_row < 0:
                return False
            elif start_row + word_len >= self.size_r:
                return False

            # check is upper cell has no letters
            #1   <====
            #2  d
            #3brother
            #4  g
            if (start_row - 1) >= 0 and self.field[start_row - 1][column_id]:
                return False

            # Does cell after the last cell of the word has smth in it?
            if (start_row + word_len) < self.size_r and\
                    self.field[start_row + word_len][column_id]:
                return False

            # check every cell and neighbour cells on contain letters
            for i in range(len(word)):
                if i == char_pos:
                    # this is where words crossing each other
                    continue

                current_row_id = start_row + i

                # right cell
                if (column_id + 1) < self.size_c and\
                        self.field[current_row_id][column_id + 1]:
                    return False
                # current cell
                if self.field[current_row_id][column_id]:
                    return False
                # left cell
                if (column_id - 1) >= 0 and\
                        self.field[current_row_id][column_id - 1]:
                    return False
            return (start_row, column_id, 'v')

        def check_row(word, char_pos, row_id, column_id):
            word_len = len(word)

            # column index where first word's letter will be placed
            start_column = column_id - char_pos

            # Does word will cross field's borders
            if start_column < 0:
                return False
            elif start_column + word_len >= self.size_c:
                return False

            # Does cell prior the first cell has smth in it
            if (start_column - 1) >= 0 and\
                    self.field[row_id][start_column - 1]:
                return False

            # Does cell after the last word cell has smth in it
            if (start_column + word_len) < self.size_c and\
                    self.field[row_id][start_column + word_len]:
                return False

            # check every cell and neighbour cells on contain letters
            for i in range(word_len):
                if i == char_pos:
                    # this is where words crossing each other
                    continue

                current_column_id = start_column + i

                # upper cell
                if (row_id - 1) >= 0 and\
                        self.field[row_id - 1][current_column_id]:
                    return False
                # current cell
                if self.field[row_id][current_column_id]:
                    return False
                # lower cell
                if (row_id + 1) < self.size_r and\
                        self.field[row_id + 1][current_column_id]:
                    return False
            return (row_id, start_column, 'h')

        for char_pos in range(word_len):
            if self.chars[word[char_pos]]:
                # position was found, check it is it ok
                coordinates = self.chars[word[char_pos]]

                for row_id, column_id in coordinates:
                    res = check_row(word, char_pos, row_id, column_id)
                    if res:
                        self.write_word_to_field(word, *res)
                        return res
                    res = check_column(word, char_pos, row_id, column_id)
                    if res:
                        self.write_word_to_field(word, *res)
                        return res
        return False

    def generate_crossword(self):
        self.chars = {chr(a): set() for a in range(ord('a'), ord('z') + 1)}

        # placing init word
        self.write_word_to_field(self.words[0], 3, 3, 'h')
        word_count = 1
        word_coordinates = {}
        word_coordinates[self.words[0]] = (3, 3, 'h')

        for word in self.words[1:]:
            coord = self.place_word(word)
            if coord:
                #save coordinates
                word_coordinates[word] = coord
                word_count += 1
            if word_count == 15:
                break
        return word_coordinates


def main():
    #words = ('transmission', 'pepper', 'trumpet', 'elephant', 'ocean',
             #'cottage', 'basketball', 'zoo')

    #TODO REMOVE IT
    import sqlite3
    #TODO END

    conn = sqlite3.connect('engwords.db')
    c = conn.cursor()
    query = '''SELECT word, translation FROM "words"
             WHERE length(word) < 15 ORDER BY RANDOM() LIMIT 30;'''
    c.execute(query)
    tmp_words = c.fetchall()
    conn.close()
    words = []

    for word in tmp_words:
        if re.match('^[a-z]+$', word[0]):
            words.append(word[0])

    mc = Crossword(words, size_r=30, size_c=30)
    coordinates = mc.generate_crossword()
    mc.print_field()
    print(coordinates)
    return


if __name__ == "__main__":
    main()

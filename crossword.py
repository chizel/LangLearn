#! /usr/bin/env python3
# -*- coding: utf-8 -*-


def show(*argv, **kwarg):
    for arg in argv:
        print(arg)
    for k, v in kwarg.items():
        prin(k, v)
    exit()


class Crossword():
    def __init__(self, words, size_r=30, size_c=30):
        self.words = words
        # number of rows
        self.size_r = size_r
        # number of columns
        self.size_c = size_c

        self.__init_field__()
        self.sort_words_by_length()
        return

    def __init_field__(self):
        '''generate empty crossword field by size size_r, size_c'''
        self.field = []
        li = ['' for _ in range(self.size_c)]
        for i in range(self.size_r):
            self.field.append(li[:])
        return

    def pfield(self):
        for line in self.field:
            s = ''
            for cell in line:
                if cell:
                    s += cell
                else:
                    s += '*'
            print(s)
        return

    def sort_words_by_length(self):
        self.sorted_words = sorted(self.words, key=len, reverse=True)
        return

    def write_word_to_field(self, word, r0, c0, axis):
        '''Write word to the field.

        '*' in a cell means you can't write a symbol to this cell
        (start and end of word).

        '''
        word_len = len(word)

        if axis == 'row':
            if c0 + word_len > self.size_c:
                raise TypeError('You are crossed field\'s bounds!')

            if c0 > 0:
                self.field[r0][c0 - 1] = '*'

            for i in range(word_len):
                self.field[r0][c0 + i] = word[i]
                self.chars[word[i]].add((r0, c0 + i))

            if c0 + i + 1 < self.size_c:
                self.field[r0][c0 + i + 1] = '*'

        elif axis == 'column':
            if r0 + word_len > self.size_r:
                raise TypeError('You are crossed field\'s bounds!')

            if r0 > 0:
                self.field[r0 - 1][c0] = '*'

            for i in range(word_len):
                self.field[r0 + i][c0] = word[i]
                self.chars[word[i]].add((r0 + i, c0))

            if r0 + i + 1 < self.size_r:
                self.field[r0 + i + 1][c0] = '*'
        else:
            raise TypeError('Wrong axis argument! Must be "row" or "column"!')
        return

    def place_word(self, word):
        word_len = len(word)

        def check_column(word, char_pos, row_id, column_id):
            # row index where first word's letter will be placed
            #1  d<====
            #2brother
            #3  g
            start_row = row_id - char_pos

            # word will cross field's bounds
            if start_row < 0:
                return False

            # check if upper cell has no letters
            #1   <====
            #2  d
            #3brother
            #4  g
            if (start_row - 1) >= 0 and self.field[start_row - 1][column_id]:
                return False

            # is cell after the last cell of the word has something in it?
            if (start_row + word_len) < self.size_r and\
                    self.field[start_row + word_len][column_id]:
                return False

            for i in range(len(word)):
                if i == char_pos:
                    # this is where words crossing each other
                    continue

                current_row_id = start_row + i

#TODO CHECK BOUNDS!!!
                # right cell
                if self.field[current_row_id][column_id + 1]:
                    return False
                #current cell
                if self.field[current_row_id][column_id]:
                    return False
                # left cell
                elif self.field[current_row_id][column_id - 1]:
                    return False
            return (start_row, column_id, 'column')

        def check_row(word, char_pos, row_id, column_id):
            word_len = len(word)

            # column index where first word's letter will be placed
            start_column = column_id - char_pos

            # Does word will cross field's borders
            if start_column < 0:
                return False

            # does cell prior the first cell has something in it
            if (start_column - 1) >= 0 and\
                    self.field[row_id][start_column - 1]:
                return False

            # check is cell after the last word cell has something in it
            if (start_column + word_len) < self.size_c and\
                    self.field[row_id][start_column + word_len]:
                return False

            for i in range(word_len):
                if i == char_pos:
                    # this is where words crossing each other
                    continue

                current_column_id = start_column + i

                # upper cell
                if self.field[row_id - 1][current_column_id]:
                    return False
                # current cell
                if self.field[row_id][current_column_id]:
                    return False
                # lower cell
                elif self.field[row_id + 1][current_column_id]:
                    return False
            return (row_id, start_column, 'row')

        for char_pos in range(word_len):
            if self.chars[word[char_pos]]:
                # position was found, check it is it ok
                coordinates = self.chars[word[char_pos]]

                for row_id, column_id in coordinates:
                    res = check_row(word, char_pos, row_id, column_id)
                    if res:
                        self.write_word_to_field(word, *res)
                        return (res[0], res[1])
                    res = check_column(word, char_pos, row_id, column_id)
                    if res:
                        self.write_word_to_field(word, *res)
                        return (res[0], res[1])
        return False

    def generate_crossword(self):
        self.chars = {chr(a): set() for a in range(ord('a'), ord('z') + 1)}

        # placing init word
        self.write_word_to_field(self.sorted_words[0], 3, 3, 'row')
        word_count = 1
        word_coordinates = {}
        word_coordinates[self.sorted_words[0]] = (3, 3)

        for word in self.sorted_words[1:]:
            coord = self.place_word(word)
            if coord:
                #save coordinates
                word_coordinates[word] = coord
                word_count += 1
            if word_count == 15:
                break

        #self.place_word(self.sorted_words[1])
        #self.place_word(self.sorted_words[2])
        self.pfield()
        #print(sorted(self.chars.items()))
        self.word_coordinates = word_coordinates
        return


def main():
    #words = ('transmission', 'pepper', 'trumpet', 'elephant', 'ocean',
             #'cottage', 'basketball', 'zoo')

    #TODO REMOVE IT
    import sqlite3
    import re
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
    mc.generate_crossword()
    print(mc.word_coordinates)
    return


if __name__ == "__main__":
    main()

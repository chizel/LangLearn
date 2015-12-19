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
            print(line)
        return

    def sort_words_by_length(self):
        self.sorted_words = sorted(self.words, key=len, reverse=True)
        return

    def write_word_to_field(self, word, r0, c0, axis):
        '''Write word to the field.

        '*' in a cell means you can't write a symbol to this cell
        (start and end of word).

        '''

        # TODO: keep words' coordinates for simple navigation
        #i.e. ((x0,y0)(x1,y1))
        # TODO: keep letters' coordinates
        #letters = {'a':[(0,0), (5,7)], 'b':[], c:[(1,0)], ...}

        word_len = len(word)

        if axis == 'row':
            if c0 + word_len > self.size_c:
                raise TypeError('You are crossed field\'s bounds!')

            if c0 > 0:
                self.field[r0][c0 - 1] = '*'

            for i in range(word_len):
                self.field[r0][c0 + i] = word[i]
                self.chars[word[i]].add((r0, c0 + i))

            if c0 + i < self.size_c:
                self.field[r0][c0 + i + 1] = '*'

        elif axis == 'column':
            if r0 + word_len > self.size_r:
                raise TypeError('You are crossed field\'s bounds!')

            if r0 > 0:
                self.field[r0 - 1][c0] = '*'

            for i in range(word_len):
                self.field[r0 + i][c0] = word[i]
                self.chars[word[i]].add((r0 + i, c0))

            if r0 + i < self.size_r:
                self.field[r0 + i + 1][c0] = '*'
        else:
            raise TypeError('Wrong axis argument! Must be "row" or "column"!')
        return

    def place_word(self, word):
        word_len = len(word)

        #def check_cell(r, c):
            #self.field[r][c]
            #return

        def check_row(word, r, c):
            return False

        def check_column(word, char_pos, row_ind, column_ind):
            # row index where first word's letter will be placed
            #1  d<====
            #2brother
            #3  g
            start_row = row_ind - char_pos

            # word will cross field's bounds
            if start_row < 0:
                return False

            # check if upper cell has no letters
            #1   <====
            #2  d
            #3brother
            #4  g
            if (start_row - 1) >= 0 and self.field[start_row - 1][column_ind]:
                return False

            for i in range(len(word)):
                if i == char_pos:
                    # this is where words crossing each other
                    continue

                current_row_ind = start_row + i

                # right cell
                if self.field[current_row_ind + i][column_ind]:
                    return False
                # left cell
                elif self.field[current_row_ind - i][column_ind]:
                    return False
            return (start_row, column_ind, 'column')

        for char_pos in range(word_len):
            if self.chars[word[char_pos]]:
                # position was found, check it is it ok
                coordinates  = self.chars[word[char_pos]]

                for row_ind, column_ind in coordinates:
                    #check_row()
                    res = check_column(word, char_pos, row_ind, column_ind)
                    if res:
                        self.write_word_to_field(word, *res)
                        return True
        return False

    def generate_crossword(self):
        self.chars = {chr(a): set() for a in range(ord('a'), ord('z') + 1)}

        # placing init word
        self.write_word_to_field(self.sorted_words[0], 3, 3, 'row')
        self.place_word(self.sorted_words[1])
        self.place_word(self.sorted_words[2])
        self.pfield()
        #print(sorted(self.chars.items()))
        return None


def main():
    words = ('transmission', 'pepper', 'trumpet', 'elephant', 'ocean',
             'cottage', 'basketball', 'zoo')
    mc = Crossword(words, size_r=30, size_c=30)
    mc.generate_crossword()
    return


if __name__ == "__main__":
    main()

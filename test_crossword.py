#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from crossword import Crossword


class TestCrossword(unittest.TestCase):

    def test_check_words(self):
        with self.assertRaises(TypeError):
            words = ['Wrong']
            cw = Crossword(words)
            words = ['_word']
            cw = Crossword(words)
            words = ['r ong']
            cw = Crossword(words)

    def test_init_field(self):
        words = ['word']
        cw = Crossword(words, 10, 5)
        self.assertEqual(len(cw.field), 5)
        self.assertEqual(len(cw.field[0]), 10)

    def test_sort_words_by_length(self):
        words = ['a', 'long', 'ok']
        cw = Crossword(words)
        ws = cw.sort_words_by_length(words)
        self.assertEqual(ws[0], words[1])
        self.assertEqual(ws[1], words[2])
        self.assertEqual(ws[2], words[0])

    def test_generate_crossword(self):
        words = ['tree', 'orb', 'forest', 'start']
        cw = Crossword(words)
        cw.generate_crossword()
        # <f>orest
        self.assertEqual(cw.field[3][3], 'f')
        # or<b>
        self.assertEqual(cw.field[5][4], 'b')
        # sta<r>t
        self.assertEqual(cw.field[6][7], 'r')
        # tr<e>e
        self.assertEqual(cw.field[7][9], 'e')
        # tre<e>
        self.assertEqual(cw.field[7][10], 'e')

if __name__ == "__main__":
    unittest.main()

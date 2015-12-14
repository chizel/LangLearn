#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *

class LearnWords():
    def __init__(self, limit, db_name='engwords.db'):
        self.read_words(random=True, limit=limit):

    def read_words(self, random=True, limit=0):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        query = 'SELECT word, translation FROM "words"'
        query += 'WHERE length(word) < 15'

        if random:
            query += 'ORDER BY RANDOM()'

        if limit:
            query += 'LIMIT %d' % limit

        query += ';'
        c.execute()
        self.words = c.fetchall() 
        conn.close()
        return

    def get_words(self, count=10):
        for i in range(count):
            yield self.words[i]
 
    def interface(self):
        root = Tk()

def main():
    lw = LearnWords(10)
    print(lw.get_words())
    return


if __name__ == "__main__":
    main()


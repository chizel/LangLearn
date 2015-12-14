#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import sqlite3


class LearnWords():
    def __init__(self, db_name='engwords.db'):
        self.db_name = db_name

    def read_words(self, random=True, limit=10):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        query = 'SELECT word, translation FROM "words" '
        query += 'WHERE length(word) < 15 '

        if random:
            query += 'ORDER BY RANDOM() '

        if limit:
            query += 'LIMIT %d' % limit

        query += ';'
        c.execute(query)
        self.words = c.fetchall()
        conn.close()
        return

    def get_words(self, count=10):
        self.read_words(random=True, limit=count)
        for i in range(count):
            yield self.words[i]
        return None

    def init_gui(self, font_size=14):
        self.root = tk.Tk()
        self.font_size = font_size
        #e = Entry(root)
        #e.pack()
        #s=e.get()

    def spell_words(self, word_count=10):
        self.init_gui()
        words = self.read_words(word_count)
        self.pos = 0

        # label with result
        result_lbl = tk.Label(self.root,
                              font=self.font_size,
                              text='Write your answer below!')
        result_lbl.pack()
        answer_ent = tk.Entry(self.root,
                              font=self.font_size,
                              width=50)
        answer_ent.focus()
        answer_ent.pack()

        def check_answer():
            answer = answer_ent.get()
            answer_ent.delete(0, 'end')

            if answer == self.word[0]:
                result_lbl.config(text='Right!')
            else:
                result_lbl.config(text=answer + ' not ' + self.word[0])
            self.word = next(words)
            word_lbl.config(text=self.word[1])

        # word translation label
        word_lbl = tk.Label(self.root,
                            font=self.font_size, 
                            text=self.word[1])
        word_lbl.pack()

        self.root.bind('<Return>', lambda e: check_answer())

        # button to answer
        answer_btn = tk.Button(self.root, text="Answer",
                               width=10,
                               command=check_answer)
        answer_btn.pack()
        self.root.mainloop()
        return


def main():
    lw = LearnWords()
    lw.spell_words(10)
    return


if __name__ == "__main__":
    main()

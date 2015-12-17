#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import sqlite3
import random


class LearnWords():
    def __init__(self, db_name='engwords.db'):
        self.db_name = db_name

    def read_words(self, random=True, limit=10):
        # for random answers
        limit *= 2
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

    def get_words(self, word_count=10):
        self.read_words(random=True, limit=word_count)
        for i in range(word_count):
            yield self.words[i]
        return None

    def get_random_items(self, items, items_count, include):
        res = random.sample(items, items_count)

        if not items[include] in res:
            res[0] = items[include]

        random.shuffle(res)
        return res

    def init_gui(self, font_size=18):
        self.root = tk.Tk()
        self.font_size = font_size

        # menu
        menu_bar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        task_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Tasks', menu=task_menu)
        task_menu.add_command(label='Spell words', command=self.spell_word)
        task_menu.add_command(label='Guess word translation', command=self.guess_word_translation)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About...", command='')

        self.root.config(menu=menu_bar)
        # end menu


        min_x = 800
        max_x = 800
        min_y = 500
        max_y = 500
        self.root.minsize(min_x, min_y)
        self.root.maxsize(max_x, max_y)
        #screen_width = root.winfo_screenwidth()
        #screen_height = root.winfo_screenheight()
        self.root.mainloop()

    def guess_word_translation(self, word_count=10):
        self.read_words(random=True, limit=word_count)
        self.pos = 0

        self.root.title('Guess word translation')
        frame = tk.Frame(self.root, bd=5, relief=tk.RIDGE, width=800, height=500)
        frame.place(x=100,y=100)
        #frame.configure(background='black')

        word_lbl = tk.Label(frame,
                            font=self.font_size,
                            text='Press enter to start',
                            width=20,
                            wraplength=150,
                            #anchor=tk.W,
                            justify=tk.CENTER
                            )
        result_lbl = tk.Label(frame,
                              text='',
                              font=self.font_size,
                              )
        left_lbl = tk.Label(frame,
                            text='',
                            font=self.font_size,
                            width=20,
                            wraplength=150,
                            )
        right_lbl = tk.Label(frame,
                            text='',
                            font=self.font_size,
                            width=20,
                            wraplength=150,
                            )

        def init():
            word = self.words[self.pos]
            word_lbl.configure(text=word[1])
            guesses = self.get_random_items(self.words, 2, self.pos)
            left_lbl.configure(text=guesses[0][0])
            right_lbl.configure(text=guesses[1][0])

        def check_answer(answer):
            word = self.words[self.pos]

            if answer == word[0]:
                result_lbl.config(text='Right!')
            else:
                result_lbl.config(text='Wrong!')

            self.pos += 1
            if self.pos >= word_count:
                #!!!!!!!!!!!!!!!!!!!!! destroing frame
                #!!!!!!!!!!!!!!!!!!!!! need more polishing
                frame.destroy()
                return
            init()

        word_lbl.grid(row=0, column=1)
        word_lbl.configure(background='orange')
        result_lbl.grid(row=1,column=1)
        left_lbl.bind('<Button-1>', lambda e: check_answer(left_lbl.cget('text')))
        left_lbl.grid(row=1, column=0)
        right_lbl.bind('<Button-1>', lambda e: check_answer(right_lbl.cget('text')))
        right_lbl.grid(row=1, column=2)

        frame.bind('<Right>', lambda e: check_answer(right_lbl.cget('text')))
        frame.bind('<Left>', lambda e: check_answer(left_lbl.cget('text')))
        frame.bind('<Return>', lambda e: init())
        frame.focus()
        return

    def spell_word(self, word_count=10):
        self.read_words(word_count)
        frame = tk.Frame(self.root, bd=5, relief=tk.RIDGE, width=800, height=500)
        frame.place(x=100,y=100)
        frame.focus()
        self.pos = 0

        # label with result
        result_lbl = tk.Label(frame,
                              font=self.font_size,
                              text='Write your answer below!')
        result_lbl.pack()
        answer_ent = tk.Entry(frame,
                              font=self.font_size,
                              width=50)
        answer_ent.focus()
        answer_ent.pack()

        def check_answer():
            print('iiii')
            answer = answer_ent.get()
            answer_ent.delete(0, 'end')

            if answer == self.words[self.pos][0]:
                result_lbl.config(text='Right!')
            else:
                result_lbl.config(text=answer + ' not ' + self.words[self.pos][0])

            self.pos += 1
            if self.pos > word_count:
                frame.destroy()
                return
            word_lbl.config(text=self.words[self.pos][1])

        # word translation label
        word_lbl = tk.Label(frame,
                            font=self.font_size, 
                            text=self.words[self.pos][1])
        word_lbl.pack()

        self.root.bind('<Return>', lambda e: check_answer())

        # button to answer
        answer_btn = tk.Button(frame,
                               text="Answer",
                               width=10,
                               command=check_answer)
        answer_btn.pack()
        return


def main():
    lw = LearnWords()
    lw.init_gui()
    #lw.spell_word(10)
    #lw.guess_word_translation(5)
    return


if __name__ == "__main__":
    main()

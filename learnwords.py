#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import sqlite3
import random
import re
from crossword import Crossword


class LearnWords():
    def __init__(self, db_name='engwords.db'):
        self.db_name = db_name
        # [number of right answers, all answers count]
        self.result = [0, 0]
        # default background color
        self.bg_color = '#F8DCB1'
        # a little bit darker than bg_color
        self.bg_darkest = '#E9B96E'
        # color of elemnet if answer is right
        self.color_ok = '#8AE234'
        # color of elemnet if answer is wrong
        self.color_no = '#F34949'

    def read_words(self, random=True, limit=10):
        # TODO decide where to place this code
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

    def get_random_items(self, items, items_count, include):
        '''Returns random items from 'items' in quntaty 'items_count'
        with item[include]'''
        res = random.sample(items, items_count)

        if not items[include] in res:
            res[0] = items[include]

        random.shuffle(res)
        return res

    def init_main_frame(self, sx=0, sy=0, px=0, py=0):
        '''Frame where all other frames placed.
        To clear this main_frame just call this function'''
        self.main_frame = tk.Frame(
            self.root,
            width=sx,
            height=sy,
            bg=self.bg_color
            )
        self.main_frame.place(x=px, y=py)
        return

    def init_gui(self, font_size=18):
        '''Initializing GUI. Creating root window, setting window size,
        creating menubar'''
        self.root = tk.Tk()
        self.font_size = font_size

        self.min_x = 1000
        self.min_y = 700
        max_x = 1300
        max_y = 1200
        self.root.minsize(self.min_x, self.min_y)
        self.root.maxsize(max_x, max_y)

        self.init_main_frame(sx=self.min_x,
                             sy=self.min_y
                             )

        # menu
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='File', menu=file_menu)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.root.destroy)

        task_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Tasks', menu=task_menu)
        task_menu.add_command(
            label='Crossword',
            command=self.crossword)
        task_menu.add_command(
            label='Spell words',
            command=self.spell_word)
        task_menu.add_command(
            label='Guess word translation',
            command=self.guess_word_translation)
        task_menu.add_command(
            label='Translation-word',
            command=lambda: self.word_translation(display=1))
        task_menu.add_command(
            label='Word-translation',
            command=self.word_translation)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='Help', command=self.show_help)
        help_menu.add_command(label='About', command=self.show_about)

        self.root.config(menu=menu_bar)
        # end menu

        #TODO REMOVE
        self.crossword()
        #TODO END

        self.root.bind('<Control-q>', lambda e: self.root.destroy())
        self.root.bind('<Control-Q>', lambda e: self.root.destroy())
        self.root.mainloop()
        return

    def guess_word_translation(self, word_count=10):
        '''You're given word-translation and you need to guess to what
        word from 2 given words it benongs'''
        self.init_main_frame(sx=self.min_x,
                             sy=self.min_y
                             )
        self.read_words(random=True, limit=word_count)

        self.root.title('Guess word translation')
        frame = tk.Frame(self.main_frame,
                         width=1000,
                         height=700,
                         bd=5,
                         relief=tk.RIDGE,
                         )
        frame.place(x=100, y=100)
        word_lbl = tk.Label(frame,
                            font=self.font_size,
                            text='Press enter to start',
                            width=20,
                            wraplength=150,
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

        def fill_lbl():
            '''Filling lefg_lbl and right_lbl'''
            word_lbl.configure(text=self.words[self.pos][1])
            guesses = self.get_random_items(self.words, 2, self.pos)
            left_lbl.configure(text=guesses[0][0])
            right_lbl.configure(text=guesses[1][0])

        def init():
            '''Initializing program, setting key bindings'''
            # disabling return key
            frame.bind('<Return>', lambda e: 1)
            left_lbl.bind('<Button-1>',
                          lambda e: check_answer(left_lbl.cget('text')))
            left_lbl.grid(row=1, column=0)
            right_lbl.bind('<Button-1>',
                           lambda e: check_answer(right_lbl.cget('text')))
            right_lbl.grid(row=1, column=2)

            frame.bind('<Right>',
                       lambda e: check_answer(right_lbl.cget('text')))
            frame.bind('<Left>', lambda e: check_answer(left_lbl.cget('text')))
            self.result[0] = 0
            self.result[1] = word_count
            # current word position in words list
            self.pos = 0
            fill_lbl()

        def check_answer(answer):
            '''checks given answer'''
            word = self.words[self.pos]

            if answer == word[0]:
                result_lbl.config(text='Right!')
                self.result[0] += 1
            else:
                result_lbl.config(text='Wrong!')

            self.pos += 1
            if self.pos >= word_count:
                frame.destroy()
                # send result to main window
                self.show_result()
                return
            fill_lbl()

        frame.bind('<Return>', lambda e: init())
        word_lbl.grid(row=0, column=1)
        word_lbl.configure(background='orange')
        result_lbl.grid(row=1, column=1)
        frame.focus()
        return

    def spell_word(self, word_count=10):
        '''You're given a word translation. You need to spell word from
        memory'''
        self.init_main_frame(sx=self.min_x, sy=self.min_y)
        self.read_words(word_count)
        self.root.title('Spell words')
        frame = tk.Frame(self.main_frame,
                         width=1000,
                         height=700,
                         bd=5,
                         relief=tk.RIDGE,
                         )
        frame.place(x=100, y=100)
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
        self.result[0] = 0
        self.result[1] = word_count

        def check_answer():
            '''Answer checking'''
            answer = answer_ent.get()
            answer_ent.delete(0, 'end')

            if answer == self.words[self.pos][0]:
                result_lbl.config(text='Right!')
                self.result[0] += 1
            else:
                tmp_msg = answer + ' not ' + self.words[self.pos][0]
                result_lbl.config(text=tmp_msg)

            self.pos += 1
            if self.pos >= word_count:
                frame.destroy()
                # send result to main window
                self.show_result()
                return
            word_lbl.config(text=self.words[self.pos][1])

        word_lbl = tk.Label(frame,
                            font=self.font_size,
                            text=self.words[self.pos][1])
        word_lbl.pack()
        answer_ent.bind('<Return>', lambda e: check_answer())
        answer_btn = tk.Button(frame,
                               text='Answer',
                               width=10,
                               command=check_answer)
        answer_btn.pack()
        return

    def word_translation(self, word_count=10, display=0):
        # TODO add informative docstring
        self.init_main_frame(sx=self.min_x,
                             sy=self.min_y
                             )
        self.read_words(random=True, limit=word_count)
        self.pos = 0

        if display == 0:
            word_guess = 1
            window_title = 'Translation-word'
        else:
            word_guess = 0
            window_title = 'Word-translation'

        self.root.title(window_title)

        frame = tk.Frame(self.main_frame,
                         width=700,
                         height=400,
                         bd=5,
                         relief=tk.RIDGE,
                         )
        frame.place(x=0, y=0)

        word_lbl = tk.Label(frame,
                            font=self.font_size,
                            text='Press enter to start',
                            width=20,
                            wraplength=150,
                            justify=tk.CENTER
                            )
        result_lbl = tk.Label(frame,
                              font=self.font_size)
        str_lbls = [tk.StringVar() for _ in range(4)]
        lbls = [tk.Label(frame,
                         textvariable=str_lbls[i],
                         font=self.font_size) for i in range(4)]

        def fill_lbl():
            word = self.words[self.pos]
            word_lbl.configure(text=word[display])
            word_lbl.configure(bg='red')
            guesses = self.get_random_items(self.words, 4, self.pos)
            for i in range(4):
                str_lbls[i].set(guesses[i][word_guess])

        def init():
            frame.bind('<Return>', lambda e: 1)
            for i in range(4):
                tmp_f = lambda e, i=i: check_answer(i)
                lbls[i].bind('<Button-1>', tmp_f)
                frame.bind(str(i + 1), tmp_f)
            self.result[0] = 0
            self.result[1] = word_count
            self.pos = 0
            fill_lbl()

        def check_answer(lbl_id):
            if str_lbls[lbl_id].get() == self.words[self.pos][word_guess]:
                result_lbl.config(text='Right!')
                self.result[0] += 1
            else:
                msg = str_lbls[lbl_id].get()
                msg += ' not ' + self.words[self.pos][word_guess]
                result_lbl.config(text=msg)

            self.pos += 1
            if self.pos >= word_count:
                frame.destroy()
                # send result to main window
                self.show_result()
                return
            fill_lbl()

        frame.bind('<Return>', lambda e: init())
        word_lbl.grid(row=0, column=0)
        result_lbl.grid(row=1, column=0)
        for i in range(4):
            lbls[i].grid(row=i, column=1)
        frame.focus()
        return

    def crossword(self, word_count=15):
        # 0 - horizontal, 1 - vertical
        self.move = 0

        class crossword_cell(tk.Entry):
            def __init__(self, *args, def_char, **kwargs):
                self.def_char = def_char
                super(crossword_cell, self).__init__(*args, **kwargs)

        def create_cell(row, column, char):
            field[row][column] = crossword_cell(
                frame,
                font=self.font_size,
                width=2,
                justify=tk.CENTER,
                bg=self.bg_darkest,
                def_char=char
                )
            field[row][column].grid(row=row, column=column)
            field[row][column].bind('<Key>',
                                    lambda e: check_key(e, row, column))
            field[row][column].bind('<Button>',
                                    lambda e: check_key(e, row, column))
            return

        def fill_field(word, row, column, direction):
            start = (row, column)
            word_len = len(word)

            if direction == 'h':
                for i in range(word_len):
                    create_cell(row, column + i, word[i])
            elif direction == 'v':
                for i in range(word_len):
                    create_cell(row + i, column, word[i])
            else:
                raise TypeError('Wrong axis argument! Must be "h" or "v"!')
            return

        def activate_cell(row, column, direction):
            if direction == 'h':
                self.move = 0
            else:
                self.move = 1
            field[row][column].focus()

        #TODO fix it? is it bug or feature?
        #if someone inserted text(Control+v or middle-mouse)
        #it will be shown even if it contains several character
        def check_key(e, row, column, direction=None):
            key_char = e.char.lower()

            # is it character key was pressed?
            if len(key_char) == 1 and ord('a') <= ord(key_char) <= ord('z'):
                field[row][column].delete(0, 'end')

                # move vertical
                if self.move:
                    if field[row + 1][column]:
                        field[row + 1][column].focus()
                #move horizontal
                else:
                    if field[row][column + 1]:
                        field[row][column + 1].focus()
            # moving to other cells
            elif e.keysym == 'Left':
                if field[row][column - 1]:
                    field[row][column - 1].focus()
                    self.move = 0
            elif e.keysym == 'Right':
                if field[row][column + 1]:
                    field[row][column + 1].focus()
                    self.move = 0
            elif e.keysym == 'Up':
                if field[row - 1][column]:
                    field[row - 1][column].focus()
                    self.move = 1
            elif e.keysym == 'Down':
                if field[row + 1][column]:
                    field[row + 1][column].focus()
                    self.move = 1
            elif e.keysym == 'BackSpace':
                # clear current cell
                if field[row][column]:
                    field[row][column].delete(0, 'end')

                # moving to previous cell
                if self.move:
                    if field[row - 1][column]:
                        field[row - 1][column].focus()
                else:
                    if field[row][column - 1]:
                        field[row][column - 1].focus()
            # mouse click
            elif e.num == 1:
#TODO highlight word translation
                if field[row + 1][column] or field[row - 1][column]:
                    self.move = 1
                else:
                    self.move = 0
            return

        def check_crossword():
            for row in field:
                for cell in row:
                    if not cell:
                        continue
                    answer = cell.get()
                    if cell.def_char == answer:
                        cell.configure(bg=self.color_ok)
                    elif answer != '':
                        cell.configure(bg=self.color_no)
            return

        def reset_cells_bg():
            for row in field:
                for cell in row:
                    if cell:
                        cell.configure(bg=self.bg_darkest)
            return

        #TODO add functionality
        def check_answer():
            return

        self.init_main_frame(sx=self.min_x,
                             sy=self.min_y
                             )
        self.read_words(random=True, limit=word_count)
        frame = tk.Frame(
            self.main_frame,
            width=1000,
            height=700,
            bg=self.bg_color
            )

        #TODO SET PROPER SIZE
        frame.place(x=180, y=0)
        words = []

        for word in self.words:
            if re.match('^[a-z]+$', word[0]):
                words.append(word[0])

        mc = Crossword(words, size_r=30, size_c=30)
        crossword_items = mc.generate_crossword()

        # view translations
        transl_frm = tk.Frame(self.main_frame, bg=self.bg_color)
        transl_frm.place(x=0, y=0)
        transl_lbls = {}

        translations = {}

        field = []
        li = ['' for _ in range(30)]

        for i in range(30):
            field.append(li[:])

        i = 0

        for word, coordinates in crossword_items.items():
            fill_field(word, *coordinates)

            r = coordinates[0]
            c = coordinates[1]
            direction = coordinates[2]

            # find word translation
            for tmp_word, tmp_translation in self.words:
                if word == tmp_word:
                    translations[word] = tmp_translation
                    break

            transl_lbls[word] = tk.Label(
                transl_frm,
                text=translations[word],
                bd=2,
                relief=tk.RIDGE,
                wraplength=150,
                justify=tk.CENTER
                )
            transl_lbls[word].grid(row=i, column=0)
            transl_lbls[word].bind(
                '<Button-1>',
                lambda e, d=direction, r=r, c=c: activate_cell(r, c, d)
                )
            i += 1
        answer_btn = tk.Button(
            transl_frm,
            text='Answer',
            width=10,
            command=check_answer)
        answer_btn.grid()
        check_btn = tk.Button(
            transl_frm,
            text='Check',
            width=10,
            command=check_crossword)
        check_btn.grid()
        frame.focus()
        return

    def show_result(self):
        self.root.title('Result')
        msg = str(self.result[0]) + ' from ' + str(self.result[1])
        tk.Label(self.main_frame, text=msg).pack()
        return

    def show_help(self):
        # TODO add more info
        help_window = tk.Toplevel()
        help_msg = 'Use arrow keys to answer in "Guess word"\n'
        help_msg += 'Use enter to answer in "Spell word"\n'
        help_msg += 'Use Control+q to quit the programm.\n'
        tk.Label(help_window, text=help_msg).pack()
        help_window.bind('<Control-q>', lambda e: help_window.destroy())
        help_window.bind('<Control-Q>', lambda e: help_window.destroy())
        return

    def show_about(self):
        # TODO add more info
        about_window = tk.Toplevel()
        tk.Label(about_window, text='This program is in developmnet').pack()
        about_window.bind('<Control-q>', lambda e: about_window.destroy())
        about_window.bind('<Control-Q>', lambda e: about_window.destroy())
        return


def main():
    lw = LearnWords()
    lw.init_gui()
    return


if __name__ == '__main__':
    main()

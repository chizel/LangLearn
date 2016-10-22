#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import random
import re
import configparser
import tkinter as tk

from crossword import Crossword


class LearnWords():
    def __init__(self, db_name='engwords.db'):
        self.db_name = db_name
        # [number of correct answers, number of all answers]
        self.result = [0, 0]
        self.load_settings()
        # score for current quiz
        self.tmp_result = 0
        #TODO add users and change user_id to input from settings
        self.user_id = 1

        #connecting to db
        self.db_connect = sqlite3.connect(self.db_name)
        self.cursor = self.db_connect.cursor()
        self.read_score()

    def load_settings(self):
        '''Loads settings from file'''
        self.config = configparser.ConfigParser()
        try:
            self.config.read('settings.ini')
        except:
            raise IOError('Can\'t read settings.ini')

        #TODO add window with settings and write them to file
        #        with open('settings.ini', 'w') as configfile:
        #            self.config.write(configfile)

    def read_score(self):
        '''Reading user's score from db'''
        query = '''SELECT score
                    FROM users
                    WHERE id = ?'''

        self.cursor.execute(query, str(self.user_id))
        self.score = int(self.cursor.fetchone()[0])

    def update_score(self, score, answers_count):
        '''Update score (number of right answers) and answers_count
        (number of all answers)'''
        self.score += score

        # writing to db
        query = '''UPDATE users
                SET score=?, answers_count=?
                    WHERE id=?;'''

        self.cursor.execute(query, (score, answers_count, self.user_id))
        self.db_connect.commit()

    def read_words(self, limit=10, random=True):
        '''Reading words from db'''
        limit = int(limit)
        #TODO maybe remove
        # for random answers
        limit *= 2
        query = 'SELECT word, translation FROM "words" '
        query += 'WHERE length(word) < 15 '

        if random:
            query += 'ORDER BY RANDOM() '
        if limit:
            query += 'LIMIT %d' % limit

        query += ';'
        self.cursor.execute(query)
        self.words = self.cursor.fetchall()

    def get_random_items(self, items, items_count, include):
        '''Returns random items from 'items' in quntaty 'items_count'
        with item[include]'''
        res = random.sample(items, items_count)

        if not items[include] in res:
            res[0] = items[include]

        random.shuffle(res)
        return res

    def init_main_frame(self):
        '''Frame where all other frames placed.
        To clear this main_frame just call this function'''
        self.main_frame = tk.Frame(
            self.root,
            width=self.config['gui']['min_w'],
            height=self.config['gui']['min_h'],
            bg=self.config['colors']['bg']
            )
        self.main_frame.place(x=0, y=20)
        text = 'Your score: %d' % self.score
        score_lbl = tk.Label(self.root, text=text)
        # TODO place it in right position
        score_lbl.place(x=0, y=0)
        #score_lbl.pack()
        return

    def init_gui(self):
        '''Initializing GUI. Creating root gui, setting gui size,
        creating menubar'''
        self.root = tk.Tk()

        self.root.minsize(
            self.config['gui']['min_w'],
            self.config['gui']['min_h']
            )
        self.root.maxsize(
            self.config['gui']['max_h'],
            self.config['gui']['max_w']
            )

        self.init_main_frame()

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

    def guess_word_translation(self):
        '''You're given word-translation and you need to guess to what
        word from 2 given words it benongs'''
        self.init_main_frame()
        self.read_words(limit=self.config['app']['items'])

        self.root.title('Guess word translation')
        frame = tk.Frame(self.main_frame,
                         width=1000,
                         height=700,
                         bd=5,
                         relief=tk.RIDGE,
                         )
        frame.place(x=200, y=100)
        word_lbl = tk.Label(frame,
                            font=self.config['gui']['font_size'],
                            text='Press enter to start',
                            width=20,
                            wraplength=150,
                            justify=tk.CENTER
                            )
        result_lbl = tk.Label(frame,
                              text='',
                              font=self.config['gui']['font_size'],
                              )
        left_lbl = tk.Label(frame,
                            text='',
                            font=self.config['gui']['font_size'],
                            width=20,
                            wraplength=150,
                            )
        right_lbl = tk.Label(frame,
                             text='',
                             font=self.config['gui']['font_size'],
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
            self.tmp_result = 0
            self.result[1] = int(self.config['app']['items'])
            # current word position in the words list
            self.pos = 0
            fill_lbl()

        def check_answer(answer):
            '''checks given answer'''
            word = self.words[self.pos]
            if answer == word[0]:
                result_lbl.config(text='Right!')
                result_lbl.config(bg=self.config['colors']['right'])
                self.tmp_result += 1
            else:
                result_lbl.config(text='Wrong!')
                result_lbl.config(bg=self.config['colors']['wrong'])

            self.pos += 1
            if self.pos >= int(self.config['app']['items']):
                # send result to main gui
                self.show_result(frame)
                return
            fill_lbl()

        frame.bind('<Return>', lambda e: init())
        word_lbl.grid(row=0, column=1)
        result_lbl.grid(row=1, column=1)
        frame.focus()
        return

    def spell_word(self):
        '''You're given a word translation. You need to spell word from
        memory'''
        self.init_main_frame()
        self.read_words(limit=self.config['app']['items'])
        self.root.title('Spell words')
        self.pos = 0
        self.tmp_result = 0
        self.result[1] = int(self.config['app']['items'])
        frame = tk.Frame(self.main_frame,
                         width=self.config['gui']['min_w'],
                         height=self.config['gui']['min_h'],
                         bd=5,
                         relief=tk.RIDGE,
                         )
        frame.place(x=200, y=100)
        # label with result
        result_lbl = tk.Label(frame,
                              font=self.config['gui']['font_size'],
                              text='Write your answer below!')
        result_lbl.pack()
        answer_ent = tk.Entry(frame,
                              font=self.config['gui']['font_size'],
                              width=50,
                              justify=tk.CENTER)
        answer_ent.focus()
        answer_ent.pack()

        def check_answer():
            '''Answer checking'''
            answer = answer_ent.get()
            answer_ent.delete(0, 'end')

            if answer == self.words[self.pos][0]:
                result_lbl.config(text='Right!')
                result_lbl.config(bg=self.config['colors']['right'])
                self.tmp_result += 1
            else:
                tmp_msg = 'Right answer: ' + self.words[self.pos][0]
                result_lbl.config(text=tmp_msg)
                result_lbl.config(bg=self.config['colors']['wrong'])

            self.pos += 1
            if self.pos >= int(self.config['app']['items']):
                # send result to main gui
                self.show_result(frame)
                return
            word_lbl.config(text=self.words[self.pos][1])

        word_lbl = tk.Label(frame,
                            font=self.config['gui']['font_size'],
                            text=self.words[self.pos][1],
                            wraplength=350)
        word_lbl.pack()
        answer_ent.bind('<Return>', lambda e: check_answer())
        answer_btn = tk.Button(frame,
                               text='Answer',
                               width=10,
                               command=check_answer)
        answer_btn.pack()
        return

    def word_translation(self, display=0):
        # TODO add informative docstring
        self.init_main_frame()
        self.read_words(limit=self.config['app']['items'])
        self.pos = 0
        self.tmp_result = 0

        if display == 0:
            word_guess = 1
            gui_title = 'Translation-word'
        else:
            word_guess = 0
            gui_title = 'Word-translation'

        self.root.title(gui_title)

        frame = tk.Frame(self.main_frame,
                         width=700,
                         height=400,
                         bd=5,
                         relief=tk.RIDGE,
                         )
        frame.place(x=0, y=0)

        word_lbl = tk.Label(frame,
                            font=self.config['gui']['font_size'],
                            text='Press enter to start',
                            width=20,
                            wraplength=150,
                            justify=tk.CENTER
                            )
        result_lbl = tk.Label(frame,
                              font=self.config['gui']['font_size'])
        str_lbls = [tk.StringVar() for _ in range(4)]

        # labels with answers
        lbls = [tk.Label(
            frame,
            textvariable=str_lbls[i],
            font=self.config['gui']['font_size']) for i in range(4)]

        def fill_lbl():
            word = self.words[self.pos]
            word_lbl.configure(text=word[display])
            guesses = self.get_random_items(self.words, 4, self.pos)
            for i in range(4):
                str_lbls[i].set(guesses[i][word_guess])

        def init():
            frame.bind('<Return>', lambda e: 1)
            for i in range(4):
                tmp_f = lambda e, i=i: check_answer(i)
                lbls[i].bind('<Button-1>', tmp_f)
                frame.bind(str(i + 1), tmp_f)
            self.result[1] = int(self.config['app']['items'])
            self.pos = 0
            fill_lbl()

        def check_answer(lbl_id):
            if str_lbls[lbl_id].get() == self.words[self.pos][word_guess]:
                result_lbl.config(text='Right!')
                result_lbl.config(bg=self.config['colors']['right'])
                self.tmp_result += 1
            else:
                msg = str_lbls[lbl_id].get()
                msg += ' not ' + self.words[self.pos][word_guess]
                result_lbl.config(bg=self.config['colors']['wrong'])
                result_lbl.config(text=msg)

            self.pos += 1
            if self.pos >= int(self.config['app']['items']):
                # send result to main gui
                self.show_result(frame)
                return
            fill_lbl()

        frame.bind('<Return>', lambda e: init())
        word_lbl.grid(row=0, column=0)
        result_lbl.grid(row=1, column=0)
        for i in range(4):
            lbls[i].grid(row=i, column=1)
        frame.focus()
        return

    def crossword(self):
        # h - horizontal, v - vertical
        self.move = 'h'
        self.tmp_result = 0

        class crossword_cell(tk.Entry):
            '''custom class from tk.Entry that contains additional
            variable for checking default value of a cell'''
            def __init__(self, *args, def_char, **kwargs):
                self.def_char = def_char
                super(crossword_cell, self).__init__(*args, **kwargs)

        def create_cell(row, column, char):
            field[row][column] = crossword_cell(
                frame,
                width=2,
                justify=tk.CENTER,
                font=self.config['gui']['font_size'],
                bg=self.config['colors']['bg_darker'],
                def_char=char
                )
            field[row][column].grid(row=row, column=column)
            field[row][column].bind('<Key>',
                                    lambda e: check_key(e, row, column))
            field[row][column].bind('<Button>',
                                    lambda e: check_key(e, row, column))
            return

        def fill_field(word, row, column, direction):
            if direction == 'h':
                for i in range(len(word)):
                    create_cell(row, column + i, word[i])
            elif direction == 'v':
                for i in range(len(word)):
                    create_cell(row + i, column, word[i])
            else:
                raise TypeError('Wrong axis argument! Must be "h" or "v"!')
            return

        def activate_cell(row, column, direction):
            self.move = direction
            field[row][column].focus()

        def check_key(e, row, column, direction=None):
            key_char = e.char.lower()

            # is it character key was pressed?
            if len(key_char) == 1:
                if key_char == ' ':
                    field[row][column].delete(0, 'end')
                elif ord('a') <= ord(key_char) <= ord('z'):
                    field[row][column].delete(0, 'end')

                    # move vertical
                    if self.move == 'v':
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
                    self.move = 'h'
            elif e.keysym == 'Right':
                if field[row][column + 1]:
                    field[row][column + 1].focus()
                    self.move = 'h'
            elif e.keysym == 'Up':
                if field[row - 1][column]:
                    field[row - 1][column].focus()
                    self.move = 'v'
            elif e.keysym == 'Down':
                if field[row + 1][column]:
                    field[row + 1][column].focus()
                    self.move = 'v'
            elif e.keysym == 'BackSpace':
                # clear current cell
                if field[row][column]:
                    field[row][column].delete(0, 'end')

                # moving to previous cell
                if self.move == 'v':
                    if field[row - 1][column]:
                        field[row - 1][column].focus()
                else:
                    if field[row][column - 1]:
                        field[row][column - 1].focus()
            # mouse click
            elif e.num == 1:
#TODO highlight word translation
# I need to find to what word relate current cell
# but how?
                if field[row + 1][column] or field[row - 1][column]:
                    self.move = 'v'
                else:
                    self.move = 'h'
            return

        def check_crossword():
            for row in field:
                for cell in row:
                    if not cell:
                        # not a cell, skip it
                        continue
                    answer = cell.get()
                    if cell.def_char == answer:
                        cell.configure(bg=self.config['colors']['right'])
                    elif answer != '':
                        cell.configure(bg=self.config['colors']['wrong'])
            return

        def reset_cells_bg():
            for row in field:
                for cell in row:
                    if cell:
                        cell.configure(bg=self.config['colors']['bg_darker'])
            return

        #TODO add functionality
        def check_answer():
            # remove global vars that was used in this function

            right_answers = 0

            for word in crossword_items:
                row, column, pos = crossword_items[word]
                len_word = len(word)
                if pos == 'v':
                    add_r = 1
                    add_c = 0
                else:
                    add_r = 0
                    add_c = 1

                right = True

                for i in range(len_word):
                    cell = field[row + (add_r * i)][column + (add_c * i)]
                    answer = cell.get()
                    if not cell.def_char == answer:
                        right = False
                        break

                if right:
                    right_answers += 1
            print(right_answers)
# TODO remove this frame, write answers to db
            return

        self.init_main_frame()
        self.read_words(limit=self.config['app']['items'])
        frame = tk.Frame(
            self.main_frame,
            width=1000,
            height=700,
            bg=self.config['colors']['bg']
            )

        #TODO SET PROPER SIZE
        frame.place(x=180, y=0)
        # forbid Control+Key combinations
        frame.bind('<Control_L><Key>', lambda e: 1)

        words = []
        for word in self.words:
            if re.match('^[a-z]+$', word[0]):
                words.append(word[0])

        mc = Crossword(words, size_r=30, size_c=30)
        crossword_items = mc.generate_crossword()

        # show translations labels
        transl_frm = tk.Frame(self.main_frame, bg=self.config['colors']['bg'])
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
            # focus on the first cell of the word
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

    def show_result(self, frame):
        # destroing frame with app elements
        frame.destroy()
        self.result[0] += self.tmp_result
        self.result[1] = int(self.config['app']['items'])
        self.init_main_frame()
        self.root.title('Result')
        self.update_score(*self.result)
        msg = str(self.tmp_result) + ' from ' + str(self.result[1])
        tk.Label(self.main_frame, text=msg).pack()
        return

    def show_help(self):
        # TODO add more info
        help_gui = tk.Toplevel()
        help_msg = 'Use arrow keys to answer in "Guess word"\n'
        help_msg += 'Use enter to answer in "Spell word"\n'
        help_msg += 'Use Control+q to quit the programm.\n'
        tk.Label(help_gui, text=help_msg).pack()
        help_gui.bind('<Control-q>', lambda e: help_gui.destroy())
        help_gui.bind('<Control-Q>', lambda e: help_gui.destroy())
        return

    def show_about(self):
        # TODO add more info
        about_gui = tk.Toplevel()
        tk.Label(about_gui, text='This program is in developmnet').pack()
        about_gui.bind('<Control-q>', lambda e: about_gui.destroy())
        about_gui.bind('<Control-Q>', lambda e: about_gui.destroy())
        return


def main():
    lw = LearnWords()
    lw.init_gui()
    # closing db connection
    lw.db_connect.close()


if __name__ == '__main__':
    main()

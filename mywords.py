#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import os.path
import random
#from urllib.request import urlopen
import sqlite3
from bs4 import BeautifulSoup


class EnWords():
    # working directory
    wdir = os.path.dirname(os.path.realpath(__file__))

    # file with words as json
    words_file = os.path.join(wdir, 'tmp', 'engwords.txt')

    def __init__(self, db_name):
        self.db_name = db_name

    def parse_words_from_ll(self, name=False):
        '''parse words from lingualeo dictionary page, write them as json.
        To get these words visit
        http://lingualeo.com/ru/glossary/learn/dictionary
        select words what you wish to learn and press print icon and you will
        be redirected to another page with words save that page by pressing
        Ctrl+S with default name in the folder with script.
        If you have saved page with another name, pass that name to
        parse_words_from_ll()'''

        # default page name
        pn = 'LinguaLeo vocabulary printing | English language online.html'
        if name:
            pn = name

        try:
            with open(os.path.join(self.wdir, pn), 'r') as f:
                page = f.read()
        except IOError as e:
            print('Error! {}'.format(e))
            return None

        s = BeautifulSoup(page)
        cells = s.find_all('tr')
        words = []

        for cell in cells:
            reg = '<td><b>(.*)</b>.*<td class="transcr">(.*)</td>.*'
            reg += '<td class="tran">(.*)</td>'
            m = re.compile(reg, re.DOTALL)
            rword = m.search(str(cell))
            word = [x.strip() for x in rword.groups()]
            tmp_dict = {'word': word[0],
                        'transcription': word[1],
                        'translation': word[2],
                        }
            words.append(tmp_dict)

        with open(self.words_file, 'w') as f:
            f.write(json.dumps(words, ensure_ascii=False))
        return True

    def parse_words_from_lltxt(self, name='words.txt'):
        try:
            with open(os.path.join(self.wdir, name),
                      'r', encoding='utf-8') as f:
                raw_words = f.readlines()
        except IOError as e:
            print('Error! {}'.format(e))
            return None

        start = 0
        for line in raw_words:
            if line[0] != '1':
                start += 1
            else:
                break

        end = 0
        n = len(raw_words) - 1

        while n:
            if re.match('^\d', raw_words[n]):
                end = n
                break
            n -= 1

        words = []
        for line in raw_words[start:end]:
            word = [x.strip() for x in line.split('\t')]
            tmp_dict = {'word': word[1],
                        'transcription': word[2],
                        'translation': word[3],
                        }
            words.append(tmp_dict)

        with open(self.words_file, 'w') as f:
            f.write(json.dumps(words, ensure_ascii=False))
        return True

    def read_json_words(self):
        with open(self.words_file, 'r') as f:
            self.json_words = json.load(f)
            return

    def read_words(self, limit=10):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute('''SELECT word, translation FROM 'words'
                  WHERE length(word) < 15
                  ORDER BY RANDOM()
                  LIMIT %d;''' % limit)
        self.words = c.fetchall()
        conn.close()
        return

    def write_words_to_db(self,):
        # is words already loaded to self.json_words
        if not hasattr(self, 'json_words'):
            self.read_json_words()

        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        # is table exists?
        c.execute('''SELECT name FROM sqlite_master
                  WHERE type='table' AND name='words';''')

        if not c.fetchone():
            # Create table
            c.execute('''CREATE TABLE words
                         (id integer primary key,
                         word text,
                         transcription text,
                         translation text);
                         ''')

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        conn.close()
        return
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        for word in self.json_words:
            c.execute('''INSERT INTO words
                      ('word', 'transcription', 'translation')
                      VALUES (?, ?, ?)''',
                      [word['word'],
                       word['transcription'],
                       word['translation'],
                       ]
                      )

        conn.commit()
        conn.close()


class EngTests():
    def __init__(self, words):
        # list of word-translation tuples
        random.shuffle(words)
        self.words = words

    def write_word(self):
        score = 0

        for i in range(10):
            word = self.words[i]
            print(word[1])
            guess_word = input('')

            if guess_word.lower() == word[0].lower():
                print("Hooray! You are right!")
                score += 1
            else:
                print("Damn! You are wrong! Right answer is '%s'!" % word[0])
            print(score)
        print('You have %d from %d points!' % (score, 10))


def main():
    my_words = EnWords(db_name='engwords.db')
    #my_words.parse_words_from_ll()
    #my_words.parse_words_from_lltxt()
    #my_words.read_words()
    my_words.write_words_to_db()
    #my_test = EngTests(my_words.words)
    #my_test.write_word()
    return


if __name__ == "__main__":
    main()


#def create_directory(path, remove_file=True):
    #'''Creates directory. If path is a file and remove_file=True
    #than function will remove file and create a directory'''
    #if not os.path.isdir(path):
        #try:
            #os.mkdir(path)
        #except:
            #if remove_file:
                #path = path.rstrip('/')
                #os.remove(path)
                #os.mkdir(path)
    #return

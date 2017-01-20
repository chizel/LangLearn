#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import subprocess


def playaudio(word, library, ext='.wav', platform='linux'):
    word = word.lower()
    words = word.split()
    files = []

    for w in words:
        tmp = os.path.join(library, w[0], w + ext)
        if not os.path.exists(tmp):
            print('nope ', tmp)
            return
        files.append(tmp)
    params = ['play', '-q']
    params.extend(files)

    if platform == 'linux':
        play = subprocess.Popen(params)
    elif platform == 'windows':
        try:
            import winsound
            winsound.PlaySound('%s.wav' % audiofiles, winsound.SND_FILENAME)
        except:
            raise('Error! Can\'t import windsound.')
    else:
        raise("Error! Platform isn't supported! Your platform is %s" % platform)


def main():
    # test
    platform = 'linux'
    sound_library = '/home/a/other/GoldenDict_Dicts/en_snd/'
    word = 'axis'
    playaudio(word, sound_library, platform)


if __name__ == "__main__":
    main()

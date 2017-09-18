# -*- coding: utf-8 -*-
import csv
import re
import os

music_filename = 'music.dic'

delimiter = '、|；|（|）|｛|｝|\(|\)|－'

if not os.path.exists(os.path.dirname('assets/dictionary/{0}'.format(music_filename))):
    try:
        os.makedirs(os.path.dirname('assets/dictionary/{0}'.format(music_filename)))
    except:
        raise

with open('assets/dictionary/music.csv') as s:
    read_data = csv.reader(s)
    with open('assets/dictionary/{0}'.format(music_filename), 'a') as d:
        for row in read_data:
            music_split = re.split(delimiter, row[1])
            for word in music_split:
                if word:
                    d.write('{0}\n'.format(word))



# -*- coding: utf-8 -*-
import json
import re
import os

custom_word_pattern = r'\{\[\S{4}\]\}'
stopword_pattern = r'，'
english_pattern = r'\('
mydict_filename = 'mydict.dic'

if not os.path.exists(os.path.dirname('assets/dictionary/{0}'.format(mydict_filename))):
    try:
        os.makedirs(os.path.dirname('assets/dictionary/{0}'.format(mydict_filename)))
    except:
        raise

with open('assets/dictionary/dict-revised.json') as s:
    read_data = s.read()
    s.close()
    dict_json = json.loads(read_data)
    with open('assets/dictionary/{0}'.format(mydict_filename), 'a') as d:
        for word in dict_json:
            my_word = word['title']

            if re.search(custom_word_pattern, my_word) is None:

                # with English name
                if re.search(english_pattern, my_word) is not None:
                    en_idx = my_word.index('(') 
                    my_word = my_word[:en_idx]
                    d.write('{0}\n'.format(my_word))
                    continue

                # with stopword
                if re.search(stopword_pattern, my_word) is not None:
                    word_arr = my_word.split(stopword_pattern)
                    for word in word_arr:
                        d.write('{0}\n'.format(word))
                    continue    

                d.write('{0}\n'.format(my_word))


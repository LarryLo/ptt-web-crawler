# -*- coding: utf-8 -*-
import re
import os
import mafan

stopword_filename = 'ext_stopword.dic'

if not os.path.exists(os.path.dirname('assets/dictionary/{0}'.format(stopword_filename))):
    try:
        os.makedirs(os.path.dirname('assets/dictionary/{0}'.format(stopword_filename)))
    except:
        raise

with open('assets/dictionary/ext_stopword.txt') as s:
    with open('assets/dictionary/{0}'.format(stopword_filename), 'a') as d:
        for line in s:
           d.write('{0}'.format(line))
           if not mafan.text.has_punctuation(line):
               d.write('{0}'.format(mafan.tradify(line)))

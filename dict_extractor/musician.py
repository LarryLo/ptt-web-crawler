# -*- coding: utf-8 -*-
import csv
import re
import os

musician_filename = 'musician.dic'

delimiter = '－|-|,|‧|\(|\)'

if not os.path.exists(os.path.dirname('assets/dictionary/{0}'.format(musician_filename))):
    try:
        os.makedirs(os.path.dirname('assets/dictionary/{0}'.format(musician_filename)))
    except:
        raise

with open('assets/dictionary/musician.csv') as s:
    read_data = csv.reader(s)
    with open('assets/dictionary/{0}'.format(musician_filename), 'a') as d:
        for row in read_data:
            musician_split = re.split(delimiter, row[1])
            for word in musician_split:
                d.write('{0}\n'.format(word))


# -*- coding: utf-8 -*-
import os
import configparser

config = configparser.ConfigParser()
config.read('etc/config.ini')

for board in eval(config['ptt']['ptt.board.list']):
    board = board.lower()
    if not os.path.exists('tmp/{0}'.format(board)):
        try:
            os.makedirs('tmp/{0}'.format(board))
        except:
            raise

class FileWrapper:
    '''
    A very simple file io wrapper to store tmp html files
    '''
    @staticmethod
    def store(board, article_id, article):
        board = board.lower()
        with open('tmp/{0}/{1}'.format(board, article_id), 'w') as f:
            f.write(article)
            f.close


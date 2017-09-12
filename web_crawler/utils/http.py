# -*- coding: utf-8 -*-
import configparser
import urllib.request
from urllib.request import Request

config = configparser.ConfigParser()
config.read('etc/config.ini')

class PttWrapper:
    """
    A urllib wrapper to send request to ptt
    """
    def __init__(self):
        self.protocol = config['ptt']['ptt.protocol']
        self.url_prefix = config['ptt']['ptt.url.prefix']
        self.headers = {
            'Content-type': 'Accept text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'ptt-rocks',
            'Cookie': 'over18=1', }

        # oldest index: 1
        # newest index: '' (blank)
    def get_article_list(self, board, index):
        req = Request(
            "{0}://{1}/{2}/index{3}.html".format(
                self.protocol, 
                self.url_prefix, 
                board, 
                index), 
            method='GET',
            headers=self.headers)
        with urllib.request.urlopen(req) as rsp:
            return rsp.read()

    def get_article(self, board, article_id):    
        req = Request(
            "{0}://{1}/{2}/{3}.html".format(
                self.protocol, 
                self.url_prefix, 
                board, 
                article_id), 
            method='GET',
            headers=self.headers)
        with urllib.request.urlopen(req) as rsp:
            return rsp.read()
        

# -*- coding: utf-8 -*-
import logging
import configparser
import urllib3

config = configparser.ConfigParser()
config.read('etc/config.ini')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=config['log']['log.file'],
                    filemode='w')
logger = logging.getLogger(__file__)

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
        http = urllib3.PoolManager()
        try:
            req = http.request(
                    'GET',
                    '{0}://{1}/{2}/index{3}.html'.format(
                        self.protocol, 
                        self.url_prefix, 
                        board, 
                        index), 
                    headers=self.headers)
            return req.data
        except Exception as e:    
            logger.error(str(e))
            return ''

    def get_article(self, board, article_id):    
        http = urllib3.PoolManager()
        try:
            req = http.request(
                    'GET',
                    '{0}://{1}/{2}/{3}.html'.format(
                        self.protocol, 
                        self.url_prefix, 
                        board, 
                        article_id), 
                    headers=self.headers)
            return req.data
        except Exception as e:    
            logger.error(str(e))
            return ''


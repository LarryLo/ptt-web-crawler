# -*- coding: utf-8 -*-
import configparser
import time
import logging
from utils.http import PttWrapper
from utils.elasticsearch import ElasticsearchWrapper
from utils.parser import PttHtmlParser
from utils.file import FileWrapper 
from utils.gcp import GCPWrapper

config = configparser.ConfigParser()
config.read('etc/config.ini')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=config['log']['log.file'],
                    filemode='w')
logger = logging.getLogger(__file__)

def main():
    ptt_wrapper = PttWrapper()
    es = ElasticsearchWrapper()
    gcp = GCPWrapper()

    for board in eval(config['ptt']['ptt.board.list']):
        # Get article list by board index page
        article_list_html = ptt_wrapper.get_article_list(board, '')
        article_page_count = int(PttHtmlParser.count_article_list(board, article_list_html))
        articles = []

        for idx in range(1, article_page_count):
            # Collect ptt articles as document type to index into elasticsearch
            ## Get article list by index
            article_list_html = ptt_wrapper.get_article_list(board, idx)
            ## Get each article id by article_list_html
            article_id_list = PttHtmlParser.parse_article_list(board, article_list_html)

            start_time = time.time()
            per_page_articles = [handle_article(ptt_wrapper, gcp, board, article_id) for article_id in article_id_list]
            articles.extend(per_page_articles)
            logger.info('Round {0}/{1}: {2} seconds'.format(idx, article_page_count, time.time() - start_time))

            if idx == article_page_count:
                # Index latest page
                es.bulk_index_article(articles)
            elif idx % int(config['elasticsearch']['es.index.period']) == 0:
                start_time = time.time()
                es.bulk_index_article(articles)
                logger.info('Index {0}/{1}: {2} seconds'.format(idx, article_page_count, time.time() - start_time))
                del articles[:]

def handle_article(ptt_wrapper, gcp, board, article_id):
    article_html = str(ptt_wrapper.get_article(board, article_id), 'utf-8')
    if article_html:
        article = PttHtmlParser.parse_article(article_id, article_html)
        FileWrapper.store(board, article_id, article_html)
        ## Upload file to gcp storage
        ### Not thread safe
        gcp.upload(board, article_id)
        return article

if __name__ == '__main__':
    main()

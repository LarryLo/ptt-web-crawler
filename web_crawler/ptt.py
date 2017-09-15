# -*- coding: utf-8 -*-
import configparser
import time
import logging
from utils.http import PttWrapper
from utils.elasticsearch import ElasticsearchWrapper
from utils.parser import PttHtmlParser
from utils.file import FileWrapper 

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='/tmp/ptt-crawler.log',
                    filemode='w')
logger = logging.getLogger(__file__)

config = configparser.ConfigParser()
config.read('etc/config.ini')

def main():
    ptt_wrapper = PttWrapper()
    es = ElasticsearchWrapper()

    for board in eval(config['ptt']['ptt.board.list']):
        # Get article list by board index page
        article_list_html = ptt_wrapper.get_article_list(board, '')
        article_page_count = int(PttHtmlParser.count_article_list(board, article_list_html))
        articles = []

        for idx in range(1, article_page_count):
            # Collection of documents to batch index
            # Get each article list by index
            article_list_html = ptt_wrapper.get_article_list(board, idx)
            # Get each article id by article_list_html
            article_id_list = PttHtmlParser.parse_article_list(board, article_list_html)

            start_time = time.time()
            for article_id in article_id_list:
                # Get each article html by article_id
                article_html = ptt_wrapper.get_article(board, article_id)
                article_html = str(article_html, 'utf-8')
                if article_html:
                    article = PttHtmlParser.parse_article(article_id, article_html)
                    articles.append(article)
                # Store article to tmp folder
                FileWrapper.store(board, article_id, article_html)    
                    
            logger.info('Round {0}/{1}: {2} seconds'.format(idx, article_page_count, time.time() - start_time))

            if idx == article_page_count:
                # Index latest page
                es.bulk_index_article(articles)
            elif idx % 20 == 0:
                start_time = time.time()
                es.bulk_index_article(articles)
                logger.info('Index {0}/{1}: {2} seconds'.format(idx, article_page_count, time.time() - start_time))
                del articles[:]

if __name__ == '__main__':
    main()

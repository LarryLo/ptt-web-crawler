# -*- coding: utf-8 -*-
import configparser
import time
from utils.http import PttWrapper
from utils.elasticsearch import ElasticsearchWrapper
from utils.parser import PttHtmlParser

config = configparser.ConfigParser()
config.read('etc/config.ini')

def main():
    ptt_wrapper = PttWrapper()
    
    es = ElasticsearchWrapper()
    for board in eval(config['ptt']['ptt.board.list']):
        # Get article list by board index page
        article_list_html = ptt_wrapper.get_article_list(board, '')
        article_page_count = int(PttHtmlParser.count_article_list(board, article_list_html))
        for idx in range(1, article_page_count):
            # Collection of documents to batch index
            articles = []
            # Get each article list by index
            article_list_html = ptt_wrapper.get_article_list(board, idx)
            # Get each article id by article_list_html
            article_id_list = PttHtmlParser.parse_article_list(board, article_list_html)
            for article_id in article_id_list:
                # Get each article html by article_id
                article_html = ptt_wrapper.get_article(board, article_id)
                article = PttHtmlParser.parse_article(article_id, article_html)
                articles.append(article)

            # Index articles every page
            es.bulk_index_article(articles)


if __name__ == '__main__':
    main()

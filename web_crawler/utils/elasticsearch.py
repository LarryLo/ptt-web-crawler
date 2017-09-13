# -*- coding: utf-8 -*-
import json
import configparser
from elasticsearch import Elasticsearch 
from elasticsearch import helpers

config = configparser.ConfigParser()
config.read('etc/config.ini')

class ElasticsearchWrapper:
    """
    An elasticsearch wrapper implemented by singleton
    """
    __single = None
    def __new__(clz):
        if not ElasticsearchWrapper.__single:
            ElasticsearchWrapper.__single = object.__new__(clz)
        return ElasticsearchWrapper.__single    

    def __init__(self):
        self.index_article = 'ptt_article'
        self.index_comment = 'ptt_comment'
        if 'elasticsearch' not in config:
            print('Not found [elasticsearch] section in settins, we\'ll use localhost:9200 as default.')
            self.conn = Elasticsearch()
        else:
            if config['elasticsearch']['es.url']:
                self.conn = Elasticsearch(eval(config['elasticsearch']['es.url']))
            else:
                self.conn = Elasticsearch()
        self.conn.indices.create(index=self.index_article, ignore=400, body=self.get_article_mapping())
        self.conn.indices.create(index=self.index_comment, ignore=400)

    def get_article_mapping(self):
        mapping = {
        'mappings': {
            self.index_article: {
                'properties': {
                    'board': {
                        'type': 'keyword',
                        },    
                    'article_id': {
                        'type': 'keyword',
                        },    
                    'author': {
                        'type': 'keyword',
                        },    
                    'title': {
                        'type': 'text',
                        },    
                    'content': {
                        'type': 'text',
                        },    
                    'site_name': {
                        'type': 'keyword',
                        },    
                    'created_datetime': {
                        'type': 'keyword',
                        },    
                    'ip': {
                        'type': 'keyword',
                        },    
                    'article_url': {
                        'type': 'keyword',
                        },    
                    'like': {
                        'type': 'nested',
                        'properties': {
                            'user_id': 'keyword',
                            'tag': 'keyword',
                            'content': 'keyword',
                            'datetime': 'keyword',
                            }
                        },    
                    'dislike': {
                        'type': 'nested',
                        'properties': {
                            'user_id': 'keyword',
                            'tag': 'keyword',
                            'content': 'keyword',
                            'datetime': 'keyword',
                            }
                        },    
                    'arrow': {
                        'type': 'nested',
                        'properties': {
                            'user_id': 'keyword',
                            'tag': 'keyword',
                            'content': 'keyword',
                            'datetime': 'keyword',
                            }
                        },    
                    }    
                }
            }
        }
        return json.dumps(mapping) 

    def bulk_index_article(self, articles):
        actions = [
            {
                '_op_type': 'index',
                '_index': self.index_article,
                '_type': self.index_article,
                '_id': article.article_id,
                '_source': {
                    'board': article.board,
                    'article_id': article.article_id,
                    'author': article.author,
                    'title': article.title,
                    'content': article.content,
                    'site_name': article.site_name,
                    'created_datetime': article.created_datetime,
                    'ip': article.ip,
                    'article_url': article.article_url,
                    'like': [ like.__dict__ for like in article.like ],
                    'dislike': [ dislike.__dict__ for dislike in article.dislike ],
                    'arrow': [ arrow.__dict__ for arrow in article.arrow ]
                }
            }
            for article in articles
        ]

        helpers.bulk(self.conn, actions)


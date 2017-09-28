# -*- coding: utf-8 -*-
import configparser
import re
import time
import logging
from base.article import PttArticle
from base.comment import PttComment
from pyquery import PyQuery as pq

config = configparser.ConfigParser()
config.read('etc/config.ini')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=config['log']['log.file'],
                    filemode='w')
logger = logging.getLogger(__file__)

class PttHtmlParser:
    '''
    A very simple parser to parse html content 
    '''
    @staticmethod
    def count_article_list(board, html):
        a = pq(html)('a').filter('.wide')[1].attrib['href']
        article_page_count = int(re.search(r'\d+', a).group(0)) + 1
        return article_page_count

    @staticmethod
    def parse_article_list(board, html):
        title_list = pq(html)('div .title')
        article_id_list = []
        for title in title_list:
            try:
                url = re.search(r'M.\d+.\d\S+', title.find('a').attrib['href'])
                article_id_list.append(url.group(0)[:-5])
            except Exception as e:
                logger.info('No [{0}] article url.'.format(title))
                logger.error(str(e))

        return article_id_list

    @staticmethod
    def parse_article(article_id, html):
        full_content = pq(html)('#main-content')
        ## metadata
        meta_values = full_content.find('.article-meta-value')
        # board
        board = '' if len(meta_values) != 4 else meta_values[1].text
        # author
        author = '' if len(meta_values) != 4 else meta_values[0].text
        # title
        title = '' if len(meta_values) != 4 else meta_values[2].text
        # datetime
        created_datetime = '' if len(meta_values) != 4 else meta_values[3].text
        ## comments 
        # like
        # dislike
        # arrow
        like = []
        dislike = []
        arrow = []
        comments = full_content.find('.push')
        for comment in comments:
            user_id = pq(comment).find('.push-userid').text()
            push = pq(comment).find('.push-tag').text()
            content = pq(comment).find('.push-content').text()
            ipdatetime = pq(comment).find('.push-ipdatetime').text()
            ptt_comment = PttComment(user_id, push, content, ipdatetime)

            if push == '推':
               like.append(ptt_comment) 
            elif push == '噓':    
               dislike.append(ptt_comment) 
            elif push == '→':  
               arrow.append(ptt_comment) 

        ## main content
        # content
        content = full_content.remove('.push').remove('.article-metaline').remove('article-metaline-right').text()
        ## ptt        
        site_name = pq(html)('#logo').text()
        ## ip
        f2_text = full_content.find('span.f2').text()
        ip_pattern1 = r'來自: \d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}'
        ip_pattern2 = r'From: \d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}'
        ip_re = re.search(ip_pattern1, f2_text)
        ip = ''
        if ip_re is None:
            ip_re = re.search(ip_pattern2, content)
            if ip_re is not None:
                ip = ip_re.group(0)[5:] 
        else:
            ip = ip_re.group(0)[3:]

        ## article_url 
        article_url = '{0}://{1}/{2}/{3}.html'.format(
                    config['ptt']['ptt.protocol'],
                    config['ptt']['ptt.url.prefix'],
                    board,
                    article_id)

        article = PttArticle(
                board, 
                article_id, 
                author,
                title, 
                content, 
                site_name,
                created_datetime,
                ip,
                article_url,
                like,
                dislike,
                arrow)
        return article


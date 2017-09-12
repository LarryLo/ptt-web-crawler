# -*- coding: utf-8 -*-
import configparser
import re
from base.article import PttArticle
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('etc/config.ini')


class PttHtmlParser:
    '''
    A very simple parser to parse html content 
    '''
    @staticmethod
    def count_article_list(board, html):
        soup = BeautifulSoup(html, 'html.parser')
        # parse each field
        paging = soup.find_all('a', class_='wide')
        last_sec_page = paging[1]['href']
        article_page_count = int(re.search(r'\d+', last_sec_page).group(0)) + 1
        return article_page_count

    @staticmethod
    def parse_article_list(board, html):
        soup = BeautifulSoup(html, 'html.parser')
        # parse each field
        title = soup.find_all('div', class_='title')

        article_id_list = []
        for idx in range(len(title)):
            article_id_list.append(re.search(r'M.\d+.\d\S+',title[idx].a['href']).group(0)[:-5])
        return article_id_list


    @staticmethod
    def parse_article(article_id, html):
        soup = BeautifulSoup(html, 'html.parser')
        # parse each field
        main_content = soup.find_all('span')
        # board
        board = main_content[6].string
        # author
        author = main_content[4].string
        # title
        title = soup.find('meta', property='og:title')
        title = '' if title is None else title['content']
        # content
        meta = soup.find_all('div', class_='article-metaline')
        content = ''
        for sibling in meta[2].next_siblings:
            if sibling.string is not None:
                content += sibling.string
        # ptt        
        site_name = soup.find('meta', property='og:site_name')
        site_name = '' if site_name is None else site_name['content']
        # datetime
        created_datetime = main_content[10].string
        
        # ip
        ip_pattern1 = soup.find_all(string=re.compile('批踢踢實業坊\(ptt.cc\), 來自: '))

        ip = ''
        if len(ip_pattern1) != 0:
            ip = re.search(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', ip_pattern1[0])
            ip = ip.group(0) 
        elif len(ip_pattern1) == 0:    
            ip_pattern2 = soup.find_all(string=re.compile('編輯:\s\w+ \(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\)'))
            if len(ip_pattern2) != 0:
              ip = re.search(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', ip_pattern2[0])
              ip = ip.group(0) 

        # article_url 
        article_url = '{0}://{1}/{2}/{3}.html'.format(
                    config['ptt']['ptt.protocol'],
                    config['ptt']['ptt.url.prefix'],
                    board,
                    article_id)
        # like
        like = len(soup.find_all('span', class_='push-tag', string=re.compile('推')))
        # dislike
        dislike = len(soup.find_all('span', class_='push-tag', string=re.compile('噓')))
        # arrow
        arrow = len(soup.find_all('span', class_='push-tag', string=re.compile('→')))

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


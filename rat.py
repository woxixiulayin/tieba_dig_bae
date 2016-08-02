#!/usr/bin/env python
#! coding:utf-8
import urllib2
import json
#from BeautifulSoup import BeautifulSoup
from lxml import etree
import socket
import chardet
# from multiprocessing import Process, Queue, Pool, Manager
import logging
logging.basicConfig(level=logging.INFO)
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

tieba_preurl = "http://tieba.baidu.com/"


class Post(dict):

    def __init__(self, **kw):
        super(Post, self).__init__(**kw)
        self.id = ""
        self.title = ""
        self.author = ""
        self.url_link = ""
        self.rep_num = 0
        self.last_time = ""
        self.body = ''

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError('Post has no this attribute %s' % key)

    def __setter__(self, key, value):
        self[key] = value


def li2post(li):
    li_obj = json.loads(li.get('data-field'))
    post = Post()
    post.id = li_obj['id']
    post.author = li_obj['author_name']
    post.rep_num = int(li_obj['reply_num'])
    post.last_time = li.xpath(
        './/div[1]/div[2]/div[2]/div[2]/span[2]')[0].text.strip()
    link_a = li.xpath('.//div[1]/div[2]/div[1]/div[1]/a')[0]
    post.title = link_a.get('title')
    post.url_link = tieba_preurl + link_a.get('href')
    post.body = li.xpath(
        './/div[1]/div[2]/div[2]/div[1]/div[1]')[0].text
    post.tags = 'tieba'
    return post

def post2dict(post):
    p_dict = {}
    p_dict['id'] = post.id
    p_dict['author'] = post.author
    p_dict['rep_num'] = post.rep_num
    p_dict['last_time'] = post.last_time
    p_dict['title'] = post.title
    p_dict['url_link'] = post.url_link
    p_dict['body'] = post.body
    p_dict['tags'] = 'tieba'
    return p_dict


class My_url():

    def __init__(self, url):
        logging.info('search url: %s' % url)
        self.resp = ''
        self.content = ''
        try:
            self.content = urllib2.urlopen(url, timeout=5).read()
            chartype = chardet.detect(self.content)
            logging.info('html type is %s' % chartype['encoding'])
            self.content = self.content.decode('utf8')
            logging.info(self.content)
        except urllib2.URLError:
            logging.info("Bad URL or timeout")
        except socket.timeout:
            logging.info("socket timeout")
        except StandardError, e:
            print e
        if self.content == '':
            self.content = 'no response'
        self.tree = etree.HTML(self.content)
        # self.save()

    def prettify(self):
        #self.content = BeautifulSoup(self.content).prettify()
        return self.content

    def save(self, filename='my.html'):
        self.prettify()
        with open('my.html', 'wb') as f:
            f.write(self.content)


class Tieba_url(My_url):

    def get_all_li(self):
        self.all_li = self.tree.xpath('//li[@class="j_thread_list clearfix"]')
        if len(self.all_li) == 0:
            self.all_li = self.tree.xpath(
                '//li[@class=" j_thread_list clearfix"]')
        logging.info('get origin lis number is %d' % len(self.all_li))
        return self.all_li

    def get_posts_need(self, author=None, least_reply=10):
        self.posts = []
        self.get_all_li()
        for li in self.all_li:
            post = li2post(li)
            if author != None and len(author) != 0 and post.author != author.decode('utf-8'):
                continue
            if post.rep_num < least_reply:
                continue
            logging.info('['+post.author+'***'+str(post.rep_num)+']')
            self.posts.append(post2dict(post))
        return self.posts


def find_worker(url, author, rep_num, q, lock):
    posts_1_page = Tieba_url(url).get_posts_need(author, rep_num)
    if len(posts_1_page) > 0:
        lock.acquire()
        q.put(posts_1_page)
        lock.release()

class Query(dict):

    def __init__(self, para):
        self.tieba_name = para.get('tieba_name')
        self.deepth = para.get('deepth', 1)
        self.rep_num = para.get('rep_num', 10)
        self.author = para.get('author', None)
        logging.info('''tieba_name is %s,
                        deepth is %s,
                        rep_num is %s,
                        author is %s''' % (self.tieba_name, self.deepth, self.rep_num, self.author ))

    def find(self):
        posts_all_pages = []
        # m = Manager()
        # q = m.Queue()
        # lock = m.Lock()
        # p = Pool()
        # for n in range(self.deepth):
        #     p.apply_async(find_worker, args=("http://tieba.baidu.com/f?kw=" + self.tieba_name + '&pn=' + str(
        #         n * 50), self.author, self.rep_num, q, lock,))
        # p.close()
        # p.join()
        # while not q.empty():
        #     posts_all_pages.extend(q.get(True))
        for n in range(self.deepth):
            posts_all_pages.extend(Tieba_url("http://tieba.baidu.com/f?kw=" + self.tieba_name + '&pn=' + str(
                 n * 50)).get_posts_need(self.author, self.rep_num))

        logging.info('get all needed post')
        return posts_all_pages

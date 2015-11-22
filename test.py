#!/usr/bin/env python
# coding:utf-8
import unittest
from rat import *
import os,sys
import logging
logging.basicConfig(level=logging.INFO)
reload(sys)
sys.setdefaultencoding('utf-8')



class Testcase(unittest.TestCase):

    def test_query_default(self):
        condition = {
            'tieba_name': "戒色",
            'deepth': 5,
            'rep_num': 1000,
            'author': ''
        }
        # self.assertEquals(type(Query(**condition).find()), list)
        logging.info('get_posts_single_theard find number is: %d' % len(Query(condition).get_posts_single_theard()))
        # logging.info('get_posts_gevent find number is: %d' % len(Query(condition).get_posts_gevent()))
        # logging.info('get_posts_mutil_theard find number is: %d' % len(Query(condition).get_posts_mutil_theard()))
        # self.assertTrue(len(Query(**condition).find())>0, True)

if __name__ == '__main__':
    unittest.main()

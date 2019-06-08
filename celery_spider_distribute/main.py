#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2019/6/7 23:49


from celery_spider_distribute.spider import crawl_category_list

if __name__ == '__main__':

    url = 'http://www.xiachufang.com/category/'
    crawl_category_list.delay(url)

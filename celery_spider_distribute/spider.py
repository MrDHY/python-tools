#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2019/6/7 23:23

import re
import requests

from urllib.parse import urljoin
from lxml.html import etree
from celery_spider_distribute import app

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/73.0.3683.86 Safari/537.36',
}


def send_request(url, parmas=None, data=None, headers=None):
    """
    :param url: 请求的url地址
    :param parmas: get请求的查询参数
    :param data: post请求的表单数据
    :param headers: 请求的请求头
    :return:
    """

    if parmas and data:
        print('参数错误')
        return
    elif not parmas and not data:
        response = requests.get(url, headers=headers)
    elif parmas:
        response = requests.get(url, params=parmas, headers=headers)
    elif data:
        response = requests.post(url, data=data, headers=headers)

    else:
        response = requests.get(url)

    if response.status_code == 200:
        return response.text, response.url


baseUrl = 'http://www.xiachufang.com/category/104/'


def extract_first(data_list, default=None):
    """

    :return
    """
    if len(data_list) > 0:
        return data_list[0]
    else:
        return default


# ignore_result=True,忽略结果
@app.task(ignore_result=True)
def crawl_category_list(url):
    """

    :param url: 待下载的url
    :return:
    """
    html, url = send_request(url=url)
    app.send_task("celery_spider_distribute.spider.parse_category_data", args=(html,), queue='crawl_caipu_list',
                  routing_key='crawl_caipu_list')


@app.task
def parse_category_data(html):
    # 解析分类的数据(名称，url地址，id)
    etree_html = etree.HTML(html)
    li_as = etree_html.xpath('//div[@class="cates-list-mini clearfix "]/ul/li/a')
    categorys = []
    for a in li_as:
        info = dict()
        # 标题
        info['title'] = extract_first(a.xpath('./text()'))
        # url地址
        info['url'] = extract_first(a.xpath('./@href'))
        # id
        info['id'] = re.search(r'\d+', info['url']).group()
        # full_url = 'http://www.xiachufang.com' + info['url']
        full_url = urljoin(baseUrl, info['url'])
        # 根据分类url地址，发起请求
        crawl_caipu_list.delay(full_url, info['id'])
        app.send_task("celery_spider_distribute.spider.crawl_caipu_list", args=(full_url, info['id']),
                      queue='crawl_caipu_list',
                      routing_key='crawl_caipu_list')

        categorys.append(info)

    return categorys


@app.task(ignore_result=True)
def crawl_caipu_list(url, categoryId):
    """
    根据分类的url地址，请求获取菜谱列表页面
    :param url:
    :param categoryId:
    :return:
    """
    html, url = send_request(url=url)
    etree_html = etree.HTML(html)
    # 提取菜谱列表数据,获取菜谱详情url地址
    caipu_as = etree_html.xpath('//ul[@class="list"]/li//p[@class="name"]/a')
    for a in caipu_as:
        caipu_url = urljoin(baseUrl, extract_first(a.xpath('./@href')))
        # 根据详情url请求，获取详情数据
        print('菜谱url地址', caipu_url)
        # crawl_caipu_detail.delay(caipu_url, categoryId)
        app.send_task("celery_spider_distribute.spider.crawl_caipu_detail", args=(caipu_url, categoryId),
                      queue='crawl_caipu_detail',
                      routing_key='crawl_caipu_detail')
    # 下一页
    next_url = extract_first(etree_html.xpath('//a[@class="next"]/@href'))
    if next_url:
        next_url = urljoin(baseUrl, next_url)
        # crawl_caipu_list.delay(next_url, categoryId)
        app.send_task("celery_spider_distribute.spider.crawl_caipu_list", args=(next_url, categoryId),
                      queue='crawl_caipu_list',
                      routing_key='crawl_caipu_list')


@app.task
def crawl_caipu_detail(url, categoryId):
    html, url = send_request(url=url)
    # 解析菜谱详情数据
    etree_html = etree.HTML(html)
    detail = dict()
    # 标题
    detail['title'] = extract_first(etree_html.xpath('//h1[@class="page-title"]/text()'), '')
    # categoryId
    detail['categoryId'] = categoryId
    return detail

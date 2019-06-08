#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2019/6/7 23:24

import os
from celery import platforms
from kombu import Exchange, Queue

# 主要用于启动定时任务
# from datetime import timedelta
# from celery.schedules import crontab

BASE_LOG = os.path.dirname(os.path.dirname(__file__)) + '/logs'
worker_log_path = os.path.join(BASE_LOG, 'celery.logs')
beat_log_path = os.path.join(BASE_LOG, 'beat.logs')
platforms.C_FORCE_ROOT = True

os.makedirs(BASE_LOG, exist_ok=True)

# broker的配置
BROKER_URL = "redis://:Mindata123@127.0.0.1:21601/1"
CELERY_RESULT_BACKEND = "redis://:Mindata123@127.0.0.1:21601/2"
CELERY_TASK_RESULT_EXPIRES = 1000
CELERY_TIMEZONE = 'Asia/Shanghai'

# 指定任务的序列化
CELERY_TASK_SERIALIZER = 'json'

# 指定执行结果的序列化
CELERY_RESULT_SERIALIZER = 'json'

# 指定日志文件
# CELERYD_LOG_FILE = worker_log_path
# CELERYBEAT_LOG_FILE = beat_log_path

# 指定队列和对应的路由
CELERY_QUEUES = (
    Queue(
        'default',
        exchange=Exchange('default'),
        routing_key='default'
    ),
    Queue(
        'crawl_caipu_list',
        exchange=Exchange('crawl_caipu_list'),
        routing_key='crawl_caipu_list',
    ),
    Queue(
        'crawl_caipu_detail',
        exchange=Exchange('crawl_caipu_detail'),
        routing_key='crawl_caipu_detail'
    )
)

# 根据路由指定对应的函数模块和队列
CELERY_ROUTES = {
    'celery_spider_distribute.spider.crawl_caipu_list': {
        'queue': 'crawl_caipu_list',
        'routing_key': 'crawl_caipu_list',
    },
    'celery_spider_distribute.spider.crawl_caipu_detail': {
        'queue': 'crawl_caipu_detail',
        'routing_key': 'crawl_caipu_detail',
    },
    'celery_spider_distribute.spider.crawl_category_list': {
        'queue': 'crawl_caipu_list',
        'routing_key': 'crawl_caipu_list',
    }

}

# 降低爬取频率
CELERY_ANNOTATIONS = {'*': {'rate_limit': '1/s'}}

# 定时任务可以参照这个
# 启动命令: celery beats -A + 项目名 + -l info
# CELERYBEAT_SCHEDULE = {
#     'task1': {
#         'task': 'celery_demo.task1.add',
#         'schedule': timedelta(seconds=10),  # 表示每10秒发送一次任务消息
#         'args': (10, 20)
#     },
#     'task2': {
#         'task': 'celery_demo.task2.mut',
#         'schedule': crontab(hour=22, minute=24),  # 表示在每天的晚上10点24分发送一次任务消息
#         'args': (10, 10)
#     }
# }

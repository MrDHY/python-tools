#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2019/6/7 23:21

from celery import Celery
app = Celery(
    "write_pro_doc",
    include=[
        'celery_spider_distribute.spider',
    ]
)

# 加载配置
app.config_from_object(
    'celery_spider_distribute.celery_config'
)

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2019/6/8 15:28

import threading


def do_something(task):
    print(task)


def get_task(config):
    return config.task


class MyThread(object):
    def __init__(self, gain_config):
        self.gain_config = gain_config
        self.threads = []

    # 处理线程 读取任务
    @staticmethod
    def deal(task):
        do_something(task)

    # 主线程
    def run(self):
        task = get_task(self.gain_config)
        thd = threading.Thread(target=self.deal, args=(task,))
        thd.setDaemon(True)
        thd.start()
        self.threads.append(thd)

    def join(self):
        for t in self.threads:
            t.join()

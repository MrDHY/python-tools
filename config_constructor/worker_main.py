#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2019/6/8 15:20

import os
import argparse

import logging
import logging.config

from config_constructor.config import Myconfig
from config_constructor.worker_thread import MyThread


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='配置文件', default='conf/worker.conf')
    parser.add_argument('--logging', help='日志配置', default='conf/logging.conf')
    args = parser.parse_args()

    # 配置日志
    if args.logging:
        os.makedirs('log', exist_ok=True)
        logging.config.fileConfig(args.logging)

    config = Myconfig(args.config)
    abu_thread = MyThread(config)
    abu_thread.run()
    abu_thread.join()
    logging.info('thread exit.')


if __name__ == '__main__':
    main()
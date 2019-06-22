#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2019/6/19 22:30


def run(host, port):
    """
    run server on given host:port

    :type host: str
    :param host: server host
    :type port: int
    :param port: server port

    :return app

    """
    print('running on :{}:{}'.format(host, port))
    return 0
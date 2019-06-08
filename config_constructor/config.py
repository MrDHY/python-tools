#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :2019/6/8 15:20

import os
import redis
import configparser


class Myconfig(object):

    def __init__(self, config_file):
        if config_file is not None and os.path.exists(config_file):
            cf = configparser.ConfigParser()
            cf.read(config_file)

            self.rds_host = cf.get('redis', 'host')
            self.rds_port = cf.getint('redis', "port")
            self.rds_password = cf.get('redis', 'password')

    def get_rds(self):
        rds = redis.Redis(host=self.rds_host, port=self.rds_port, db=0, password=self.rds_password,
                          decode_responses=True)
        return rds

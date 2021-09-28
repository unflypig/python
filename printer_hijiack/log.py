#!/usr/bin/python
#-*- coding:utf-8 -*-
#Copyright (C) 2020 Geniatech Ltd. All rights reserved.
#File Name: log.py
#Author: zhangtao
#Mail: zhangtao@geniatech.com
#Created Time: 2020-12-11 18:18:48
###########################################################

import logging
from logging import handlers

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warn':logging.WARN,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }
    def __init__(self,filename,level='info',when='H',backCount=480,fmt='[%(asctime)s][%(levelname)-5s]->%(pathname)s(%(lineno)d):%(message)s'):
    #def __init__(self,filename,level='info',when='D',backCount=3,fmt='[%(levelname)-8s][%(asctime)s]->%(pathname)s(line:%(lineno)d) %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#set log format
        self.logger.setLevel(self.level_relations.get(level))#set log level
        sh = logging.StreamHandler()#echo to screen
        sh.setFormatter(format_str) #set format show on screen
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')
        th.setFormatter(format_str)
        self.logger.addHandler(sh) 
        self.logger.addHandler(th)
        #self.LOG = gtc_log_init(config.LOG_FILE_PATH, config.LOG_LEVEL)


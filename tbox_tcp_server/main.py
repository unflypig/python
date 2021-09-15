###########################################################
#!/usr/bin/python
#-*- coding:utf-8 -*-
#Copyright (C) 2020 Geniatech Ltd. All rights reserved.
#File Name: remote_cmd.py
#Author: zhangtao
#Mail: zhangtao@geniatech.com
#Created Time: 2021-03-30 12:09:06
###########################################################
import log
import socket
import sys
import time
import _thread
import os

upload_config_dir = {}
TABLE_NAME = "TBOX_DATA"
DATABASE_WRITE_ENABLE = True
tcp_socket = False
SERVER_CONN = False
#LOG = log.Logger(config.LOG_FILE_PATH,level=config.LOG_LEVEL)
LOG = log.Logger("/tmp/test.log","debug")
LOG.logger.info('remote cmd application start up')
def send_cmd(s):
    while True:
        rmt_cmd = input("============Please input remote command, end with enter:================")
        rmt_cmd = rmt_cmd.encode('utf-8')
        LOG.logger.info("============get command:[%s]===========" %rmt_cmd)
        if(len(rmt_cmd) > 5):
            s.send(rmt_cmd)
        time.sleep(1)
        #s.send("I AM A CMD")
        #time.sleep(1.5)

while True:
    server_domain = "172.17.36.9"
    server_port = 50003
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((server_domain, server_port))
    except:
        LOG.logger.error("bind to %s fail, retry..." %server_port)
        time.sleep(2)
        continue
    try:
        server.listen(5)
    except:
        LOG.logger.error("listen to %s fail, retry..." %server_port)
        time.sleep(2)
        continue
    LOG.logger.info("tcp server listen on port:%s success,start to wait connect..." %server_port)
    conn, addr = server.accept()
    LOG.logger.info("client:%s connected in %d port" %(addr[0], addr[1]))
    _thread.start_new_thread(send_cmd, (conn,))
    while True:
        try:
            data = conn.recv(1024)
            data = data.decode()
            LOG.logger.info("recieve from client:[%s]" %data)
            #HEAD,001,866834043101265,143807010421,VIN:DAFULA1ELECTR0N1C,GPS:,STAT:AAAA5,FUEL:FF;FF;FF;FF;FF,ENGINE:FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF,OTHER:FF;FF;FF;FF;FF;FF;FF;FF;FF;FF,MD5:4882C9BA781348AB53FD56CC10BC7BE5,FOOT#
            ack_data = ""
            if("UUID" in data):
                ack_data = data
                LOG.logger.info("ack data is [%s]" %ack_data)
            else:
                ack_data = data.split(",")[3]
                #ack_data = "8888888888888888888"
                ack_data = "#HEAD,001,TIME:" + ack_data +",FOOT#"
                LOG.logger.info("ack data is [%s]" %ack_data)
            conn.send(ack_data.encode('utf-8'))
        except:
            LOG.logger.info("fail")
            conn.close()
            conn, addr = server.accept()
            LOG.logger.info("client:%s connected in %d port" %(addr[0], addr[1]))

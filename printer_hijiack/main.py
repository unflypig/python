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
import thread
import os

upload_config_dir = {}
TABLE_NAME = "TBOX_DATA"
DATABASE_WRITE_ENABLE = True
tcp_socket = False
SERVER_CONN = False
#LOG = log.Logger(config.LOG_FILE_PATH,level=config.LOG_LEVEL)
LOG = log.Logger("/tmp/test.log","debug")
log = LOG.logger
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
def strToHex(data):
    HexData = ""
    for byte in data:
        HexByte = "%x" %ord(byte)
        HexByte = str(HexByte)
        if(len(HexByte) < 2):
            HexByte = "0" + HexByte
        HexData = HexData + "0x" + HexByte
    return HexData
def tcpClient():
    host = "10.168.4.144"
    port = 9100
    sock = False
    #Attempt connection to server
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
        except:
            LOG.logger.error("Could not make a connection to the server")
        else:
            LOG.logger.error("Make a connection to the server success")
            return sock

def tcpClientRecv(clienSock, serverSock):
    while True:
        data = clienSock.recv(2048)
        #data = data.decode()
        log.debug("recv form printer data[%s]" %strToHex(data))
        log.debug("Transmit to pos machine")
        serverSock.send(data)
        log.debug("Transmit to pos success")
def tcpServerRecv(clienSock, serverSock):
    while True:
        data = serverSock.recv(2048)
        #data = data.decode()
        log.debug("recv form pos machine data[%s]" %strToHex(data))
        log.debug("Transmit to printer")
        clienSock.send(data)
        log.debug("Transmit to printer success")



while True:
    #server_domain = "192.168.30.232"
    server_domain = "10.168.4.143"
    server_port = 9100
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
    #_thread.start_new_thread(send_cmd, (conn,))
    clientSock = tcpClient()
    thread.start_new_thread(tcpServerRecv, (clientSock, conn))
    thread.start_new_thread(tcpClientRecv, (clientSock, conn))
    while True:
        time.sleep(1)
    while True:
        try:
            data = conn.recv(1024)
            data = data.decode()
            data_str = strToHex(data)
            LOG.logger.info("recieve from pos machine:[%s]" %data_str)

            #conn.send(data)
            clientSock.send(data)
            LOG.logger.info("Transmit data form pos machine to printer success")

            LOG.logger.info("Wait printer response...")
            dataFromPrinter = clientSock.recv(1024)
            dataFromPrinter = dataFromPrinter.decode()
            LOG.logger.info("Get printer response[%s], transmit it to pos..." %strToHex(dataFromPrinter))

            conn.send(dataFromPrinter)
            LOG.logger.info("Transmit data form printer to pos machine success")
            #HEAD,001,866834043101265,143807010421,VIN:DAFULA1ELECTR0N1C,GPS:,STAT:AAAA5,FUEL:FF;FF;FF;FF;FF,ENGINE:FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF;FF,OTHER:FF;FF;FF;FF;FF;FF;FF;FF;FF;FF,MD5:4882C9BA781348AB53FD56CC10BC7BE5,FOOT#
        except:
            LOG.logger.info("fail")
            conn.close()
            conn, addr = server.accept()
            LOG.logger.info("client:%s connected in %d port" %(addr[0], addr[1]))


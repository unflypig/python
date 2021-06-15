#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import logging
import time
import sys
import os

logger = logging.getLogger("updatelog")
url = 'http://192.168.20.1:8000/cgi-bin/luci'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
    'Referer': url,
    'Connection': 'keep-alive'
}

data = {
    "username": "root",
    "password": "geniatech2018",
}

def get_SSH_stauts():
    r = requests.post(url, headers=headers, data=data)
    result = r.headers
    set_cookie = result['Set-Cookie']
    set_cookie_list = set_cookie.split(';')
    cookie = set_cookie_list[0]
    stok = set_cookie_list[2]

    getssh = url + '/;' + stok + '/admin/status/getSSHstatus'
    get_ssh_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
        'Referer': getssh,
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cookie': cookie
    }

    r = requests.get(getssh, headers = get_ssh_headers)
    return r.text

def set_SSH_val():
    r = requests.post(url, headers=headers, data=data)
    result = r.headers
    set_cookie = result['Set-Cookie']
    set_cookie_list = set_cookie.split(';')
    cookie = set_cookie_list[0]
    stok = set_cookie_list[2]

    setssh = url + '/;' + stok + '/admin/status/setSSHonoff'
    sshval = {
        'sshSwitch': '1'
    }
    set_ssh_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
        'Referer': setssh,
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cookie': cookie
    }

    r = requests.post(setssh, headers=set_ssh_headers, data=sshval)
    if r.status_code == 200:
        logger.info(u"打开 SSH 成功")

def main():
    txt = get_SSH_stauts()
    if txt == "off":
        set_SSH_val()
    else:
        logger.info(u"SSH 已经开启")

if __name__ == '__main__':
    logger.info(u"-----------------------------------------SSH")
    time.sleep(2)
    main()
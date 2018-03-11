#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 22:36:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import socket
import requests
import json

def isNetOK(testserver):
    s=socket.socket()
    s.settimeout(3)
    try:
        status = s.connect_ex(testserver)
        if status == 0:
            s.close()
            return True
        else:
            return False
    except Exception as e:
        return False

def isNetChainOK(testserver=('www.baidu.com',443)):
    isOK = isNetOK(testserver)
    return isOK
    

def isNetUSAOK(testserver=('www.google.com',443)):
    isOK = isNetOK(testserver)
    return isOK
    
def isNetYouTubeOK(testserver=('www.youtube.com',443)):
    isOK = isNetOK(testserver)
    return isOK

def isNetStateFromURL(purl = 'https://raw.githubusercontent.com/fengmm521/serverstate/master/serverstate.json',server = 'sell1.woodcol.com:4443'):
    res = requests.get(self.purl, verify=False)
    dictmp = json.loads(res.text)
    if server in dictmp and dictmp[server]:
        return True
    else:
        return False

def main():

    #在github上保存一个文件，用来设置服务器是否正常工作中:
    #然后使用https请法度这个文件：https://raw.githubusercontent.com/fengmm521/serverstate/master/serverstate.json
    chinanet = isNetChainOK()
    print chinanet
    usanet = isNetUSAOK()
    print usanet
    youtubenet = isNetYouTubeOK()
    print youtubenet
    

if __name__ == '__main__':
    main()

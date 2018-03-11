#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 22:36:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os, sys
import time

import json

import requests
import zlib

testHost = 'https://192.168.123.200:4443/'
Host = 'https://sell1.woodcol.com:4443/'

#压缩
def _compress(msg):
    dat = zlib.compress(msg, zlib.Z_BEST_COMPRESSION)
    print('ziplen-co-->',len(msg),len(dat))
    return dat

#解压缩
def _decompress(dat):
    msg = zlib.decompress(dat)
    print('ziplen-de-->',len(dat),len(msg))
    return msg


def postDataToURL(purl,data,isTest = False):
    rurl = ''
    if isTest:
        rurl = testHost + purl
    else:
        rurl = Host + purl
    print rurl
    cdata = _compress(data)
    response = requests.post(rurl,data=cdata,verify=False)
    dat = response.text
    return dat

def getDataFromURL(purl,isTest = False):
    
    rurl = ''
    if isTest:
        rurl = testHost + purl
    else:
        rurl = Host + purl
    print rurl
    try:
        s = requests.session()
        s.headers.update({'User-agent', 'Mozilla 5.10'})
        res = s.get(rurl, verify=False)
        return res.text
    except Exception, e:
        print e
    return None

def trail(dmsg,isTest = False):
    dat = json.dumps(dmsg)
    res = postDataToURL('trail',dat,isTest)
    print(res)
    return res

def bind(dmsg,isTest = False):

    dat = json.dumps(dmsg)
    res = postDataToURL('bind',dat,isTest)
    print(res)
    return res

def check(dmsg,isTest = False):
    dat = json.dumps(dmsg)
    res = postDataToURL('check',dat,isTest)
    print(res)
    return res


def main():

    tmp = {}
    tmphard = {}
    tmphard['cpu'] = {'cpuip':'123456789','cpuspeed':'3.4G','cpucore':4,'cpures':'intel i5'}
    tmphard['harddisk'] = {'sid':'adbcd1234','UUID':'xxxx-xxxx-xxxx-xxxx','Size':1024000}
    tmphard['memory'] = [{'sid':'abckdaeff111','UUID':'xxxx-xxxx-xxxx-0001','Size':8000},{'sid':'abckdaeff111','UUID':'xxxx-xxxx-xxxx-0002','Size':8000}]
    tmphard['mainboard'] = {'sid':'djo2032i11','UUID':'mainboard-ccxxx-cefesd-xxxx'}
    tmphard['BIOS'] = {'sid':'doeibios000','version':'versionxxx'}
    tmphard['netMacaddr'] = {'name':'netcard','mac':'12-34-32-12-33'}
    tmp['hardmsg'] = tmphard

    tmp['cardid'] = ''

    tmp['time'] = str(int(time.time()))

    tmp['type'] = 'trail'

    trail(tmp,isTest = True)
    time.sleep(0.5)
    
    tmp = {}
    tmphard = {}
    tmphard['cpu'] = {'cpuip':'123456789','cpuspeed':'3.4G','cpucore':4,'cpures':'intel i5'}
    tmphard['harddisk'] = {'sid':'adbcd1234','UUID':'xxxx-xxxx-xxxx-xxxx','Size':1024000}
    tmphard['memory'] = [{'sid':'abckdaeff111','UUID':'xxxx-xxxx-xxxx-0001','Size':8000},{'sid':'abckdaeff111','UUID':'xxxx-xxxx-xxxx-0002','Size':8000}]
    tmphard['mainboard'] = {'sid':'djo2032i11','UUID':'mainboard-ccxxx-cefesd-xxxx'}
    tmphard['BIOS'] = {'sid':'doeibios000','version':'versionxxx'}
    tmphard['netMacaddr'] = {'name':'netcard','mac':'12-34-32-12-33'}
    tmp['hardmsg'] = tmphard

    tmpCard = {}
    tmpCard['sid'] = 'testcard12334928392'
    tmp['cardid'] = tmpCard

    tmp['time'] = str(int(time.time()))

    tmp['type'] = 'bind'

    bind(tmp,isTest = True)
    time.sleep(0.5)

    tmp = {}
    tmphard = {}
    tmphard['cpu'] = {'cpuip':'123456789','cpuspeed':'3.4G','cpucore':4,'cpures':'intel i5'}
    tmphard['harddisk'] = {'sid':'adbcd1234','UUID':'xxxx-xxxx-xxxx-xxxx','Size':1024000}
    tmphard['memory'] = [{'sid':'abckdaeff111','UUID':'xxxx-xxxx-xxxx-0001','Size':8000},{'sid':'abckdaeff111','UUID':'xxxx-xxxx-xxxx-0002','Size':8000}]
    tmphard['mainboard'] = {'sid':'djo2032i11','UUID':'mainboard-ccxxx-cefesd-xxxx'}
    tmphard['BIOS'] = {'sid':'doeibios000','version':'versionxxx'}
    tmphard['netMacaddr'] = {'name':'netcard','mac':'12-34-32-12-33'}
    tmp['hardmsg'] = tmphard

    tmpCard = {}
    tmpCard['sid'] = 'testcard12334928392'
    tmp['cardid'] = tmpCard

    tmp['time'] = str(int(time.time()))

    tmp['type'] = 'check'

    check(tmp,isTest = True)
    time.sleep(0.5)

if __name__ == '__main__':
    main()

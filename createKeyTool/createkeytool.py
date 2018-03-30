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
import hashlib
import base64

import platform

sysSystem = platform.system()


testHost = 'https://192.168.123.200:4443/'
Host = 'https://sell1.woodcol.com:4443/'

class CreateKeyTool(object):
    """docstring for ClientRegTool"""
    def __init__(self,savePth = './youtubekey'):
        super(CreateKeyTool, self).__init__()
        self.keysavePth = savePth + os.sep +'out'
        self.key1kapth = savePth + os.sep +'1ka'
        if not os.path.exists(self.key1kapth):
            os.mkdir(self.key1kapth)
        if not os.path.exists(self.keysavePth):
            os.mkdir(self.keysavePth) 

    def saveNewKeyToFile(self,keystr):

        fname = str(time.strftime("%Y-%m-%d_%H%M%S",time.localtime()))
        
        fpth = self.keysavePth + os.sep + fname + '.txt'
        keys = json.loads(keystr)
        outstr = ''
        for k in keys:
            outstr += k + '\n'
        outstr = outstr[:-1]
        f = open(fpth,'w')
        f.write(outstr)
        f.close()

        fpth = self.key1kapth + os.sep + fname + '.txt'
        keys = json.loads(keystr)
        outstr = ''
        for k in keys:
            outstr += k + ','
        outstr = outstr[:-1]
        f = open(fpth,'w')
        f.write(outstr)
        f.close()


    #压缩
    def _compress(self,msg):
        dat = zlib.compress(msg, zlib.Z_BEST_COMPRESSION)
        print('ziplen-co-->',len(msg),len(dat))
        return dat

    #解压缩
    def _decompress(self,dat):
        msg = zlib.decompress(dat)
        print('ziplen-de-->',len(dat),len(msg))
        return msg


    def postDataToURL(self,purl,data,isTest = False):
        rurl = ''
        if isTest:
            rurl = testHost + purl
        else:
            rurl = Host + purl
        print rurl
        cdata = self._compress(data)
        response = requests.post(rurl,data=cdata,verify=False)
        dat = response.text
        if len(dat) > 0:
            dattmp = base64.b64decode(dat)
            msg = self._decompress(dattmp)
            return msg
        else:
            return ''

    def getDataFromURL(self,purl,isTest = False):
        
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

    def getUrl(self,purl):
        try:
            if purl[0:5] == 'https':
                res = requests.get(self.purl, verify=False)
                print(res.text)
                return res.text
            else:
                res = requests.get(self.purl)
                print(res.text)
                return res.text
        except Exception as e:
            print(e)
        return None

    

    def createKeys(self,count = 50,isTest = False):
        f = open('./youtubekey/create.json','r')
        jstr = f.read()
        f.close()
        dat = json.loads(jstr)
        dat['count'] = count
        outstr = json.dumps(dat)
        res = self.postDataToURL('mycreate',outstr,isTest)
        keys = json.loads(res)
        self.saveNewKeyToFile(keys)

    def openKeyDir(self):
        if sysSystem == 'Windows':  
            os.startfile('./youtubekey')
        elif sysSystem == 'Darwin':
            cmd = 'open %s'%('./youtubekey')
            os.system(cmd)
        elif sysSystem == 'Linux':
            cmd = 'xdg-open %s'%('./youtubekey')
            os.system(cmd)
            

def main(arg):
    createobj = CreateKeyTool()
    if len(arg) == 2:
        createobj.createKeys(count = int(arg[1]),isTest = False)
    elif len(arg) == 3:
        createobj.createKeys(count = int(arg[1]),isTest = bool(arg[2]))
    else:
        createobj.createKeys(count = 10,isTest = False)
    time.sleep(0.5)
    createobj.openKeyDir()


if __name__ == '__main__':
    arg = sys.argv
    main(arg)

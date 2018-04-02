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

from clienttool import SystemMsgTool
from clienttool import AEStool
from clienttool import importFile

class UpdateTool(object):
    """docstring for ClientRegTool"""
    def __init__(self,isDebug = False):
        super(UpdateTool, self).__init__()

        self.isDebug = isDebug

        if not os.path.exists('data'):
            os.mkdir('data')

        if self.isDebug:
            self.Host = 'https://192.168.123.200:4443/'
        else:
            self.Host = 'https://sell1.woodcol.com:4443/'

        self.clienttoolpth = 'data' + os.sep + 'clientRegTool'

        self.hardmsg = self.getSystemMsg()

        aeskey = self.getAESKey()
        self.aesobj = AEStool.prpcrypt(aeskey)

        self.importObj = importFile.LoadModeTool(self.aesobj)

        if not os.path.exists('data'):
            os.mkdir('data')
    
    def getSystemMsg(self):
        return SystemMsgTool.SystemMsgObj().getSysMsg()

    def getAESKey(self):
        hardIDtmp = self.hardmsg['HardID'] + 'clientcode.woodcol.com'
        hexstr = hashlib.sha256(hardIDtmp).hexdigest()
        result = bytearray.fromhex(hexstr)
        return bytes(result)
    #压缩
    def _compress(self,msg):
        dat = zlib.compress(msg, zlib.Z_BEST_COMPRESSION)
        # print('ziplen-co-->',len(msg),len(dat))
        return dat

    #解压缩
    def _decompress(self,dat):
        msg = zlib.decompress(dat)
        # print('ziplen-de-->',len(dat),len(msg))
        print('正在解压数据...')
        return msg

    def postDataToURL(self,purl,data):
        rurl = self.Host + purl
        cdata = self._compress(data)
        # print rurl
        print('正在获取数据...')
        response = requests.post(rurl,data=cdata,verify=False)
        dat = response.text
        if len(dat) > 0:
            dattmp = base64.b64decode(dat)
            msg = self._decompress(dattmp)
            return msg
        else:
            print('加载clientregtool错误')
            return ''

    def saveCode(self,pcode):
        objcode = base64.b64decode(pcode)
        self.importObj.saveEnSourceToFile(objcode,self.clienttoolpth)
        m = self.importObj.loadAESModeFormEnSource(objcode, 'clientRegTool')
        return m

    def getClientRegTool(self):
        harddic = {}
        if os.path.exists(self.clienttoolpth):
            m = self.importObj.loadAESModeFromFile(self.clienttoolpth, 'clientRegTool')
            return m
        harddictmp = self.hardmsg
        harddic['HardID'] = harddictmp['HardID']
        dat = json.dumps(harddic)
        res = self.postDataToURL('code',dat)
        bdic = json.loads(res)
        clienttool = self.saveCode(bdic['code'])
        return clienttool

    def getDownTool(self,imobj):
        m = imobj.loadAESModeFromFile(self.downlaodpth, 'downtool')
        return m




def main():
    time.sleep(0.5)

if __name__ == '__main__':
    main()

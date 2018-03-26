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
from clienttool import RSAtool

testHost = 'https://192.168.123.200:4443/'
Host = 'https://sell1.woodcol.com:4443/'

class ClientRegTool(object):
    """docstring for ClientRegTool"""
    def __init__(self):
        super(ClientRegTool, self).__init__()
        self.clienDataPth = 'data' + os.sep + 'client.dat'

        aeskey = self.getAESKey()
        self.aesobj = AEStool.prpcrypt(aeskey)
        codeAESKey = self.getCodeAESKey()
        self.aesCodeObj = AEStool.prpcrypt(codeAESKey)   #试用时使用的加密方法
        self.softID = ''
        if not os.path.exists('data'):
            os.mkdir('data')
        
        self.isTrail = True
        self.getIsTrailFromClient()

    def saveMsgToClientObj(self,key,strmsg):
        clientobj = {}
        if os.path.exists(self.clienDataPth):
            f = open(self.clienDataPth,'rb')
            dat = f.read()
            f.close()
            datstr = self.aesobj.decrypt(dat)
            clientobj = json.loads(datstr)
            clientobj[key] = strmsg
        else:
            clientobj[key] = strmsg
        jstr = json.dumps(clientobj)
        endat = self.aesobj.encrypt(jstr)
        f = open(self.clienDataPth,'wb')
        f.write(endat)
        f.close()

    def getMsgFromClientObj(self,key):
        clientobj = {}
        if os.path.exists(self.clienDataPth):
            f = open(self.clienDataPth,'rb')
            dat = f.read()
            f.close()
            datstr = self.aesobj.decrypt(dat)
            clientobj = json.loads(datstr)
            if key in clientobj:
                return clientobj[key]
        return ''

    def saveIsTrailToclient(self):
        self.saveMsgToClientObj('isTrail',str(int(self.isTrail)))
    def getIsTrailFromClient(self):
        tmpstr = self.getMsgFromClientObj('isTrail')
        if tmpstr == '0' or tmpstr == '':
            self.isTrail = False
        else:
            self.isTrail = True

    def saveDataToClient(self,fname,data):
        fpth = 'data' + os.sep + fname
        eddat = self.aesobj.encrypt(data)
        f = open(fpth,'wb')
        f.write(eddat)
        f.close()

    def readDataFromClient(self,fname):
        fpth = 'data' + os.sep + fname
        if os.path.exists(fpth):
            f = open(fpth,'rb')
            dat = f.read()
            f.close()
            outdat = self.aesobj.decrypt(dat)
            return outdat
        return None

    def getSystemMsg(self):
        return SystemMsgTool.SystemMsgObj().getSysMsg()

    def getAESKey(self):
        harddic = self.getSystemMsg()
        hardIDtmp = harddic['HardID'] + 'woodcol.com'
        hexstr = hashlib.sha256(hardIDtmp).hexdigest()
        result = bytearray.fromhex(hexstr)
        if len(result) >= 128:
            return result[:128]
        else:
            return None

    def getCodeAESKey(self):
        harddic = self.getSystemMsg()
        regID = self.getMsgFromClientObj('regID')
        hardIDtmp = harddic['HardID'] + 'code.woodcol.com' + regID
        hexstr = hashlib.sha256(hardIDtmp).hexdigest()
        result = bytearray.fromhex(hexstr)
        if len(result) >= 128:
            return result[:128]
        else:
            return None
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


    def trail(self,isTest = False):
        harddic = self.getSystemMsg()
        harddic['regID'] = ''
        dat = json.dumps(harddic)
        res = self.postDataToURL('trail',dat,isTest)
        bdic = json.loads(res)
        print(bdic['erro'])
        print(bdic['msg'])

    def bind(self,regCodeID,isTest = False):
        if len(regCodeID) < 10:
            print('注册码输入错误')
            return
        harddic = self.getSystemMsg()
        harddic['regID'] = regCodeID
        dat = json.dumps(harddic)
        res = self.postDataToURL('bind',dat,isTest)
        bdic = json.loads(res)
        print(bdic['erro'])
        print(bdic['msg'])

        if bdic['erro'] == 0:
            self.isTrail = False
            self.saveIsTrailToclient()
            code = bdic['code']



    def check(self,regCodeID = None,isTest = False):
        harddic = self.getSystemMsg()
        if regCodeID != None:
            harddic['regID'] = regCodeID
        else:
            harddic['regID'] = self.getMsgFromClientObj('regID')
        dat = json.dumps(harddic)
        res = self.postDataToURL('check',dat,isTest)
        bdic = json.loads(res)
        print(bdic['erro'])
        print(bdic['msg'])

    def sendPubkey(self):
        pass

    def sendURLMsg(self,msg,isTest):
        harddic = {}
        harddic['HardID'] = self.getSystemMsg()['HardID']
        harddic['url'] = msg
        harddic['isTrail'] = int(self.isTrail)
        dat = json.dumps(harddic)
        res = self.postDataToURL('msg',dat,isTest)
        bdic = json.loads(res)
        print(bdic['erro'])
        print(bdic['msg'])
        print(bdic['count'])




def main():
    regobj = ClientRegTool()
    regobj.trail(isTest = True)
    time.sleep(0.5)

    regobj.bind('027tQGphPbmiYXwNmzrVDvZA',isTest = True)
    time.sleep(0.5)

    regobj.check('027tQGphPbmiYXwNmzrVDvZA',isTest = True)
    time.sleep(0.5)

    regobj.sendURLMsg('https://woodcol.com',isTest = True)
    time.sleep(0.5)

if __name__ == '__main__':
    main()

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

class ClientRegTool(object):
    """docstring for ClientRegTool"""
    def __init__(self,isDebug = False):
        super(ClientRegTool, self).__init__()

        if not os.path.exists('data'):
            os.mkdir('data')

        self.clienDataPth = 'data' + os.sep + 'client.dat'


        self.downlaodpth = 'data' + os.sep + 'downloadtool'

        self.isDebug = isDebug

        self.rqimagePth = 'data' + os.sep + 'image.png'

        if self.isDebug:
            self.Host = 'https://192.168.123.200:4443/'
        else:
            self.Host = 'https://sell1.woodcol.com:4443/'

        self.downcount = 0

        self.downtoolMode = None

        aeskey = self.getAESKey()
        self.aesobj = AEStool.prpcrypt(aeskey)
        codeAESKey = self.getCodeAESKey()
        self.aesCodeObj = AEStool.prpcrypt(codeAESKey)   #试用时使用的加密方法

        self.importObj = importFile.LoadModeTool(self.aesCodeObj)

        self.softID = ''
        if not os.path.exists('data'):
            os.mkdir('data')
        
        if not os.path.exists(self.rqimagePth):
            self.getStoreRQImageFromServer()

        self.isTrail = True
        self.getIsTrailFromClient()

    def getDownTool(self):
        if self.downtoolMode:
            return self.downtoolMode
        self.downtoolMode = self.importObj.loadAESModeFromFile(self.downlaodpth, 'downtool')
        return self.downtoolMode

    def getStoreRQImageFromServer(self):
        imageurl = 'image.png'
        rurl = self.Host + imageurl
        s = requests.Session()
        s.headers.update({'User-agent':'Mozilla 5.10'})
        html = s.get(rurl,verify=False)
        with open(self.rqimagePth, 'wb') as file:
            file.write(html.content)
    def getDownloadToolOjb(self):
        if not os.path.exists(self.downlaodpth):
            self.getDownloadToolOjb()               

    #从服务器下载相应下载工具代码
    def getDownLoadToolFromServer(self):
        pass

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
        hardIDtmp = harddic['HardID'] + 'youtube.woodcol.com'
        hexstr = hashlib.sha256(hardIDtmp).hexdigest()
        result = bytearray.fromhex(hexstr)
        return bytes(result)

    def getCodeAESKey(self,regID = None):
        harddic = self.getSystemMsg()
        tmpRegID = ''
        if regID != None:
            tmpRegID = regID
        else:
            tmpRegID = self.getMsgFromClientObj('regID')
        hardIDtmp = harddic['HardID'] + 'code.woodcol.com' + tmpRegID
        # print(hardIDtmp)
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
        print('正在请求数据...')
        response = requests.post(rurl,data=cdata,verify=False)
        dat = response.text
        if len(dat) > 0:
            dattmp = base64.b64decode(dat)
            msg = self._decompress(dattmp)
            return msg
        else:
            return ''

    def getDataFromURL(self,purl):
        rurl = self.Host + purl
        try:
            s = requests.Session()
            s.headers.update({'User-agent', 'Mozilla 5.10'})
            res = s.get(rurl, verify=False)
            return res.text
            # html.content
        except Exception, e:
            print e
        return None

    def getUrl(self,purl):
        try:
            if purl[0:5] == 'https':
                res = requests.get(self.purl, verify=False)
                # print(res.text)
                return res.text
            else:
                res = requests.get(self.purl)
                # print(res.text)
                return res.text
        except Exception as e:
            print(e)
        return None


    def trail(self,isGetCode = False):
        harddic = self.getSystemMsg()
        harddic['regID'] = ''
        if isGetCode:
            harddic['getCode'] = 'downtool'
        dat = json.dumps(harddic)
        res = self.postDataToURL('trail',dat)
        bdic = json.loads(res)
        # print(bdic['erro'])
        # print(bdic['msg'])
        if len(bdic['code']) > 100:
            code = bdic['code']
            encode = base64.b64decode(code)
            if 'regID' in bdic:
                codeAESKey = self.getCodeAESKey(bdic['regID'])
                self.saveMsgToClientObj('regID',bdic['regID'])
                self.aesCodeObj = AEStool.prpcrypt(codeAESKey)   #试用时使用的加密方法
            self.importObj.aesobj = self.aesCodeObj
            self.importObj.saveEnSourceToFile(encode, self.downlaodpth)
            self.downtoolMode = self.importObj.loadAESModeFormEnSource(encode,'downtool')
        return bdic

    def bind(self,regCodeID):
        if len(regCodeID) < 10:
            print('注册码输入错误'.decode())
            return
        harddic = self.getSystemMsg()
        harddic['regID'] = regCodeID
        dat = json.dumps(harddic)
        res = self.postDataToURL('bind',dat)
        bdic = json.loads(res)
        # print(bdic['erro'])
        # print(bdic['msg'])

        if bdic['erro'] == 0:
            self.isTrail = False
            self.saveIsTrailToclient()
            self.saveMsgToClientObj('regID', regCodeID)
            code = bdic['code']
            encode = base64.b64decode(code)
            self.importObj.saveEnSourceToFile(encode, self.downlaodpth)
        return bdic['msg'],bdic['erro']



    def check(self,regCodeID = None):
        harddic = self.getSystemMsg()
        if regCodeID != None:
            harddic['regID'] = regCodeID
        else:
            harddic['regID'] = self.getMsgFromClientObj('regID')
        dat = json.dumps(harddic)
        res = self.postDataToURL('check',dat)
        bdic = json.loads(res)
        # print(bdic['erro'])
        # print(bdic['msg'])
        if bdic['erro'] == 1:
            code = bdic['code']
            encode = base64.b64decode(code)
            self.importObj.saveEnSourceToFile(encode, self.downlaodpth)


    def sendPubkey(self):
        pass

    def getDownCount(self):
        count = self.getMsgFromClientObj('downcount')
        if count != None and count != '':
            return int(count)
        else:
            return 0

    def sendURLMsg(self,msg):
        harddic = {}
        harddic['HardID'] = self.getSystemMsg()['HardID']
        harddic['url'] = msg
        harddic['isTrail'] = int(self.isTrail)
        dat = json.dumps(harddic)
        res = self.postDataToURL('msg',dat)
        bdic = json.loads(res)
        # print(bdic['erro'],'erro')
        # print(bdic['msg'],'msg')
        # print(bdic['count'],'count')
        self.downcount = bdic['count']
        self.saveMsgToClientObj('downcount', bdic['count'])
        return bdic['erro'],self.downcount




def main():
    regobj = ClientRegTool(isDebug = True)
    regobj.trail()
    time.sleep(0.5)

    regobj.bind('027tQGphPbmiYXwNmzrVDvZA')
    time.sleep(0.5)

    regobj.check('027tQGphPbmiYXwNmzrVDvZA')
    time.sleep(0.5)

    regobj.sendURLMsg('https://woodcol.com')
    time.sleep(0.5)

if __name__ == '__main__':
    main()

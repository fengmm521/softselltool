#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 22:36:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os, sys
import time
import clienttool
import RSAtool
import AEStool
import NetWorkTest


class Authentication(object):
    """docstring for Authentication"""
    def __init__(self):
        self.version = None     #软件版本
        self.hardMsg = None     #软件运行硬件环境信息
        self.osMsg = None       #软件运行操作系统
        self.osVersion = None   #软件运行操作系统版本
        self.RegistCode = None  #购买的注册码
        self.AESKey = None      #使用注册码和硬件码生成的AES本地数据加密密码
        self.mRSAPubKey = None  #验证服务器的公钥密码
        self.hosturl = 'https://sell1.woodcol.com:4443/'
        self.mkeyUrl = self.hosturl + 'public.pem'          #向服务器请求服务器公钥
        self.sendUPubKeyUrl = self.hosturl + 'userPubkey'   #使用服务器端公钥加密后向服务器发送自已的公钥
        self.trailUrl = self.hosturl + 'trail'              #试用
        self.bindUrl = self.hosturl + 'bind'                #绑定
        self.checkUrl = self.hosturl + 'check'              #验证

        self.mKeyPth = './data'         #服务器公钥保存地址
        self.gKeyPth = './data'         #本地密钥
        self.registCodePth = './data'   #已注册信息
        #从服务器下载的库文件，当用户注册后或者发送试用时从服务器下载得到,试用版会得到有库文件使用次数限制内容,注册版库文件没有使用次数限制
        self.libPth = './lib'   
        self.AESObj = None
        self.RSAObj = None

        self.baiduStat = False           #国内网络访问是否正常
        self.YoutubeStat = False         #youtube访问是否正常
        self.GoogleStat = False          #google访问是否正常
        self.serverStat = False          #验证服务器设置是否正常

        self.init()

    def init(self):

        self.baiduStat = NetWorkTest.isNetChainOK()
        self.YoutubeStat = NetWorkTest.isNetYouTubeOK()
        self.GoogleStat = NetWorkTest.isNetUSAOK()
        self.serverStat = NetWorkTest.isNetStateFromURL()

        #此时会生一个临时的RSA私钥和公钥
        self.RSAObj = RSAtool.prpcrypt(self.mkeyUrl, self.mKeyPth, self.gKeyPth,isCreateGkey = True)
    
        if self.YoutubeStat and self.serverStat:
            self.sendGPubKeyToServer()
            self.checkSoftRunState()
        else:
            print('访问youtube或者本地服务器错误')


    #将用户公钥发送给服务器端
    def sendGPubKeyToServer(self):
        gpubkeypsck1 = self.RSAObj.getGPubkey()
        res = clienttool.postDataToURL(self.sendUPubKeyUrl, gpubkeypsck1)
        print(res)  
        #服务器返回用户数据AES加密关键字
        #之后服务器发送下来的文件用户保存在本地时使用userHardID + AES关键字的sha1值加密保存
        #AES关键字使用userHardID + 一个特别字符串保存在本地

    #获取软件运行类型,1.试用,2.已注册,3.注册服务器连接失败
    def checkSoftRunState(self):
        print('checkSoftRunState---->...')


    def getDataFromServer(self,url,name):
        dat = clienttool.postDataToURL(url, str(name))
        ddat = self.RSAObj.decryptWithGhostPriKey(dat)
        print(ddat)
        return ddat

def main():

    pass
    

if __name__ == '__main__':
    main()

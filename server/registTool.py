#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-07 09:28:00
# @Link    : http://fengmm521.blog.163.com
# @Version : $Id$
#https服务器
import os
import json
import time
import RSAtool
import dbTool
import hashlib
import base58

def httpGet(urlstr):
    req = urllib2.Request(urlstr)
    req.add_header('User-agent', 'Mozilla 5.10')
    res = urllib2.urlopen(req)
    html = res.read()
    return html


class RegistTool(object):
    """docstring for WXMsgTool"""
    def __init__(self,keyPth = './regkeys',dbpth = './db'):
        super(RegistTool, self).__init__()
        
        self.keyPth = keyPth
        self.userPubKeyPth = keyPth + '/userpubkey'
        if not os.path.exists(self.keyPth):
            os.mkdir(self.keyPth)
            os.mkdir(self.userPubKeyPth)
        
        self.RSAObj = None
        self.dbPth = dbpth


        self.userPubKeys = {}

        self.db = dbTool.DBMObj(self.dbPth)

        self.initRSAKey()
    def initRSAKey(self):
        
        self.RSAObj = RSAtool.prpcrypt('', self.userPubKeyPth, self.keyPth,isCreateGkey = False)

    def setUserPubKeys(self,userHardID,pubkeypkcs1):
        self.userPubKeys[userHardID] = self.RSAObj.getKeyWithPKCS1(pubkeypkcs1)

    def getServerPubkey(self):
        return self.RSAObj.getGPubkey()



    #使用用户公钥发送加密消息给用户
    def encrypMsgToUser(self,userHardID,msg):
        if userHardID in self.userPubKeys:
            emsg = self.RSAObj.encryptWithPubKey(msg, self.userPubKeys[userHardID])
            return emsg
        else:
            print('erro.用户(%s)公钥不存在'%(userHardID))
            return None

    #使用服务器私钥解密用户发送的数据
    def decryptMsg(self,emsg):
        msg = self.RSAObj.decryptWithGhostPriKey(emsg)
        return msg

    #收到用户已解密后的数据
    def resiveUserMsg(self,emsg,sendHandel):
        msg = self.decryptMsg(emsg)
        print(msg)


        #这里是用户注册消息处理逻辑
        userHardID = self.getUserHardIDWithHardMsg(msg)

        #处理完之后消息返回用户

        self.sendMsgToUser(userHardID,msg,sendHandel)



    #通过用户硬件获取用户硬件ID
    def getUserHardIDWithHardMsg(self,msg):
        print(msg)

    def sendMsgToUser(self,userHardID,msg,sendHandel):

        #得到用户公钥加密后的消息
        emsg = self.encrypMsgToUser(userHardID, msg)
        #https响应消息给用户
        sendHandel.sendMsg(emsg)

    #生成新的注册码
    def createRegistCode(self,count = 50):
        ks = []
        sendtmp = str(time.time())
        
        crcount = self.db.select('createcount')
        if crcount == None:
            crcount = 1
        else:
            crcount = int(crcount) + 1
        kfrontstr = base58.b58encode_int(crcount)
        if len(kfrontstr) == 1:
            kfrontstr = '0' + kfrontstr
        for i in range(count):
            tmpn = '0x' + hashlib.md5(sendtmp + str(i)).hexdigest()
            num = int(tmpn,16)
            bastr = base58.b58encode_int(num)
            tmpka = kfrontstr + bastr
            ks.append(tmpka)
        vs = ['{}'] * count
        self.db.insetList(ks, vs)
        jout = json.dumps(ks)
        return jout



if __name__ == '__main__':
    


# # 生成rsa密钥
# $ openssl genrsa -des3 -out server.key 2048
# # 去除掉密钥文件保护密码
# $ openssl rsa -in server.key -out server.key
# # 生成ca对应的csr文件
# $ openssl req -new -key server.key -out server.csr
# # 自签名
# $ openssl x509 -req -days 2048 -in server.csr -signkey server.key -out server.crt
# $ cat server.crt server.key > server.pem

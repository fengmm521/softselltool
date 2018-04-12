#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-07 09:28:00
# @Link    : http://fengmm521.blog.163.com
# @Version : $Id$
#https服务器
import os
import json
import time
# import RSAtool
import dbTool
import hashlib
import base58


if not os.path.exists('db'):
    os.mkdir('db')

class hardKeysTool(object):
    """docstring for WXMsgTool"""
    def __init__(self,dbpth = './db/hard'):
        super(hardKeysTool, self).__init__()
        
        self.dbPth = dbpth
        if not os.path.exists(self.dbPth):
            os.mkdir(self.dbPth)

        #用户硬件信息,使用硬件唯一uuid作为key
        self.hardDBpth     =   self.dbPth + os.sep + 'hard'
        self.hardDB        =   dbTool.DBMObj(self.hardDBpth)    
        
        #用户硬件登陆次数
        self.loginTimesPth = self.dbPth + os.sep + 'hardloginTimes'
        self.loginDB       =   dbTool.DBMObj(self.loginTimesPth)   


    def addHardMsgToDB(self,hardMsg):
        nkey = hardMsg['HardID']
        jstrmsg = json.dumps(hardMsg)
        self.hardDB.inset(nkey, jstrmsg)
        return nkey

    def getHardMsg(self,hardID):
        dat = self.hardDB.select(hardID)
        out = None
        if dat and dat != None:
            out = json.loads(dat)
        return out
    
    #为一个硬件设备数据库增加注册码
    def setResCodeWithHardMsg(self,hardMsgObj,resCode):
        tmphardMsg = hardMsgObj
        tmphardMsg['regID'] = resCode
        hkey = self.addHardMsgToDB(tmphardMsg)
        return hkey,resCode
    #获取硬件的软件注册码，没有注册过的客户端将返回None
    def getHardHeaveResCode(self,hardID):
        dat = self.getHardMsg(hardID)
        if dat and dat != None:
            if 'regID' in dat:
                return dat['regID']
        return None

    #为一个硬件增加一次登陆次数,返回用户登陆次数
    def hardLogin(self,hardID):
        dat = self.loginDB.select(hardID)
        dattmp = {}
        if dat and dat!= None:
            dattmp = json.loads(dat)
            dattmp['logintimes'] += 1
        else:
            dattmp = {'logintimes':1}
        out = json.dumps(dattmp)
        self.loginDB.inset(hardID, out)
        return dattmp['logintimes']

if __name__ == '__main__':
    hardtool = hardKeysTool()


# # 生成rsa密钥
# $ openssl genrsa -des3 -out server.key 2048
# # 去除掉密钥文件保护密码
# $ openssl rsa -in server.key -out server.key
# # 生成ca对应的csr文件
# $ openssl req -new -key server.key -out server.csr
# # 自签名
# $ openssl x509 -req -days 2048 -in server.csr -signkey server.key -out server.crt
# $ cat server.crt server.key > server.pem

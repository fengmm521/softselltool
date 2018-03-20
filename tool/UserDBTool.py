#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-07 09:28:00
# @Link    : http://fengmm521.blog.163.com
# @Version : $Id$
#用户下载视频网址记录
import os
import json
import time
import RSAtool
import dbTool
import hashlib
import base64

MAXTESTCOUNT = 5


#用户下载记录
class UserDBTool(object):
    """docstring for WXMsgTool"""
    def __init__(self,dbpth = './db/userdb'):
        super(UserDBTool, self).__init__()
        
        if not os.path.exists('db'):
            os.mkdir('db')


        if not os.path.exists(dbpth):
            os.mkdir(dbpth)

        #试用用户下载记录
        self.testdbpth = dbpth + os.sep + 'testdir'
        if not os.path.exists(self.testdbpth):
            os.mkdir(self.testdbpth)

        self.testdb = dbTool.DBMObj(self.testdbpth + os.sep + 'test')

        #正式用户下载记录
        self.userpth = dbpth + os.sep + 'reguser'
        if not os.path.exists(self.userpth):
            os.mkdir(self.userpth)
        
        self.basedbPth = dbpth

    #试用用户使用软件唯一ID保存下载的视频
    def addUserDBWithTestSoftID(self,softID,purl):
        tusrdat = self.testdb.select(softID)
        isTooLong = False
        if tusrdat != None:
            plist = json.loads(tusrdat)
            base64str = base64.b64encode(purl)
            plist.append(base64str)
            if len(plist) > MAXTESTCOUNT:
                isTooLong = True
                plist = plist[-5:]
                savestr = json.dumps(plist)
                self.testdb.inset(softID, savestr)
            else:
                savestr = json.dumps(plist)
                self.testdb.inset(softID, savestr)
        return isTooLong

    def addUserListDBWithRegCode(self,regCode,purls):
        tmpdb = dbTool.DBMObj(self.userpth + os.sep + regCode)
        keys = []
        values = []
        ks = tmpdb.allKeys()
        startn = 1
        if ks == None or len(ks) < 1:
            startn = 1
        else:
            startn = len(ks) + 1
        for n in range(len(purls)):
            keys.append(str(startn + n))
            base64str = base64.b64encode(purls[n])
            values.append(base64str)
        tmpdb.insetList(keys, values)

    #保存正式用户的下载地址
    def addUserDBWithRegCode(self,regCode,purl):
        tmpdb = dbTool.DBMObj(self.userpth + os.sep + regCode)
        base64str = base64.b64encode(purl)
        ks = tmpdb.allKeys()
        if ks == None or len(ks) < 1:
            tmpdb.inset('1', base64str)
        else:
            key = len(ks) + 1
            tmpdb.inset(str(key), )




if __name__ == '__main__':
    regtool = RegistTool()
    keys = regtool.createRegistCode()
    print keys

# # 生成rsa密钥
# $ openssl genrsa -des3 -out server.key 2048
# # 去除掉密钥文件保护密码
# $ openssl rsa -in server.key -out server.key
# # 生成ca对应的csr文件
# $ openssl req -new -key server.key -out server.csr
# # 自签名
# $ openssl x509 -req -days 2048 -in server.csr -signkey server.key -out server.crt
# $ cat server.crt server.key > server.pem

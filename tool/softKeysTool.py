#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-07 09:28:00
# @Link    : http://fengmm521.blog.163.com
# @Version : $Id$
#软件唯一ID工具
import os
import json
import time
import RSAtool
import dbTool
import hashlib
import base58
import random



class SoftKeysTool(object):
    """docstring for WXMsgTool"""
    def __init__(self,dbpth = './db/softkey'):
        super(SoftKeysTool, self).__init__()
        
        if not os.path.exists('db'):
            os.mkdir('db')
            os.mkdir(dbpth)
        
        
        self.dbPth = dbpth + os.sep + 'softkey'

        #此数据库保存用户唯一ID和用户硬件信息，操作系统信息,保存的数据只用作用户分析，不打算用来验证用户是否为注册用户,验证用户是否注册使用注册码和硬件码
        self.db = dbTool.DBMObj(self.dbPth)

    def getRandomStr(self):
        d1 = random.randint(0, 100)
        d2 = random.randint(0, 100)
        d3 = random.randint(0, 100)
        d4 = random.randint(0, 100)
        ostr = str(d1) + str(d2) + str(d3) + str(d4)
        return ostr

    #生成新的注册码
    def createSoftID(self):
        tlen = len(self.db.allKeys())
        sendtmp = str(time.time())
        strtmp = self.getRandomStr()
        tmpn = '0x' + hashlib.md5(sendtmp + strtmp + str(tlen)).hexdigest()
        num = int(tmpn,16)
        bastr = base58.b58encode_int(num)
        return bastr

    def addHardAndOSmsg(self,userhardmsg):
        nkey = self.createSoftID()
        if type(userhardmsg) == str:
            self.db.inset(nkey, userhardmsg)
        else:
            strtmp = json.dumps(userhardmsg)
            self.db.inset(nkey, strtmp)
        
    def getHardAndOsMsgWithSoftID(self,softID):
        strdat = self.db.select(softID):
        if strdat != None:
            odic = json.loads(strdat)
            return odic
        else:
            return None


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

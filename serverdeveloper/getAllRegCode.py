#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-07 09:28:00
# @Link    : http://fengmm521.blog.163.com
# @Version : $Id$
#https服务器
import os
import json
import time
import dbTool
import hashlib
import base58

class RegKeysTool(object):
    """docstring for WXMsgTool"""
    def __init__(self,dbpth = './db/regcode'):
        super(RegKeysTool, self).__init__()

        if not os.path.exists('db'):
            os.mkdir('db')

        if not os.path.exists(dbpth):
            os.mkdir(dbpth)


        #已付费注册用户
        self.dbPth = dbpth + os.sep + 'regcode'
        self.db = dbTool.DBMObj(self.dbPth)
        # self.regCodeObj = {}        #{regCode:{UUID:{硬件唯一码},os:{操作系统信息},hard:{硬件信息}}}

        #新生成的未使用注册码
        self.creagedbpth = dbpth + os.sep + 'create'
        self.createdb = dbTool.DBMObj(self.creagedbpth)


    #获取所有未使用的注册码
    def getNoAllRegCode(self):
        noregs = self.createdb.allKeys()
        return noregs

    def getAllRegCode(self):
        regs = self.db.allKeys()
        return regs
    def getData(self):
        dat = self.db.getDBDatas()
        return dat

if __name__ == '__main__':
    regtool = RegKeysTool()
    # keys = regtool.createRegistCode()
    # print(keys)
    allRegCode = regtool.getAllRegCode()
    print(allRegCode)
    dat = regtool.getData()
    print(dat)
# # 生成rsa密钥
# $ openssl genrsa -des3 -out server.key 2048
# # 去除掉密钥文件保护密码
# $ openssl rsa -in server.key -out server.key
# # 生成ca对应的csr文件
# $ openssl req -new -key server.key -out server.csr
# # 自签名
# $ openssl x509 -req -days 2048 -in server.csr -signkey server.key -out server.crt
# $ cat server.crt server.key > server.pem

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-07 09:28:00
# @Link    : http://fengmm521.blog.163.com
# @Version : $Id$
#用户下载视频网址记录
import os
import json
import time
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

        #试用用户下载目录
        self.testdbpth = dbpth + os.sep + 'testdir'
        if not os.path.exists(self.testdbpth):
            os.mkdir(self.testdbpth)

        self.testdb = dbTool.DBMObj(self.testdbpth + os.sep + 'test')

        #正式用户下载记录
        self.userpth = dbpth + os.sep + 'reguser'
        if not os.path.exists(self.userpth):
            os.mkdir(self.userpth)
        
        self.basedbPth = dbpth

        self.usrIPpth = dbpth + os.sep + 'ip'
        if not os.path.exists(self.usrIPpth):
            os.mkdir(self.usrIPpth)

        
    #用硬件码记录登陆IP地址和时间
    def addUserDBIPWithHardID(self,hardid,usrIP):
        tmpdb = dbTool.DBMObj(self.usrIPpth + os.sep + hardid)
        dictmp = {'ip':usrIP,'time':int(time.time())}
        jstr = json.dumps(dictmp)
        ks = tmpdb.allKeys()
        if ks != None and len(ks) > 100: #只记录最近100次的登陆IP地址
            keys = []
            values = []
            ks = ks[-99:]
            for i in range(len(ks)):
                keys.append(str(i+1))
                values.append(ks[i])
            keys.append('100')
            values.append(jstr)
            tmpdb.insetList(keys, values)
        else:
            if ks == None or len(ks) < 1:
                tmpdb.inset('1', jstr)
            else:
                key = len(ks) + 1
                tmpdb.inset(str(key),jstr)

    #试用用户使用硬件唯一ID保存下载的视频
    def addUserDBWithTestSoftID(self,hardID,purl):
        tusrdat = self.testdb.select(hardID)
        isTooLong = False
        if tusrdat != None:
            plist = json.loads(tusrdat)
            base64str = base64.b64encode(purl)
            plist.append(base64str)
            if len(plist) > MAXTESTCOUNT:
                isTooLong = True
                plist = plist[-5:]
                savestr = json.dumps(plist)
                self.testdb.inset(hardID, savestr)
            else:
                savestr = json.dumps(plist)
                self.testdb.inset(hardID, savestr)
        return isTooLong

    #批量保存正式用户下载URL
    def addUserListDBWithRegCode(self,hardID,purls):
        tmpdb = dbTool.DBMObj(self.userpth + os.sep + hardID)
        keys = []
        values = []
        ks = tmpdb.allKeys()
        startn = 1
        if ks != None and len(ks) > 1000: #只记录用户的最后1000个下载地址
            ks = ks[-800:]
            for i in range(len(ks)):
                keys.append(str(i + 1))
                values.append(ks[i])
            startn =  801
            for n in range(len(purls)):
                keys.append(str(startn + n))
                base64str = base64.b64encode(purls[n])
                values.append(base64str)
            tmpdb.insetList(keys, values)
            return len(keys)
        else:
            if ks == None or len(ks) < 1:
                startn = 1
            else:
                startn = len(ks) + 1
            for n in range(len(purls)):
                keys.append(str(startn + n))
                base64str = base64.b64encode(purls[n])
                values.append(base64str)
            tmpdb.insetList(keys, values)
            if ks == None:
                return len(keys)
            else:
                return len(keys) + len(ks)

    #使用硬件ID保存正式用户下载URL
    def addUserDBWithRegCode(self,hardID,purl):
        tmpdb = dbTool.DBMObj(self.userpth + os.sep + hardID)
        base64str = base64.b64encode(purl)
        ks = tmpdb.allKeys()
        if ks != None and len(ks) > 1000: #只记录用户的最后1000个下载地址
            keys = []
            values = []
            ks = ks[-800:]
            for i in range(len(ks)):
                keys.append(str(i + 1))
                values.append(ks[i])
            keys.append('801')
            values.append(base64str)
            tmpdb.insetList(keys, values)
            return len(ks) + 1
        else:
            if ks == None or len(ks) < 1:
                tmpdb.inset('1', base64str)
                return 1
            else:
                key = len(ks) + 1
                tmpdb.inset(str(key),base64str)
                return len(ks) + 1




if __name__ == '__main__':
    regtool = UserDBTool()
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

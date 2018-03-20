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


if not os.path.exists('db'):
    os.mkdir('db')

class hardKeysTool(object):
    """docstring for WXMsgTool"""
    def __init__(self,dbpth = './db/hard'):
        super(hardKeysTool, self).__init__()
        
        self.dbPth = dbpth
        if not os.path.exists(self.dbPth):
            os.mkdir(self.dbPth)

        #主板
        self.mainboarddbpth     =   self.dbPth + os.sep + 'mainboard'
        self.mainboarddb        =   dbTool.DBMObj(self.mainboarddbpth)    
        self.mainboardKeyObj    =   {}#{'hardmsg':'','regcode':'','osmsg':'','logintimes':0,'usedtimes':}     #主板编号数据对象{硬件信息,注册码,操作系统信息}

        #操作系统
        self.osIDdbpth          =   self.dbPth + os.sep + 'osID' 
        self.osIDdb             =   dbTool.DBMObj(self.osIDdbpth)   
        self.osIDKeyObj         =   {}#{'hardmsg':'','regcode':'','osmsg':''}     #操作系统唯一编号{硬件信息,注册码,操作系统信息}

        #硬盘
        self.hardDiskdbpth      =   self.dbPth + os.sep + 'harddisk' 
        self.hardDiskdb         =   dbTool.DBMObj(self.hardDiskdbpth)  
        self.hardDiskKeyObj     =   {}#{'hardmsg':'','regcode':'','osmsg':''}     #硬盘编号{硬件信息,注册码,操作系统信息}

        #网卡
        self.netCarddbpth       =   self.dbPth + os.sep + 'netcard' 
        self.netCarddb          =   dbTool.DBMObj(self.netCarddbpth) 
        self.netCardKeyObj      =   {}#{'hardmsg':'','regcode':'','osmsg':''}     #网卡MAC地址编号{硬件信息,注册码,操作系统信息}        
        
        #处理器
        self.cpudbpth           =   self.dbPth + os.sep + 'cpu' 
        self.cpudb              =   dbTool.DBMObj(self.cpudbpth) 
        self.CPUIDKeyObj        =   {}#{cpuid:{'hardmsg':'','regcode':'','osmsg':''}}     #CPU型号编码{硬件信息,注册码,操作系统信息}
        
        self.initAllOBJ()

    def initAllOBJ(self):
        self.mainboardKeyObj = self.mainboarddb.getDBDatas()
        self.osIDKeyObj = self.osIDdb.getDBDatas()
        self.hardDiskKeyObj = self.hardDiskdb.getDBDatas()
        self.netCardKeyObj = self.netCarddb.getDBDatas()
        self.CPUIDKeyObj = self.cpudb.getDBDatas()
        
    def getCPUMsgFromDB(self,cpuid):
        if cpuid in self.CPUIDKeyObj:
            return self.CPUIDKeyObj[cpuid]
        else:
            return None


    def getMainBoardMsgFromDB(self,mainboardID):
        if mainboardID in self.mainboardKeyObj:
            return self.mainboardKeyObj[mainboardID]
        else:
            return None

    def getOSIDFromDB(self,osID):
        if osID in self.osIDKeyObj:
            return self.osIDKeyObj[osID]
        else:
            return None

    def getHardDiskFromDB(self,harddiskID):
        if harddiskID in self.hardDiskKeyObj:
            return self.hardDiskKeyObj[harddiskID]
        else:
            return None

    def getNetCardFromDB(self,macaddrID):
        if macaddrID in self.netCardKeyObj:
            return self.netCardKeyObj[macaddrID]
        else:
            return None

    #从用户上传的硬件信息中获取各数据库ID
    def getIDFromUserHardMsg(self,userHardMsg):
        tmpdic = {}
        #cpu
        #mainboard
        #os
        #netcard
        #disk
        return tmpdic
    
    #为一个硬件设备数据库增加注册码
    def setResCodeWithHardMsg(self,userHardMsg,resCode):
        pass
    #查看一个硬件是否已注册过，
    #如果未注册且未登陆过，则增加一个新硬件信息，如果未注册过但已有该硬件，则登陆次数加1，并调用一次试用次数加1
    def checkHardHeaveResCode(self,userHardMsg):
        hdic = self.getIDFromUserHardMsg(userHardMsg)

    #为一个硬件增加一次使用次数,这里只作记录不作限制,限制试用次数由试用下载库对象libMangertool决定
    def addOnceUsedTimes(self,hdic):
        pass

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

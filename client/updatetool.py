#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 22:36:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os, sys
import time
import zlib

#软件更新工具
class UpdateTool(object):
    """docstring for UpdateTool"""
    def __init__(self, paytoolobj):
        super(UpdateTool, self).__init__()
        self.paytool = paytoolobj
        self.updateurl = paytoolobj.hosturl + 'update.json'            #最新版版本号
        self.version = 0                        #当前版本号
        self.updateList = []                    #要更新的文件列表


    def updateWithList(self):#更新文件
        if not os.path.exists('./tmp'):
            os.mkdir('./tmp')

        
    def getUdateFiles(self,userHardID):
        # 通过硬件码获取更新列表，
        #当用户是试用权限时，获取到的是试用版文件，
        #当用户是正式用户时将获取到不限次数文件，
        #当用户过了试期之后不会发送请求，而是提示用户购买注册码
        pass
        #下载的试用文件使用用户userHardID加特别字符串加密
        #下载的正式版文件使用userHardID和用户注册码加密



def main():

    pass
    

if __name__ == '__main__':
    main()

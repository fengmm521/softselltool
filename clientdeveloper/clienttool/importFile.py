#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import types
# import pyctest
#http://python3-cookbook.readthedocs.io/zh_CN/latest/c10/p11_load_modules_from_remote_machine_by_hooks.html

class LoadModeTool(object):
    """docstring for LoadModeTool"""
    def __init__(self, aesObj):
        super(LoadModeTool, self).__init__()
        self.aesobj = aesObj

    def loadAESModeFormEnSource(self,strEnCode,modeNmae):
        scode = self.aesobj.decrypt(strEnCode) #解密
        m = self.loadFromStrCode(scode, modeNmae)
        return m

    def saveSourceWithAESToFile(self,scode,pth):
        encode = self.aesobj.encrypt(scode)
        self.saveEnSourceToFile(encode, pth)

    def saveEnSourceToFile(self,encode,pth):
        f = open(pth,'wb')
        f.write(encode)
        f.close()

    def loadAESModeFromFile(self,fpth,modeNmae):
        if os.path.exists(fpth):
            f = open(fpth,'rb')
            endat = f.read()
            f.close()
            m = self.loadAESModeFormEnSource(endat, modeNmae)
            return m
        else:
            return None

    def loadFromStrCode(self,sourceCode,modeNmae):
        m = types.ModuleType(modeNmae)
        exec sourceCode in m.__dict__
        m = sys.modules.setdefault(modeNmae, m)
        m.__package__ = ''
        return m

    def loadModeFromFile(self,fname):

        fpth = fname + '.py'
        if os.path.exists(fpth):
            f = open(fpth,'r')
            pycode = f.read()
            f.close()
            m = types.ModuleType(modeNmae)
            exec pycode in m.__dict__
            m = sys.modules.setdefault(modeNmae, m)
            # print pyctest
            # print sys.modules['pyctest'].__name__
            # # print sys.modules['pyctest'].__file__
            # print sys.modules['pyctest'].__package__
            return m
        else:
            return None

def main():
    # print sys.modules
    # print sys.modules.keys()
    
    # print sys.modules['pyctest'].__path__
    # print sys.modules['pyctest'].__loader__
    loadtool = LoadModeTool(None)
    m = loadtool.loadModeFromFile()
    if m:
        print(m.pyctest())
        print(m.xxx)

        testobj = m.TESTObj('hahaha')
        testobj.showP()


if __name__ == '__main__':
    main()
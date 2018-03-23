#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 22:36:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

# from win32com.client import GetObject
import platform
# import sys
import os
# reload(sys)
# sys.setdefaultencoding('utf-8')

sysSystem = platform.system()


def getUUID():
    cmd = ""
    if sysSystem == 'Windows':  
        cmd = 'wmic csproduct get UUID'
    elif sysSystem == 'Darwin':
        cmd = "/usr/sbin/system_profiler SPHardwareDataType | fgrep 'UUID' | awk '{print $NF}'"
    elif sysSystem == 'Linux':
        cmd = "/usr/sbin/dmidecode -s system-uuid"
    output = os.popen(cmd)
    ostr = output.read()
    ostr = ostr.replace('\r','')
    ostrs = ostr.split('\n')
    uuid = ''
    for d in ostrs:
        tmpd = d.strip()
        if len(tmpd) < 20:
            continue
        else:
            uuid = tmpd
    return uuid

def getMacHardMsg():
    cmd = '/usr/sbin/system_profiler SPHardwareDataType'
    output = os.popen(cmd)
    ostr = output.read()
    ostrs = ostr.split('\n')
    print(ostr)
    out = {}
    for d in ostrs:
        tmpd = d.strip()
        if len(tmpd) > 1:
            tmpds = tmpd.split(':')
            if len(tmpds) > 1:
                k = tmpds[0].strip().replace(' ','_')
                v = tmpds[1].strip().replace(' ','_')
                if len(v) > 0:
                    out[k] = v
    return out

def main():
    uuid = getMacHardMsg()
    print(uuid)
if __name__ == '__main__':
    main()

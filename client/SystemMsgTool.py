#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 22:36:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os, sys
import time
import platform
import zlib
import uuidTool

#http://www.cnblogs.com/freeliver54/archive/2008/04/08/1142356.html

#http://blog.csdn.net/xtx1990/article/details/7288903 

class SystemMsgObj(object):
    """docstring for SystemMsgObj"""
    def __init__(self):
        super(SystemMsgObj, self).__init__()
        self.sysversion = platform.version()
        self.sysplatform = platform.platform()
        self.sysSystem = platform.system()
        self.ver = ''
        self.ostype = 0        #1.windows,2.mac,3.linux
        if self.sysSystem == 'Windows':  #mac系统
            self.ostype = 1        #1.windows,2.mac,3.linux
            self.ver = platform.win32_ver()
        elif self.sysSystem == 'Darwin':
            self.ostype = 2
            self.ver = platform.mac_ver()
            
        elif self.sysSystem == 'Linux':
            self.ostype = 3
            self.ver = platform.linux_distribution()
        self.c = None
        self.sysMsg = {}
        osMsg = {}
        osMsg['osversion'] = str(self.sysversion)
        osMsg['osplatform'] = str(self.sysplatform)
        osMsg['os'] = str(self.sysSystem)
        osMsg['ver'] = self.ver
        self.sysMsg['os'] = osMsg
        self.sysMsg['ostype'] = self.ostype
        if self.ostype == 1:
            import wmi
            self.c = wmi.WMI()
            self.initWinSystemHardMsg()
            self._winMachineGuid()
        elif self.ostype == 2:
            self.initMacSystemHardMsg()
        elif self.ostype == 3:
            self.initLinuxSystemHardMsg()
        
        self.getUserHardID()
    def initWinSystemHardMsg(self):
        hardmsg = {}
        hardmsg['cpu'] = self._printCPU()
        hardmsg['mainboard'] = self._printMain_board()
        hardmsg['BIOS'] = self._printBIOS()
        hardmsg['disk'] = self._printDisk()
        hardmsg['memory'] = self._printPhysicalMemory()
        hardmsg['battery'] = self._printBattery()
        hardmsg['MacAddr'] = self._printMacAddress()
        self.sysMsg['hard'] = hardmsg
        self.getUserHardID()
        return self.sysMsg
    def initMacSystemHardMsg(self):
        self.sysMsg['hard'] = self.getMacHardMsg()

    def getMacHardMsg(self):
        #/usr/sbin/system_profiler SPHardwareDataType
        cmd = '/usr/sbin/system_profiler SPHardwareDataType'
        output = os.popen(cmd)
        ostr = output.read()
        ostrs = ostr.split('\n')
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
    def initLinuxSystemHardMsg(self):
        pass
    def getSysMsg(self):
        return self.sysMsg
    def getUserHardID(self):
        self.sysMsg['userHardID'] = uuidTool.getUUID()

    #处理器
    def _printCPU(self):
        tmpdict = {}
        tmpdict["CpuCores"] = 0
        for cpu in self.c.Win32_Processor():     
            tmpdict["cpuid"] = str(cpu.ProcessorId).strip()
            tmpdict["CpuType"] = cpu.Name
            tmpdict['systemName'] = cpu.SystemName
            try:
                tmpdict["CpuCores"] = cpu.NumberOfCores
            except:
                tmpdict["CpuCores"] += 1
            tmpdict["CpuClock"] = cpu.MaxClockSpeed 
            tmpdict['DataWidth'] = cpu.DataWidth
        # print tmpdict
        return  tmpdict

    #主板
    def _printMain_board(self):
        boards = []
        # print len(c.Win32_BaseBoard()):
        for board_id in self.c.Win32_BaseBoard():
            tmpmsg = {}
            tmpmsg['UUID'] = board_id.qualifiers['UUID'][1:-1]   #主板UUID,有的主板这部分信息取到为空值，ffffff-ffffff这样的
            tmpmsg['SerialNumber'] = board_id.SerialNumber                #主板序列号
            tmpmsg['Manufacturer'] = board_id.Manufacturer       #主板生产品牌厂家
            tmpmsg['Product'] = board_id.Product                 #主板型号
            boards.append(tmpmsg)
        # print boards
        return boards

    #BIOS
    def _printBIOS(self):
        bioss = []
        for bios_id in self.c.Win32_BIOS():
            tmpmsg = {}
            tmpmsg['BiosCharacteristics'] = bios_id.BiosCharacteristics   #BIOS特征码
            tmpmsg['version'] = bios_id.Version                           #BIOS版本
            tmpmsg['Manufacturer'] = bios_id.Manufacturer.strip()                 #BIOS固件生产厂家
            tmpmsg['ReleaseDate'] = bios_id.ReleaseDate                   #BIOS释放日期
            tmpmsg['SMBIOSBIOSVersion'] = bios_id.SMBIOSBIOSVersion       #系统管理规范版本
            bioss.append(tmpmsg)
        # print bioss
        return bioss

    #硬盘
    def _printDisk(self):
        disks = []
        for disk in self.c.Win32_DiskDrive():
            # print disk.__dict__
            tmpmsg = {}
            tmpmsg['SerialNumber'] = disk.SerialNumber.strip()
            tmpmsg['DeviceID'] = disk.DeviceID
            tmpmsg['Caption'] = disk.Caption
            tmpmsg['Size'] = disk.Size
            tmpmsg['UUID'] = disk.qualifiers['UUID'][1:-1]
            disks.append(tmpmsg)
        # for d in disks:
        #     print d
        return disks

    #内存
    def _printPhysicalMemory(self):
        memorys = []
        for mem in self.c.Win32_PhysicalMemory():
            tmpmsg = {}
            tmpmsg['UUID'] = mem.qualifiers['UUID'][1:-1]
            tmpmsg['BankLabel'] = mem.BankLabel
            tmpmsg['SerialNumber'] = mem.SerialNumber.strip()
            tmpmsg['ConfiguredClockSpeed'] = mem.ConfiguredClockSpeed
            tmpmsg['Capacity'] = mem.Capacity
            tmpmsg['ConfiguredVoltage'] = mem.ConfiguredVoltage
            memorys.append(tmpmsg)
        # for m in memorys:
        #     print m
        return memorys

    #电池信息，只有笔记本才会有电池选项
    def _printBattery(self):
        isBatterys = False
        for b in self.c.Win32_Battery():
            isBatterys = True
        return isBatterys

    #网卡mac地址：
    def _printMacAddress(self):
        macs = []
        for n in  self.c.Win32_NetworkAdapter():
            mactmp = n.MACAddress
            if mactmp and len(mactmp.strip()) > 5:
                tmpmsg = {}
                tmpmsg['MACAddress'] = n.MACAddress
                tmpmsg['Name'] = n.Name
                tmpmsg['DeviceID'] = n.DeviceID
                tmpmsg['AdapterType'] = n.AdapterType
                tmpmsg['Speed'] = n.Speed
                macs.append(tmpmsg)
        # print macs
        return macs
    def _winMachineGuid(self):
        import _winreg
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Cryptography",0,_winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)
        result = _winreg.QueryValueEx(key, "MachineGuid")
        self.sysMsg['machineGuid'] = result[0].lower()

ostmp = SystemMsgObj()

def getHardMsg():
    return ostmp.getSysMsg()

    
def main():
    import json
    ostmp = SystemMsgObj()
    osmsg = ostmp.getSysMsg()
    # print osmsg
    jstr = json.dumps(osmsg)
    print(jstr)
    #{"osplatform": "Windows-10-10.0.16299", "disk": [{"Caption": "WDC WD10EZEX-08WN4A0", "SerialNumber": "WD-WCC6Y5KN9ZJT", "UUID": "8502C4B2-5FBB-11D2-AAC1-006008C78BC7", "DeviceID": "\\\\.\\PHYSICALDRIVE0", "Size": "1000202273280"}, {"Caption": "SAMSUNG MZNTY128HDHP-00000", "SerialNumber": "S2YMNY0J782472", "UUID": "8502C4B2-5FBB-11D2-AAC1-006008C78BC7", "DeviceID": "\\\\.\\PHYSICALDRIVE1", "Size": "128034708480"}], "ver": ["10", "10.0.16299", "", "Multiprocessor Free"], "mainboard": [{"Product": "Z270 KRAIT GAMING (MS-7A59)", "SerialNumber": "H316560067", "UUID": "FAF76B95-798C-11D2-AAD1-006008C78BC7", "Manufacturer": "MSI"}], "BIOS": [{"ReleaseDate": "20170207000000.000000+000", "version": "ALASKA - 1072009", "SMBIOSBIOSVersion": "A.40", "BiosCharacteristics": [7, 11, 12, 15, 16, 17, 19, 23, 24, 25, 26, 27, 28, 29, 32, 33, 40, 42, 43], "Manufacturer": "American Megatrends Inc."}], "userHardID": "", "MacAddr": [{"MACAddress": "4C:CC:6A:FB:A3:6C", "Speed": "100000000", "Name": "Intel(R) Ethernet Connection (2) I219-V", "AdapterType": "\u4ee5\u592a\u7f51 802.3", "DeviceID": "1"}], "memory": [{"ConfiguredVoltage": 1200, "Capacity": "8589934592", "UUID": "FAF76B93-798C-11D2-AAD1-006008C78BC7", "ConfiguredClockSpeed": 2400, "SerialNumber": "03980200", "BankLabel": "BANK 1"}, {"ConfiguredVoltage": 1200, "Capacity": "8589934592", "UUID": "FAF76B93-798C-11D2-AAD1-006008C78BC7", "ConfiguredClockSpeed": 2400, "SerialNumber": "A1860200", "BankLabel": "BANK 3"}], "ostype": 1, "osversion": "10.0.16299", "os": "Windows", "cpu": {"CpuClock": 3408, "CpuCores": 4, "systemName": "SC-201710151616", "DataWidth": 64, "cpuid": "BFEBFBFF000906E9", "CpuType": "Intel(R) Core(TM) i5-7500 CPU @ 3.40GHz"}, "battery": false, "machineGuid": "86ce2b8f-f614-4656-9e5d-ff7208f2f0c6"}

if __name__ == '__main__':
    main()

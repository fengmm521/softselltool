#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 22:36:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os, sys
import time
import wmi,zlib

#http://www.cnblogs.com/freeliver54/archive/2008/04/08/1142356.html

#http://blog.csdn.net/xtx1990/article/details/7288903 

def get_cpu_info() :
    tmpdict = {}
    tmpdict["CpuCores"] = 0
    c = wmi.WMI()
#   print c.Win32_Processor().['ProcessorId']
#   print c.Win32_DiskDrive()
    for cpu in c.Win32_Processor():     
        # print cpu
        tmpdict["cpuid"] = cpu.ProcessorId.strip()
        tmpdict["CpuType"] = cpu.Name
        try:
            tmpdict["CpuCores"] = cpu.NumberOfCores
        except:
            tmpdict["CpuCores"] += 1
            tmpdict["CpuClock"] = cpu.MaxClockSpeed 
    return tmpdict
def get_disk_info():
    tmplist = []
    encrypt_str = ""
    c = wmi.WMI ()
    for cpu in c.Win32_Processor():

#cpu 序列号
        encrypt_str = encrypt_str+cpu.ProcessorId.strip()
        print "cpu id:", cpu.ProcessorId.strip()
    for physical_disk in c.Win32_DiskDrive():
        encrypt_str = encrypt_str+physical_disk.SerialNumber.strip()

#硬盘序列号
        print 'disk id:', physical_disk.SerialNumber.strip()
        tmpdict = {}
        tmpdict["Caption"] = physical_disk.Caption
        tmpdict["Size"] = long(physical_disk.Size)/1000/1000/1000
        tmplist.append(tmpdict)
    for board_id in c.Win32_BaseBoard():

#主板序列号
        encrypt_str = encrypt_str+board_id.SerialNumber.strip()
        print "main board id:",board_id.SerialNumber.strip()
    for mac in c.Win32_NetworkAdapter():

#mac 地址（包括虚拟机的）
        print "mac addr:", mac.MACAddress
    for bios_id in c.Win32_BIOS():

#bios 序列号
        encrypt_str = encrypt_str+bios_id.SerialNumber.strip()
        print "bios number:", bios_id.SerialNumber.strip()
    print "encrypt_str:", encrypt_str

#加密算法
    print zlib.adler32(encrypt_str)
    return encrypt_str 

c = wmi.WMI()
#处理器
def printCPU():
    tmpdict = {}
    tmpdict["CpuCores"] = 0
    for cpu in c.Win32_Processor():     
        tmpdict["cpuid"] = cpu.ProcessorId.strip()
        tmpdict["CpuType"] = cpu.Name
        tmpdict['systemName'] = cpu.SystemName
        try:
            tmpdict["CpuCores"] = cpu.NumberOfCores
        except:
            tmpdict["CpuCores"] += 1
        tmpdict["CpuClock"] = cpu.MaxClockSpeed 
        tmpdict['DataWidth'] = cpu.DataWidth
    print tmpdict
    return  tmpdict

#主板
def printMain_board():
    boards = []
    # print len(c.Win32_BaseBoard()):
    for board_id in c.Win32_BaseBoard():
        tmpmsg = {}
        tmpmsg['UUID'] = board_id.qualifiers['UUID'][1:-1]   #主板UUID,有的主板这部分信息取到为空值，ffffff-ffffff这样的
        tmpmsg['SerialNumber'] = board_id.SerialNumber                #主板序列号
        tmpmsg['Manufacturer'] = board_id.Manufacturer       #主板生产品牌厂家
        tmpmsg['Product'] = board_id.Product                 #主板型号
        boards.append(tmpmsg)
    print boards
    return boards

#BIOS
def printBIOS():
    bioss = []
    for bios_id in c.Win32_BIOS():
        tmpmsg = {}
        tmpmsg['BiosCharacteristics'] = bios_id.BiosCharacteristics   #BIOS特征码
        tmpmsg['version'] = bios_id.Version                           #BIOS版本
        tmpmsg['Manufacturer'] = bios_id.Manufacturer.strip()                 #BIOS固件生产厂家
        tmpmsg['ReleaseDate'] = bios_id.ReleaseDate                   #BIOS释放日期
        tmpmsg['SMBIOSBIOSVersion'] = bios_id.SMBIOSBIOSVersion       #系统管理规范版本
        bioss.append(tmpmsg)
    print bioss
    return bioss

#硬盘
def printDisk():
    disks = []
    for disk in c.Win32_DiskDrive():
        # print disk.__dict__
        tmpmsg = {}
        tmpmsg['SerialNumber'] = disk.SerialNumber.strip()
        tmpmsg['DeviceID'] = disk.DeviceID
        tmpmsg['Caption'] = disk.Caption
        tmpmsg['Size'] = disk.Size
        tmpmsg['UUID'] = disk.qualifiers['UUID'][1:-1]
        disks.append(tmpmsg)
    for d in disks:
        print d
    return disks

#内存
def printPhysicalMemory():
    memorys = []
    for mem in c.Win32_PhysicalMemory():
        tmpmsg = {}
        tmpmsg['UUID'] = mem.qualifiers['UUID'][1:-1]
        tmpmsg['BankLabel'] = mem.BankLabel
        tmpmsg['SerialNumber'] = mem.SerialNumber.strip()
        tmpmsg['ConfiguredClockSpeed'] = mem.ConfiguredClockSpeed
        tmpmsg['Capacity'] = mem.Capacity
        tmpmsg['ConfiguredVoltage'] = mem.ConfiguredVoltage
        memorys.append(tmpmsg)
    for m in memorys:
        print m
    return memorys

#电池信息，只有笔记本才会有电池选项
def printBattery():
    isBatterys = False
    for b in c.Win32_Battery():
        isBatterys = True
    return isBatterys

#网卡mac地址：
def printMacAddress():
    macs = []
    for n in  c.Win32_NetworkAdapter():
        mactmp = n.MACAddress
        if mactmp and len(mactmp.strip()) > 5:
            tmpmsg = {}
            tmpmsg['MACAddress'] = n.MACAddress
            tmpmsg['Name'] = n.Name
            tmpmsg['DeviceID'] = n.DeviceID
            tmpmsg['AdapterType'] = n.AdapterType
            tmpmsg['Speed'] = n.Speed
            macs.append(tmpmsg)
    print macs
    return macs

def main():

    printCPU()
    printMain_board()
    printBIOS()
    printDisk()
    printPhysicalMemory()
    printMacAddress()
    print printBattery()
    

if __name__ == '__main__':
    main()

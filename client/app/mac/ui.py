# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep 12 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################


import os
import sys
import wx

###########################################################################
## Class MyFrame1
###########################################################################
import downtool

import threading

import Queue

reload(sys)
sys.setdefaultencoding( "utf-8" )

class WorkerThread(threading.Thread):
    """
    This just simulates some long-running task that periodically sends
    a message to the GUI thread.
    """
    def __init__(self, window,downstr):
        threading.Thread.__init__(self)
        self.window = window
        self.liststr = downstr
        self.savePth = window.savePth
        self.countCallBack = window.countCallBack

    def stop(self):
        pass

    def run(self):

        # downtool.downLoadWithStrList(self.liststr, self.countCallBack,self.savePth)
        try:
            downtool.downLoadWithStrList(self.liststr, self.countCallBack,self.savePth)
        except Exception as e:
            self.window.showMsg('下载视频时出错\n')
            self.window.showMsg('%s\n'%(str(e)))
        self.window.downthread = None


class UITool ( wx.Frame ):
    def __init__( self, parent  = None):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,630 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.savePth = downtool.get_desktop()

        downtool.msgtool.setUIObj(self)

        self.count = 0
        self.gaugeValueStart = 0

        self.savepthconfig = 'savepth.txt'
        if os.path.exists(self.savepthconfig):
            f = open(self.savepthconfig,'r')
            self.savePth = f.read()
            f.close()

        self.isWinSystem = downtool.isWinSystem

        self.queue = Queue.Queue()
            


        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"youtube下载工具,本工具来源,https://fengmm521.taobao.com/" ), wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"在下边输入要下载的视频网址,每个视频一行", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        sbSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 760,200 ), style=wx.TE_MULTILINE )
        sbSizer1.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
        
        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"下载文件保存路径:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        sbSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )
        
        self.m_button3 = wx.Button( self, wx.ID_ANY, u"选择保存路径", wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer1.Add( self.m_button3, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.onSavePathSelectClick, self.m_button3)
        
        self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,-1 ), 0 )
        sbSizer1.Add( self.m_textCtrl3, 1, wx.BOTTOM|wx.LEFT, 5 )
        self.m_textCtrl3.SetLabel(self.savePth)
        
        self.m_button2 = wx.Button( self, wx.ID_ANY, u"开始下载", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        sbSizer1.Add( self.m_button2, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.onDownloadClick, self.m_button2)
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"下载进度与祥情:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        sbSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )
        
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"1/100", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        sbSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )
        self.m_staticText3.SetLabel('请输入视频网址后，点开始下载')
        
        self.m_gauge1 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 750,-1 ), wx.GA_HORIZONTAL )
        self.m_gauge1.SetValue( 1 ) 
        sbSizer1.Add( self.m_gauge1, 0, wx.ALL, 5 )
        
        self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 760,98 ), style=wx.TE_MULTILINE )
        sbSizer1.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
        
        self.SetSizer( sbSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )

        
        self.showtimer = 0
        self.showTishi = ''


        self.videotmppth = ''
        self.audiotmppth = ''
        # self.Bind(wx.EVT_IDLE, self.OnIdle)


        # 创建定时器  
        self.timer = wx.Timer(self)#创建定时器  
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)#绑定一个定时器事件 
        self.startTimer(30)
    
        self.downthread = None

        self.isComplet = False

        self.Bind(wx.EVT_CLOSE,  self.OnCloseWindow)

    def __del__( self ):
        pass

    def OnCloseWindow(self, evt):
        self.stopDownloadThread()
        self.Destroy()

    def stopDownloadThread(self):
        if self.downthread:
            self.downthread.stop()
            self.downthread = None

    def onTimer(self, event):
        if not self.queue.empty():
            msgobj = self.queue.get_nowait()
            self.showMsg(msgobj.data)
        if self.isComplet:
            self.showTishi = '所有视频已下载完成'
            return
        self.count = self.count + 1
        if self.count >= 99:
            self.count = self.gaugeValueStart
        if self.gaugeValueStart == 0:
            self.m_gauge1.SetValue(0)
        else:
            self.m_gauge1.SetValue(self.count)
        self.showtimer += 1
        if self.gaugeValueStart == 0:
            self.showTishi = '请输入视频网址后，点开始下载'
        elif self.gaugeValueStart == 1:
            self.showTishi = '正在解析视频信息'
        elif self.gaugeValueStart == 50:
            self.showTishi = '正在下载视频'
        elif self.gaugeValueStart == 20:
            self.showTishi = '正在下载音频'
        elif self.gaugeValueStart == 90:
            self.showTishi = '正在合成音视频'
        if self.showtimer == 30:
            outstr = self.getDownloadFileSize()
            if outstr != '...':
                outtishi = self.showTishi + ',已下载' + outstr
                self.m_staticText3.SetLabel(outtishi)
            else:
                outtishi = self.showTishi + outstr
                self.m_staticText3.SetLabel(outtishi)
        if self.showtimer > 30:
            self.showtimer = 0

    def getDownloadFileSize(self):
        outstr = ''
        if self.gaugeValueStart == 50 and os.path.exists(self.videotmppth): #正在下载视频

            outstr = os.path.getsize(self.videotmppth)
            if outstr > 1024*1024: #m
                outstr = '%.2f'%(outstr/(1024*1024.0)) + 'mb'
            elif outstr > 1024:    #k
                outstr = '%.2f'%(outstr/(1024.0)) + 'kb'
            else:
                outstr = str(outstr) + 'byte'

        elif self.gaugeValueStart == 20 and os.path.exists(self.audiotmppth): #正在下载音频
            outstr = os.path.getsize(self.audiotmppth)
            if outstr > 1024*1024: #m
                outstr = '%.2f'%(outstr/(1024*1024.0)) + 'mb'
            elif outstr > 1024:    #k
                outstr = '%.2f'%(outstr/(1024.0)) + 'kb'
            else:
                outstr = str(outstr) + 'byte'

        else:
            outstr = '...'
        return outstr


    # Virtual event handlers, overide them in your derived class  
    def startTimer( self, value ):  
        self.timer.Start(value)#设定时间间隔为1000毫秒,并启动定时器  
        #     self.timer.Stop()  

    def showDownStart(self):
        self.gaugeValueStart = 1

    def showDownVideo(self,pth):
        self.videotmppth = pth
        self.gaugeValueStart = 50
        

    def showDownAudio(self,pth):
        self.audiotmppth = pth
        self.gaugeValueStart = 20

    def makeVideoAndAudio(self):
        self.gaugeValueStart = 90

    def downLoadComplet(self):
        self.isComplet = True
        self.m_gauge1.SetValue(0)
        self.m_staticText3.SetLabel('所有视频已下载完成')
        self.showMsg('所有视频已下载完成\n')

        if downtool.isWinSystem:
            os.startfile(self.savePth)
        elif downtool.sysplatform == 'Darwin':
            cmd = 'open %s'%(self.savePth)
            os.system(cmd)
        else:
            cmd = 'xdg-open %s'%(self.savePth)
            os.system(cmd)

    def updateSavePth(self):
        self.m_textCtrl3.SetLabel(self.savePth)
        f = open(self.savepthconfig,'w')
        f.write(self.savePth)
        f.close()

    def onSavePathSelectClick(self,event):
        dlg = wx.DirDialog(self,u"选择文件夹",style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.savePth = dlg.GetPath() #文件夹路径
            self.updateSavePth()
        dlg.Destroy()

    def countCallBack(self,pstr):
        outstr = '下载进度与祥情:' + pstr
        self.m_staticText2.SetLabel(outstr)

    def onDownloadClick(self,event):
        self.isComplet = False
        liststr = self.m_textCtrl1.GetValue()
        if not self.downthread:
            self.downthread = WorkerThread(self,liststr)
            self.downthread.setDaemon(True)
            self.downthread.start()
        else:
            self.m_staticText3.SetLabel('视频下载正在运行中...')
            self.showMsg('视频下载正在运行中...\n')
        
    def showMsg(self,msg):
        # self.m_textCtrl2.AppendText(msg)
        # print msg
        # print msg
        self.m_textCtrl2.SetInsertionPointEnd()
        if self.isWinSystem:
            # msgtmp = msg.decode('utf-8').encode('ISO-8859-1')
            self.m_textCtrl2.WriteText(msg)
        else:
            self.m_textCtrl2.WriteText(msg)



    
if __name__ == '__main__':  
    app = wx.PySimpleApp()  
    frame = UITool()  
    frame.Show()  
    app.MainLoop()  

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
# import downtool

import threading

import Queue

import time

# import clientRegTool

import updatetool

import NetWorkTest

import pytube



reload(sys)
sys.setdefaultencoding( "utf-8" )

class WorkerThread(threading.Thread):
    """
    This just simulates some long-running task that periodically sends
    a message to the GUI thread.
    """
    def __init__(self, window,downstr,pdowntool):
        threading.Thread.__init__(self)
        self.window = window
        self.liststr = downstr
        self.savePth = window.savePth
        self.countCallBack = window.countCallBack
        self.downtool = pdowntool

    def stop(self):
        pass

    def run(self):

        # downtool.downLoadWithStrList(self.liststr, self.countCallBack,self.savePth)
        try:
            self.downtool.downLoadWithStrList(self.liststr, self.countCallBack,self.savePth)
        except Exception as e:
            self.window.showMsg('下载视频时出错\n')
            self.window.showMsg('%s\n'%(str(e)))
        self.window.downthread = None
#https://www.youtube.com/watch?v=_kuRepI2D6A

ISDEBUG = False

class UITool ( wx.Frame ):

    def initClient(self):
        self.showMsg('初始化客户端')
        self.showMsg('检测访问国内网络。。。\n')
        self.isOKChina = NetWorkTest.isNetChainOK()
        if self.isOKChina:
            self.showMsg('访问国内正常\n')
        else:
            self.showMsg('网络出现故障\n')
        self.showMsg('检测是否可访问谷歌。。。\n')
        self.isOKGoogle = NetWorkTest.isNetUSAOK()
        if self.isOKGoogle:
            self.showMsg('访问谷歌正常\n')
        else:
            self.showMsg('网络出现故障\n')
        self.showMsg('检测是否可访问youtube视频网站。。。\n')
        self.isOKYoutube = NetWorkTest.isNetYouTubeOK()
        if self.isOKYoutube:
            self.showMsg('访问youtube网站正常,软件可正常使用,\n')
        else:
            self.showMsg('访问youtube网站错误,软件下载视频需要可以访问视频网站\n')

    def __init__( self, parent  = None):
        # wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,630 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,630 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.isOKGoogle = False

        self.isOKChina = False

        self.isOKYoutube = False

        try:
        # if True:
            self.updateObj = updatetool.UpdateTool(isDebug = ISDEBUG)

            # self.clientRegObj = clientRegTool.ClientRegTool(isDebug = True)
            clientRegTool = self.updateObj.getClientRegTool()
            self.clientRegObj = clientRegTool.ClientRegTool(isDebug = ISDEBUG)

            self.downcount = self.clientRegObj.getDownCount()
            

            self.downtool = self.clientRegObj.getDownTool()
            trailback = None
            if self.downtool == None:
                trailback = self.clientRegObj.trail(isGetCode = True)
                self.downtool = self.clientRegObj.getDownTool()
            else:
                if self.downtool.isTrailCode != self.clientRegObj.isTrail:
                    trailback = self.clientRegObj.trail(isGetCode = True)
                else:
                    trailback = self.clientRegObj.trail()

            self.isShowTrail = False
            if trailback['erro'] == 1:#目前是试用状态
                self.isShowTrail = True

            self.savePth = self.downtool.get_desktop()

            self.downtool.msgtool.setUIObj(self)

            self.isWinSystem = self.downtool.isWinSystem

        except Exception as e:
            self.savePth = ''
            self.isShowTrail = False

        print(os.getcwd())

        self.count = 0
        self.gaugeValueStart = 0

        self.savepthconfig = 'savepth.txt'
        if os.path.exists(self.savepthconfig):
            f = open(self.savepthconfig,'r')
            self.savePth = f.read()
            f.close()

        

        self.queue = Queue.Queue()
            


        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
        
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"youtube下载工具,本工具来源,https://fengmm521.taobao.com/" ), wx.VERTICAL )
        
        # self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"在下边输入要下载的视频网址,每个视频一行", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        # self.m_staticText1.Wrap( -1 )
        # sbSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"在下边输入要下载的视频网址,每个视频一行,试用版最多可下载五个视频，注册版没有限制。", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        sbSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 760,200 ), style=wx.TE_MULTILINE )
        sbSizer1.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
        
        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"下载文件保存路径:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        sbSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )


        #------------------
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,-1 ), 0 )
        gbSizer1.Add( self.m_textCtrl3, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.m_textCtrl3.SetLabel(self.savePth)

        #------------------
        
        # self.m_button3 = wx.Button( self, wx.ID_ANY, u"选择保存路径", wx.DefaultPosition, wx.DefaultSize, 0 )
        # sbSizer1.Add( self.m_button3, 0, wx.ALL, 5 )
        
        self.m_button3 = wx.Button( self, wx.ID_ANY, u"选择保存路径", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer1.Add( self.m_button3, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.onSavePathSelectClick, self.m_button3)
        
        # self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,-1 ), 0 )
        # sbSizer1.Add( self.m_textCtrl3, 1, wx.BOTTOM|wx.LEFT, 5 )
        # self.m_textCtrl3.SetLabel(self.savePth)

        #---------------
        sbSizer1.Add( gbSizer1, 0, 0, 5 )

        gSizer1 = wx.GridSizer( 2, 2, 0, 0 )

        gbSizer2 = wx.GridBagSizer( 0, 0 )
        gbSizer2.SetFlexibleDirection( wx.BOTH )
        gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        #---------------
        
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"1/100", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        gbSizer2.Add( self.m_staticText3, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.m_staticText3.SetLabel('请输入视频网址后，点开始下载')

        # self.m_button2 = wx.Button( self, wx.ID_ANY, u"开始下载", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        # sbSizer1.Add( self.m_button2, 0, wx.ALL, 5 )
        self.m_button2 = wx.Button( self, wx.ID_ANY, u"开始下载", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        gbSizer2.Add( self.m_button2, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.onDownloadClick, self.m_button2)
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"下载进度与祥情:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        gbSizer2.Add( self.m_staticText2, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        # sbSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )
        
        # self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"1/100", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        # self.m_staticText3.Wrap( -1 )
        # sbSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )
        # self.m_staticText3.SetLabel('请输入视频网址后，点开始下载')
        
        #-----------------
        gSizer1.Add( gbSizer2, 1, wx.EXPAND, 5 )
        
        gbSizer4 = wx.GridBagSizer( 0, 0 )
        gbSizer4.SetFlexibleDirection( wx.BOTH )
        gbSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        # imagpth = u"data" + os.sep + "image.png"
        self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"data/image.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer4.Add( self.m_bitmap1, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_buyTextTitle = wx.StaticText( self, wx.ID_ANY, u"扫二维码购买注册码永久使用", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_buyTextTitle.Wrap( -1 )
        bSizer1.Add( self.m_buyTextTitle, 1, wx.ALL, 5 )

        self.m_buyTextTitle1 = wx.StaticText( self, wx.ID_ANY, u"支持微信,支付宝购买", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.m_buyTextTitle1.Wrap( -1 )
        self.m_buyTextTitle1.SetForegroundColour( wx.Colour( 177, 255, 221 ) )

        bSizer1.Add( self.m_buyTextTitle1, 0, wx.ALL, 5 )

        self.m_textCtrl4 = wx.TextCtrl( self, wx.ID_ANY, u"请输入注册码", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl4.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        
        bSizer1.Add( self.m_textCtrl4, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_regbtn = wx.Button( self, wx.ID_ANY, u"注册", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_regbtn, 0, wx.ALL, 5 )
        def regBtnFunc(evt):
            tmpmsg,isOK = self.clientRegObj.bind(self.m_textCtrl4.GetValue())
            self.isShowTrail = bool(isOK)
            if not self.isShowTrail:
                self.hideTrailUI()
            self.showMsg(tmpmsg)

        self.Bind(wx.EVT_BUTTON,regBtnFunc, self.m_regbtn)

        gbSizer4.Add( bSizer1, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"剩余试用数:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        self.m_staticText7.SetForegroundColour( wx.Colour( 254, 217, 204 ) )
        
        bSizer2.Add( self.m_staticText7, 0, wx.ALL, 5 )

        lcount = str(max(5-self.downcount, 0))
        self.m_tailSticTxt = wx.StaticText( self, wx.ID_ANY, lcount, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_tailSticTxt.Wrap( -1 )
        self.m_tailSticTxt.SetFont( wx.Font( 40, 70, 90, 90, False, wx.EmptyString ) )
        self.m_tailSticTxt.SetForegroundColour( wx.Colour( 137, 255, 128 ) )
        
        bSizer2.Add( self.m_tailSticTxt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        gbSizer4.Add( bSizer2, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
        
        gSizer1.Add( gbSizer4, 1, wx.EXPAND, 5 )
        
        sbSizer1.Add( gSizer1, 1, wx.EXPAND, 5 )


        #-----------------



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

        self.showMsg('程序正在加载下载模块...\n')

        if self.isShowTrail:
            self.showTrailUI()
        else:
            self.hideTrailUI()
        self.showMsg('所有模块加载完成！\n')

        self.initClient()

    def __del__( self ):
        pass

    def showTrailUI(self):
        self.m_bitmap1.Enable()
        self.m_bitmap1.Show()
        self.m_buyTextTitle.Enable()
        self.m_buyTextTitle.Show()
        self.m_buyTextTitle1.Enable()
        self.m_buyTextTitle1.Show()
        self.m_textCtrl4.Enable()
        self.m_textCtrl4.Show()
        self.m_regbtn.Enable()
        self.m_regbtn.Show()
        self.m_staticText7.Enable()
        self.m_staticText7.Show()
        self.m_tailSticTxt.Enable()
        self.m_tailSticTxt.Show()


    def hideTrailUI(self):
        self.m_bitmap1.Hide()
        self.m_buyTextTitle.Hide()
        self.m_buyTextTitle1.Hide()
        self.m_textCtrl4.Hide()
        self.m_regbtn.Hide()
        self.m_staticText7.Hide()
        self.m_tailSticTxt.Hide()

        self.m_bitmap1.Disable()
        self.m_buyTextTitle.Disable()
        self.m_buyTextTitle1.Disable()
        self.m_textCtrl4.Disable()
        self.m_regbtn.Disable()
        self.m_staticText7.Disable()
        self.m_tailSticTxt.Disable()
        

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

        if self.downtool.isWinSystem:
            os.startfile(self.savePth)
        elif self.downtool.sysplatform == 'Darwin':
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

    def splitDownURLs(self,strurls):
        lines = strurls.split('\n')
        turls = []
        for l in lines:
            ltmp = l.replace('\r','')
            ltmp = ltmp.replace('\n','')
            if len(ltmp) > 10 and (ltmp[:7] == 'http://' or ltmp[:8]) == 'https://':
                turls.append(ltmp)
        count = len(turls)
        return count,turls

    def updateTrailCount(self,count):
        if self.isShowTrail:
            self.m_tailSticTxt.SetLabel(str(count))

    def onDownloadClick(self,event):
        self.isComplet = False
        liststr = self.m_textCtrl1.GetValue()
        dcount,urls = self.splitDownURLs(liststr)
        if not urls:
            return
        if self.isShowTrail and (dcount > 5 or self.downcount > 5):
                self.updateTrailCount(0)
                self.showMsg('已达最大试用次数，请购买注册码注册本软件！\n')
        else:
            isErro,scount = self.clientRegObj.sendURLMsg(urls)
            self.downcount = scount
            if isErro:
                if scount > 5:
                    self.updateTrailCount(0)
                    self.showMsg('已经达到最大试用次数，请购买注册码注册本软件！\n')
                else:
                    lcount = max(5 - scount, 0)
                    self.updateTrailCount(lcount)
                    tmpmsg = '还可以试下载%d个视频，注册后可永久使用.\n'%(lcount)
                    self.showMsg(tmpmsg)
                    if not self.downthread:
                        self.downthread = WorkerThread(self,liststr,self.downtool)
                        self.downthread.setDaemon(True)
                        self.downthread.start()
                    else:
                        self.m_staticText3.SetLabel('视频下载正在运行中...')
                        self.showMsg('视频下载正在运行中...\n')
            else:
                if not self.downthread:
                    self.downthread = WorkerThread(self,liststr,self.downtool)
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

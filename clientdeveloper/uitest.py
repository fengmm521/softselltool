# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep 12 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 791,598 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
        
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"youtube下载工具,其他小软件请留意.http://fengmm521.taobao.com" ), wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"在下边输入要下载的视频网址,每个视频一行,试用版最多可下载五个视频，注册版没有限制。", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        sbSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 760,200 ), 0 )
        sbSizer1.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
        
        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"下载文件保存路径:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        sbSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )
        
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,-1 ), 0 )
        gbSizer1.Add( self.m_textCtrl3, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        self.m_button3 = wx.Button( self, wx.ID_ANY, u"选择保存路径", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer1.Add( self.m_button3, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        sbSizer1.Add( gbSizer1, 0, 0, 5 )
        
        gSizer1 = wx.GridSizer( 2, 2, 0, 0 )
        
        gbSizer2 = wx.GridBagSizer( 0, 0 )
        gbSizer2.SetFlexibleDirection( wx.BOTH )
        gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"1/100", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        gbSizer2.Add( self.m_staticText3, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        self.m_button2 = wx.Button( self, wx.ID_ANY, u"开始下载", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        gbSizer2.Add( self.m_button2, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"下载进度与祥情:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        gbSizer2.Add( self.m_staticText2, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        gSizer1.Add( gbSizer2, 1, wx.EXPAND, 5 )
        
        gbSizer4 = wx.GridBagSizer( 0, 0 )
        gbSizer4.SetFlexibleDirection( wx.BOTH )
        gbSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"image.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
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
        
        gbSizer4.Add( bSizer1, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"剩余试用数:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        self.m_staticText7.SetForegroundColour( wx.Colour( 254, 217, 204 ) )
        
        bSizer2.Add( self.m_staticText7, 0, wx.ALL, 5 )
        
        self.m_tailSticTxt = wx.StaticText( self, wx.ID_ANY, u"5", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_tailSticTxt.Wrap( -1 )
        self.m_tailSticTxt.SetFont( wx.Font( 40, 70, 90, 90, False, wx.EmptyString ) )
        self.m_tailSticTxt.SetForegroundColour( wx.Colour( 137, 255, 128 ) )
        
        bSizer2.Add( self.m_tailSticTxt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        gbSizer4.Add( bSizer2, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
        
        gSizer1.Add( gbSizer4, 1, wx.EXPAND, 5 )
        
        sbSizer1.Add( gSizer1, 1, wx.EXPAND, 5 )
        
        self.m_gauge1 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 750,-1 ), wx.GA_HORIZONTAL )
        self.m_gauge1.SetValue( 1 ) 
        sbSizer1.Add( self.m_gauge1, 0, wx.ALL, 5 )
        
        self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 760,98 ), 0 )
        sbSizer1.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
        
        self.SetSizer( sbSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass
    


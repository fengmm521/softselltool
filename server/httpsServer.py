#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-07 09:28:00
# @Link    : http://fengmm521.blog.163.com
# @Version : $Id$
#https服务器
import os
import ssl
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import logging
import cgi
import time
import posixpath
import urllib
import sys
import shutil
import mimetypes
import json

import struct

import hashlib

import WXMsgTool

import socket
hostname = socket.gethostname()
selfip = socket.gethostbyname(hostname)

setLastIP = selfip

print 'selfIP:',selfip
print 'setLastIP:',setLastIP

#子线程下的函数调用超时工具,此工具比较消耗时间性能，但在这里可以用
from kthreadTimeoutTool import timeoutTool

#调用函数超时:http://blog.csdn.net/jinnian_lin/article/details/19918703
import signal  
class TimeOutException(Exception):  
    pass  
  
def setTimeout(num, callback):  
    def wrape(func):  
        def handle(signum, frame):  
            raise TimeOutException("运行超时！")  
        def toDo(*args, **kwargs):  
            try:  
                signal.signal(signal.SIGALRM, handle)  
                signal.alarm(num)#开启闹钟信号  
                rs = func(*args, **kwargs)  
                signal.alarm(0)#关闭闹钟信号  
                return rs  
            except TimeOutException, e:  
                callback()  
              
        return toDo  
    return wrape 



wxtool = WXMsgTool.WXMsgTool()

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

nowPth = os.path.split(os.getcwd())[1]
curdir = '.'
if nowPth == 'btcchttp':
    curdir = 'httpserver'


#okcoin合约价格预警签名相关
md5frontstr = "woodcol~!@09"
md5endStr = "okcointrade&^%12"


class myHandler(BaseHTTPRequestHandler):

    #校验消息真实性
    def verifyEsp8266Msg(self,reqdict):
        timestr = reqdict['time']
        tmpstr = ''
        if reqdict.has_key('lastprice'):
            lastprice = reqdict['lastprice']
            tmpstr = md5frontstr + timestr + lastprice + md5endStr
        else:
            tmpstr = md5frontstr + timestr + md5endStr
        sha1str = hashlib.md5(tmpstr).hexdigest()
        print sha1str,timestr
        if sha1str == reqdict['signature']:
            return True
        else:
            return False

    def do_GET(self):  
    	# print self.path
        # print self.client_address
        # print self.client_address
        if self.client_address[0] == selfip and self.path[0:3] != '/ok':

            print 'address is self'
            backstr = 'get self ask'
            length = len(backstr)
            self.send_response(200)
            self.send_header("Content-type", 'application/json; encoding=utf-8')
            self.send_header("Content-Length", str(length))
            self.end_headers()
            self.wfile.write(backstr)
            return None

        #保存当成交价信息
        if self.client_address[0] == '114.215.203.152' and self.path[0:8] == '/setlast':
            datastrs = self.path.split('?')
            if len(datastrs) > 1:
                requestr = datastrs[1]
                coms = requestr.split('&')
                reqdata = {}
                for c in coms:
                    tmps = c.split('=')
                    reqdata[tmps[0]] = tmps[1]
                if reqdata.has_key('last'):
                    wxtool.setLastPriceFromOKEX(float(reqdata['last']))
            self.sendEmptyMsg()
            return None

        if self.client_address[0].find('shadowserver') != -1:
            # self.connection.close()
            return None

        if self.path=="/":  
            self.path="/index.html"  
        
        try:  
            #根据请求的文件扩展名，设置正确的mime类型  
            sendReply = False  
            
            if self.path[0:3] == "/wx":
                sendReply = False
                datastrs = self.path.split('?')
                if len(datastrs) > 1:
                    requestr = datastrs[1]
                    coms = requestr.split('&')
                    reqdata = {}
                    for c in coms:
                        tmps = c.split('=')
                        reqdata[tmps[0]] = tmps[1]
                    # print reqdata
                # sendstr = json.dumps(tokenback)
                    if 'echostr' in reqdata.keys():
                        sendstr = reqdata['echostr']
                        length = len(sendstr)
                        self.send_response(200)
                        self.send_header("Content-type", 'application/json; encoding=utf-8')
                        self.send_header("Content-Length", str(length))
                        self.end_headers()
                        self.wfile.write(sendstr)
                    else:
                        return reqdata
            elif self.path[0:3] == "/ok": #okcoin合约价格预警
            #https://btc.woodcol.com/ok?time=1234567&signature=abcdef12345678
                datastrs = self.path.split('?')
                if len(datastrs) > 1:
                    requestr = datastrs[1]
                    coms = requestr.split('&')
                    reqdata = {}
                    for c in coms:
                        tmps = c.split('=')
                        reqdata[tmps[0]] = tmps[1]
                    if 'time' in reqdata.keys() and 'signature' in reqdata.keys():
                        if self.verifyEsp8266Msg(reqdata):
                            wxtool.limtLastTime = time.time()
                            if reqdata.has_key('lastprice'):
                                wxtool.okLastPrice = float(reqdata['lastprice'])
                            sendstr = "{\"minlimt\":%.2f,\"maxlimt\":%.2f,\"market\":%d,\"erro\":0}"%(wxtool.minlimt,wxtool.maxlimt,wxtool.market)
                            if wxtool.market == 2:
                                isBeep = 0
                                if wxtool.bitmexHttpLastPrice <= wxtool.minlimt:
                                    isBeep = -1
                                elif wxtool.bitmexHttpLastPrice >= wxtool.maxlimt:
                                    isBeep = 1
                                else:
                                    isBeep = 0
                                sendstr = "{\"minlimt\":%.2f,\"maxlimt\":%.2f,\"market\":%d,\"lastprice\":%.2f,\"isBeep\":%d,\"erro\":0}"%(wxtool.minlimt,wxtool.maxlimt,wxtool.market,wxtool.bitmexHttpLastPrice,isBeep)
                            # print sendstr
                            length = len(sendstr)
                            self.send_response(200)
                            self.send_header("Content-type", 'application/json; encoding=utf-8')
                            self.send_header("Content-Length", str(length))
                            self.end_headers()
                            self.wfile.write(sendstr)
                        else:
                            sendstr = '{\"erro\":1}'
                            # print sendstr
                            length = len(sendstr)
                            self.send_response(200)
                            self.send_header("Content-type", 'application/json; encoding=utf-8')
                            self.send_header("Content-Length", str(length))
                            self.end_headers()
                            self.wfile.write(sendstr)
            else:
                if self.path.endswith(".html"):  
                    mimetype='text/html'  
                    sendReply = True  
                elif self.path.endswith(".jpg"):  
                    mimetype='image/jpg'  
                    sendReply = True  
                elif self.path.endswith(".gif"):  
                    mimetype='image/gif'  
                    sendReply = True  
                elif self.path.endswith(".js"):  
                    mimetype='application/javascript'  
                    sendReply = True  
                elif self.path.endswith(".css"):  
                    mimetype='text/css'  
                    sendReply = True  
                elif self.path.endswith(".swf"):  
                    mimetype='application/x-shockwave-flash'  
                    sendReply = True  
                else:
                    return None

            if sendReply == True:  
                    #读取相应的静态资源文件，并发送它  
                    f = open(curdir + os.sep + self.path, 'rb')  
                    self.send_response(200)  
                    self.send_header('Content-type',mimetype)  
                    self.end_headers()  

                    self.wfile.write(f.read())  
                    f.close()  
            return None
  
        except IOError:  
            self.send_error(404,'File Not Found: %s' % self.path)  
            return None
  
    def sendEmptyMsg(self):
        self.send_response(200)
        self.send_header("Content-type", 'application/xml; encoding=utf-8')
        self.send_header("Content-Length", str(''))
        self.end_headers()
        self.wfile.write('')

    def sendMsg(self,toUserName,fromUserName,msg):
        # <xml>
        # <ToUserName><![CDATA[toUser]]></ToUserName>
        # <FromUserName><![CDATA[fromUser]]></FromUserName>
        # <CreateTime>12345678</CreateTime>
        # <MsgType><![CDATA[text]]></MsgType>
        # <Content><![CDATA[你好]]></Content>
        # </xml>
        # print 'sendmsg------>'
        sendmsg = u'<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%d</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA['%(toUserName,fromUserName,int(time.time())) + unicode(msg,'utf-8') + u']]></Content></xml>'
        # sendmsg = unicode(sendmsg,'utf-8')
        # print sendmsg
        sendmsg = sendmsg.encode('UTF-8')
        # sendmsg = asiic(sendmsg)
        self.send_response(200)
        self.send_header("Content-type", 'application/xml; encoding=utf-8')
        self.send_header("Content-Length", str(len(sendmsg)))
        self.end_headers()
        self.wfile.write(sendmsg)

    #校验消息真实性
    def verifyMsg(self,reqdict):
        tokenver = []
        tokenver.append('tokenxxx')
        tokenver.append(reqdict['nonce'])
        tokenver.append(reqdict['timestamp'])
        tokenver.sort()
        tmpstr = tokenver[0] + tokenver[1] + tokenver[2]
        sha1str = hashlib.sha1(tmpstr).hexdigest()
        if sha1str == reqdict['signature']:
            return True
        else:
            return False
    def do_POST(self):
        print 'get post'

        dictmp = self.do_GET()

        isOK = False
        if dictmp:
            isOK = self.verifyMsg(dictmp)

        if isOK:
            length = self.headers.getheader('content-length');
            nbytes = int(length)
            data = self.rfile.read(nbytes)
            wxtool.getWXMsg(data, self)
        else:
            print 'get post erro'
            self.send_error(404,'File Not Found: %s' % self.path)     
        # self.connection.close()

    # def _writeheaders(self):
    #     print self.path
    #     print self.headers
    #     self.send_response(200);
    #     self.send_header('Content-type','text/html');
    #     self.end_headers()
    def do_HEAD(self):
        print 'do_head'
        # if self.client_address[0].find('shadowserver') != -1:
        #     self.connection.close()
        #     return




class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    # daemon_threads = True
    timeout = 2
    # def handle_timeout(self):
    #     try:
    #         print 'timeout'
    #     except socket.error:
    #         print 'erro'
    #         return

    def get_request(self):
        @timeoutTool(1)  #accept调用超时，会调用timeoutFunc函数
        def timeoutGetAccept(obj):
            try:
                return obj.accept()
            except Exception as e:
                return None
        tmp = timeoutGetAccept(self.socket)
        if tmp:
            return tmp
        else:
            return None,None

    def _handle_request_noblock(self):
        try:
            request,client_address  = self.get_request()
            if not (request and client_address):
                return
        except socket.error:
            return
        if self.verify_request(request, client_address):
            try:
                self.process_request(request, client_address)
            except:
                self.handle_error(request, client_address)
                self.shutdown_request(request)

serverAddr = (selfip,4443)

if curdir == 'httpserver' or selfip[0:2] != '19':
    serverAddr = ('114.215.203.152',443)

class HttpStartObj (threading.Thread):   #继承父类threading.Thread
    def __init__(self):
        threading.Thread.__init__(self)
    def httpServerRestart(self):
        try:
            server = ThreadedHTTPServer(serverAddr, myHandler)
            print 'https server is running....'
            print 'Starting server, use <Ctrl-C> to stop'
            server.socket = ssl.wrap_socket (server.socket, certfile=curdir + '/server.pem', server_side=True)
            # server.serve_forever()
            while True: 
                server.handle_request()
        except Exception as e:
            print e
            self.httpServerRestart()
    def runHttpServer(self):
        print serverAddr
        try:
            server = ThreadedHTTPServer(serverAddr, myHandler)
            print 'https server is running....'
            print 'Starting server, use <Ctrl-C> to stop'
            server.socket = ssl.wrap_socket (server.socket, certfile=curdir + '/server.pem', server_side=True)
            # server.serve_forever()
            while True:  
                server.handle_request()
        except Exception as e:
            print e
            self.httpServerRestart()
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        
        self.runHttpServer()

def httpServerRestart():
    try:
        server = ThreadedHTTPServer(serverAddr, myHandler)
        print 'https server is running....'
        print 'Starting server, use <Ctrl-C> to stop'
        server.socket = ssl.wrap_socket (server.socket, certfile=curdir + '/server.pem', server_side=True)
        # server.serve_forever()
        while True: 
            server.handle_request()
    except Exception as e:
        print e
        httpServerRestart()
def runHttpServer(tmpp):
    print serverAddr
    try:
        server = ThreadedHTTPServer(serverAddr, myHandler)
        print 'https server is running....'
        print 'Starting server, use <Ctrl-C> to stop'
        server.socket = ssl.wrap_socket (server.socket, certfile=curdir + '/server.pem', server_side=True)
        # server.serve_forever()
        while True:  
            server.handle_request()
    except Exception as e:
        print e
        httpServerRestart()
    
    
def startServer(ltctool,btctool):

    wxtool.setBTCTool(btctool)
    wxtool.setLTCTool(ltctool)

    thr = threading.Thread(target=runHttpServer,args=(None,))
    thr.setDaemon(True)
    thr.start()
    # thread1 = HttpStartObj()
    # thread1.setDaemon(True)
    # thread1.start()

    return wxtool



if __name__ == '__main__':
    # server = ThreadedHTTPServer(serverAddr, myHandler)
    # print 'https server is running....'
    # print 'Starting server, use <Ctrl-C> to stop'
    # server.socket = ssl.wrap_socket (server.socket, certfile='server.pem', server_side=True)
    # server.serve_forever()
    print serverAddr
    wxtool.setBTCTool(None)
    wxtool.setLTCTool(None)
    server = ThreadedHTTPServer(serverAddr, myHandler)
    print 'https server is running....'
    print 'Starting server, use <Ctrl-C> to stop'
    server.socket = ssl.wrap_socket (server.socket, certfile=curdir + '/keys/server.pem', server_side=True)
    # server.socket.settimeout(2)
    # # print server.socket.getsockopt(socket.SOL_S0CKET,socket.SO_RCVTIMEO)
    # print socket.SOL_SOCKET
    # print socket.SO_RCVTIMEO
    # print server.socket.getsockopt(socket.SOL_SOCKET,socket.SO_RCVTIMEO)
    # server.socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVTIMEO,struct.pack("LL", 2, 0))
    # server.socket.setsockopt(socket.SOL_SOCKET,socket.SO_LINGER,struct.pack('ii', 0, 1))
    # print server.socket.getsockopt(socket.SOL_SOCKET,socket.SO_RCVTIMEO)
    while True:  
        server.handle_request()
        try:
            pass
        except KeyboardInterrupt:
            print 'shutdown'
            server.shutdown()
        
        
    # server.serve_forever()


# # 生成rsa密钥
# $ openssl genrsa -des3 -out server.key 2048
# # 去除掉密钥文件保护密码
# $ openssl rsa -in server.key -out server.key
# # 生成ca对应的csr文件
# $ openssl req -new -key server.key -out server.csr
# # 自签名
# $ openssl x509 -req -days 2048 -in server.csr -signkey server.key -out server.crt
# $ cat server.crt server.key > server.pem

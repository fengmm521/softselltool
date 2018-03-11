#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-07 09:28:00
# @Link    : http://fengmm521.blog.163.com
# @Version : $Id$
#这里使用pycrypto‎库
#按照方法:easy_install pycrypto‎
 
import os,sys
import base64
import requests

# from Crypto import Random
# from Crypto.Hash import SHA
# from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
# from Crypto.PublicKey import RSA
import rsa

# https://www.cnblogs.com/hhh5460/p/5243410.html

class prpcrypt():
    def __init__(self,mURL,mkeyPth,gkeyPth,isCreateGkey = True,isTest = False):
        self.mkeyPth = mkeyPth     #master公钥保存地址
        self.gkeyPth = gkeyPth     #本地密钥保存地址
        self.mURL = mURL           #master公钥请求地址，
        
        self.gprivate_pem = None
        self.gpublic_pem = None

        self.mpublic_pem = None

        self.isTest = isTest

        if isCreateGkey:
            #生成新的公私钥对
            self.createGhostKey()
            # self.saveGhostKeyToFile()
        else:
            self.readGhostKeyFromFile()
            if self.gprivate_pem == None or self.gpublic_pem == None:
                self.createGhostKey()
                self.saveGhostKeyToFile()
        self.masterKeyFromFile()

    def saveGhostKeyToFile(self):
        f = open(self.gkeyPth + '/gprivate.pem','w')
        if sys.version_info > (3,0):
            f.write(self.gprivate_pem.save_pkcs1().decode())
        else:
            f.write(self.gprivate_pem.save_pkcs1())
        f.close()
        f = open(self.gkeyPth + '/gpublic.pem','w')
        if sys.version_info > (3,0):
            f.write(self.gpublic_pem.save_pkcs1().decode())
        else:
            f.write(self.gpublic_pem.save_pkcs1())
        f.close()
    def readGhostKeyFromFile(self):
        pripth = self.gkeyPth + '/gprivate.pem'
        pubpth = self.gkeyPth + '/gpublic.pem'
        if os.path.exists(pripth) and os.path.exists(pubpth):
            f = open(pripth,'r')
            if sys.version_info > (3,0):
                self.gprivate_pem = rsa.PrivateKey.load_pkcs1(f.read().encode())
            else:
                self.gprivate_pem = rsa.PrivateKey.load_pkcs1(f.read())
            f.close()
            f = open(pubpth,'r')
            if sys.version_info > (3,0):
                self.gpublic_pem = rsa.PublicKey.load_pkcs1(f.read().encode())
            else:
                self.gpublic_pem = rsa.PublicKey.load_pkcs1(f.read())
            f.close()
        else:
            print('本地RSA密钥文件不存在，可以文件丢失，请重新生成...')

    #从文件读取交互对方的公钥
    def masterKeyFromFile(self):
        pubpth = self.mkeyPth + '/mpublic.pem'
        if os.path.exists(pubpth):
            f = open(pubpth,'r')
            if sys.version_info > (3,0):
                self.mpublic_pem = rsa.PublicKey.load_pkcs1(f.read().encode())
            else:
                self.mpublic_pem = rsa.PublicKey.load_pkcs1(f.read())
            f.close()
        else:
            self.mpublic_pem = self.requestMasterPubkey()
            if self.mpublic_pem != None:
                self.saveMasterPubkeyToFile()
        if self.mpublic_pem == None:
            print('未获取到交互对方公钥...')

    def saveMasterPubkeyToFile(self):
        pubpth = self.mkeyPth + '/mpublic.pem'
        f = open(pubpth,'w')
        if sys.version_info > (3,0):
            f.write(self.mpublic_pem.save_pkcs1().decode())
        else:
            f.write(self.mpublic_pem.save_pkcs1())
        f.close()
    #向服务器请求pubkey
    def requestMasterPubkey(self):
        rurl = self.mURL
        try:
            res = requests.get(self.mURL, verify=False)
            print(res.text)
            return res.text
        except Exception as e:
            print(e)
        return None
    #生成自已的公私钥对
    def createGhostKey(self):
        # 伪随机数生成器
        # random_generator = Random.new().read
        # rsa算法生成实例
        # rsa = RSA.generate(1024, random_generator)


        # # ghost的秘钥对的生成
        # #私钥
        # self.gprivate_pem = rsa.exportKey()
        # #公钥
        # self.gpublic_pem = rsa.publickey().exportKey()

        (self.gpublic_pem, self.gprivate_pem) = rsa.newkeys(1024)

    #使用交互方公钥加密消息数据
    def encryptWithMasterPubKey(self,msg,isBase64Out = True):
        tmpmsg = msg
        if sys.version_info > (3,0):
            tmpmsg = msg.encode()
        if isBase64Out:
            cipher_text = base64.b64encode(rsa.encrypt(tmpmsg, self.mpublic_pem))
            return cipher_text
        else:
            dmsg = rsa.encrypt(tmpmsg, self.mpublic_pem)
            return dmsg

    #使用交互方公钥验证签名    
    def verifyWithMasterPubKey(self,msg,sign,isBase64In = True):
        tmpmsg = msg
        if sys.version_info > (3,0):
            tmpmsg = msg.encode()
        if isBase64In:
            dmsg = base64.b64decode(tmpmsg)
        vermsg = rsa.verify(dmsg, sign, self.mpublic_pem)
        return vermsg

    #使用本地公钥加密消息数据
    def encryptWithGhostPubKey(self,msg,isBase64Out = True):
        tmpmsg = msg
        if sys.version_info > (3,0):
            tmpmsg = msg.encode()
        if isBase64Out:
            cipher_text = base64.b64encode(rsa.encrypt(tmpmsg, self.gpublic_pem))
            return cipher_text
        else:
            dmsg = rsa.encrypt(tmpmsg, self.gpublic_pem)
            return dmsg

    #使用本地私钥解密消息
    def decryptWithGhostPriKey(self,msg,isBase64In = True):
        dmsg = msg
        if isBase64In:
            dmsg = base64.b64decode(msg)
        text = rsa.decrypt(dmsg, self.gprivate_pem)
        return text

    #使用本地私钥签名消息
    def signWithGhostPriKey(self,msg):
        tmpmsg = msg
        if sys.version_info > (3,0):
            tmpmsg = msg.encode()
        signature = rsa.sign(tmpmsg, self.gprivate_pem, 'SHA-1')
        return signature
    #使用本地公钥验证签名    
    def verifyWithGhostPubKey(self,msg,sign,isBase64In = True):
        tmpmsg = msg
        if sys.version_info > (3,0):
            tmpmsg = msg.encode()
        dmsg = tmpmsg
        if isBase64In:
            dmsg = base64.b64decode(msg)
        vermsg = rsa.verify(dmsg, sign, self.gpublic_pem)
        return vermsg




if __name__ == '__main__':
    pc = prpcrypt(mURL='', mkeyPth = '.', gkeyPth = '.',isCreateGkey = False)
    msg = 'abcdefg---001'
    pmsg = pc.encryptWithGhostPubKey(msg)
    omsg = pc.decryptWithGhostPriKey(pmsg)

    print('msg--->',msg)
    print('pmsg-->',pmsg)
    print('omsg-->',omsg)

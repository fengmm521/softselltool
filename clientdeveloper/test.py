# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep 12 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import requests
Host = 'https://192.168.123.200:4443/'
def getImageFromURL(purl = 'image.png'):
        rurl = Host + purl
        try:
            print(rurl)
            s = requests.session()
            s.headers.update({'User-agent', 'Mozilla 5.10'})
            res = s.get(rurl, verify=False)
            print(len(res.content))
            return res.content
            # html.content
        except Exception, e:
            print e
        return None

def getImg():
    html = requests.get('https://192.168.123.200:4443/image.png',verify=False)
    with open('picture.jpg', 'wb') as file:
        file.write(html.content)

def main():
    getImg()

if __name__ == '__main__':
    main()


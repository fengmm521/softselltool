#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 22:36:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os,sys

import platform

import time

from pytube import YouTube

# print sys.path.append('/usr/local/Cellar')

reload(sys)
sys.setdefaultencoding( "utf-8" )

# print sys.getdefaultencoding()

#Windows,Darwin,linux
sysplatform = platform.platform().split('-')[0] 
sysarch = platform.architecture()[0]


isTrailCode = True


ffmpegpth = os.path.split(sys.argv[0])[0]

scrpitepth = ffmpegpth

isWinSystem = False

if sysplatform == 'Windows':
    isWinSystem = True
    
    if sysarch == '64bit':
        if ffmpegpth != '':
            ffmpegpth += '\\ffmpeg_win64\\ffmpeg.exe'
        else:
            ffmpegpth = '\\ffmpeg_win64\\ffmpeg.exe'
    else:
        if ffmpegpth != '':
            ffmpegpth += '\\ffmpeg_win32\\ffmpeg.exe'
        else:
            ffmpegpth = '\\ffmpeg_win32\\ffmpeg.exe'
elif sysplatform == 'Darwin':
    if ffmpegpth != '':
        ffmpegpth += '/ffmpeg_mac/ffmpeg'
    else:
        ffmpegpth = 'ffmpeg_mac/ffmpeg'
    cmd = 'chmod 777 %s'%(ffmpegpth)
    os.system(cmd)

# print sys.getdefaultencoding()


print('sys is %s'%(sysplatform))

print(scrpitepth )
print(ffmpegpth) 

class MsgObj():
    def __init__(self,msg,ptype = 'msg'):
        self.ptype = ptype
        self.data = msg


def get_desktop():
    if isWinSystem:
        import _winreg
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return _winreg.QueryValueEx(key, "Desktop")[0]
    else:
        return '~/Desktop'

print(get_desktop())

def isWindowsSys():
    return isWinSystem


class showMsgTool(object):
    """docstring for ClassName"""
    def __init__(self):
        self.uitool = None
        
    def setUIObj(self,uiobj):
        self.uitool = uiobj
    def showMsgTOUI(self,msg):
        if self.uitool:
            msgobj = MsgObj(msg)
            self.uitool.queue.put(msgobj)
            # self.uitool.showMsg(msg)
    def sendCmd(self,cmd):
        if self.uitool:
            msgobj = MsgObj(cmd,'cmd')
            self.uitool.queue.put(msgobj)

msgtool = showMsgTool()

if os.path.exists('log.txt'):
    os.remove('log.txt')

def savelog(logstr):

    if isWinSystem:
        f = open('log.txt','a')
        outstr = logstr + '\n'
        f.write(outstr)
        f.close()

def showMsg(msg):
    if isWinSystem:
        
        # os_codepage = sys.getfilesystemencoding()
        # outmsg = msg.decode('utf-8').encode(os_codepage)
        if msgtool:
            outmsg = msg + '\n'
            msgtool.showMsgTOUI(outmsg)
            savelog(outmsg)
        else:
            try:
                print(msg.decode('utf-8'))
            except Exception, e:
                print('in windows system chinese is not show') 
    else:
        if msgtool:
            outmsg = msg + '\n'
            msgtool.showMsgTOUI(outmsg)
            savelog(msg)
        else:
            print(msg)


#获取脚本路径
def cur_file_dir():
    pathx = sys.argv[0]
    tmppath,_file = os.path.split(pathx)
    if cmp(tmppath,'') == 0:
        tmppath = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(tmppath):
        return tmppath
    elif os.path.isfile(tmppath):
        return os.path.dirname(tmppath)
    


#获取父目录
def GetParentPath(strPath):
    if not strPath:
        return None;
    lsPath = os.path.split(strPath);
    if lsPath[1]:
        return lsPath[0];
    lsPath = os.path.split(lsPath[0]);
    return lsPath[0];

#获取目录下的所有类型文件
def getAllExtFile(pth,fromatx = ".mp4"):
    jsondir = pth
    jsonfilelist = []
    for root, _dirs, files in os.walk(jsondir):
        for filex in files:          
            name,text = os.path.splitext(filex)
            if cmp(text,fromatx) == 0:
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
            elif fromatx == ".*" :
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
    return jsonfilelist


    # def filter(
    #         self, fps=None, res=None, resolution=None, mime_type=None,
    #         type=None, subtype=None, file_extension=None, abr=None,
    #         bitrate=None, video_codec=None, audio_codec=None,
    #         only_audio=None, only_video=None,
    #         progressive=None, adaptive=None,
    #         custom_filter_functions=None,
    # ):


# <Stream: itag="22" mime_type="video/mp4" res="720p" fps="30fps" vcodec="avc1.64001F" acodec="mp4a.40.2">
# <Stream: itag="43" mime_type="video/webm" res="360p" fps="30fps" vcodec="vp8.0" acodec="vorbis">
# <Stream: itag="18" mime_type="video/mp4" res="360p" fps="30fps" vcodec="avc1.42001E" acodec="mp4a.40.2">
# <Stream: itag="36" mime_type="video/3gpp" res="240p" fps="30fps" vcodec="mp4v.20.3" acodec="mp4a.40.2">
# <Stream: itag="17" mime_type="video/3gpp" res="144p" fps="30fps" vcodec="mp4v.20.3" acodec="mp4a.40.2">
# <Stream: itag="137" mime_type="video/mp4" res="1080p" fps="30fps" vcodec="avc1.640028">
# <Stream: itag="248" mime_type="video/webm" res="1080p" fps="30fps" vcodec="vp9">
# <Stream: itag="136" mime_type="video/mp4" res="720p" fps="30fps" vcodec="avc1.4d401f">
# <Stream: itag="247" mime_type="video/webm" res="720p" fps="30fps" vcodec="vp9">
# <Stream: itag="135" mime_type="video/mp4" res="480p" fps="30fps" vcodec="avc1.4d401e">
# <Stream: itag="244" mime_type="video/webm" res="480p" fps="30fps" vcodec="vp9">
# <Stream: itag="134" mime_type="video/mp4" res="360p" fps="30fps" vcodec="avc1.4d401e">
# <Stream: itag="243" mime_type="video/webm" res="360p" fps="30fps" vcodec="vp9">
# <Stream: itag="133" mime_type="video/mp4" res="240p" fps="30fps" vcodec="avc1.4d4015">
# <Stream: itag="242" mime_type="video/webm" res="240p" fps="30fps" vcodec="vp9">
# <Stream: itag="160" mime_type="video/mp4" res="144p" fps="30fps" vcodec="avc1.4d400c">
# <Stream: itag="278" mime_type="video/webm" res="144p" fps="30fps" vcodec="vp9">
# <Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2">
# <Stream: itag="171" mime_type="audio/webm" abr="128kbps" acodec="vorbis">
# <Stream: itag="249" mime_type="audio/webm" abr="50kbps" acodec="opus">
# <Stream: itag="250" mime_type="audio/webm" abr="70kbps" acodec="opus">
# <Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="opus">

def makeMoive(ptitle,videoType = '1080p',outpth = 'out'):

    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    if (not os.path.exists('out')) and outpth == 'out':
        os.mkdir('out')
        
    if os.path.exists('tmp/output.mp4'):
        os.remove('tmp/output.mp4')

    # savename = ptitle.replace('"','').replace("'","").replace('“','').replace('”', '').replace('’', '')
    cmd = '%s -i "%s/video.mp4" -i "audio/audio.mp4" -vcodec copy -acodec copy "tmp/output.mp4"'%(ffmpegpth,videoType)
    if isWinSystem:
        cmd = u'%s -i \"%s/video.mp4\" -i \"audio/audio.mp4\" -vcodec copy -acodec copy \"tmp/output.mp4\"'%(ffmpegpth,videoType)
    showMsg(cmd)
    os.system(cmd)

    cmd = 'mv \"tmp/output.mp4\" \"%s/%s.mp4\"'%(outpth,ptitle)

    if isWinSystem:
        cmd = 'move \"tmp\\output.mp4\" \"%s\\%s.mp4\"'%(outpth,ptitle)

    showMsg(cmd)
    os.system(cmd)

def isHeaveMp4File(title,savepth):
    fs = getAllExtFile(savepth)
    for f in fs:
        if f[2].find(title) != -1:
            return True
    return False


def isHeaveMp4FileInMTVDir(title):
    fs = getAllExtFile('/Volumes/mage/moive/mtv')
    for f in fs:
        if f[2].find(title) != -1:
            return True
    return False

def titleRename(pname):
    tmpstr = pname.replace('/','')
    tmpstr = tmpstr.replace('\\','')
    tmpstr = tmpstr.replace(' ','_')
    tmpstr = tmpstr.replace(',','')
    tmpstr = tmpstr.replace(';','')
    tmpstr = tmpstr.replace('"','')
    tmpstr = tmpstr.replace("'","")
    tmpstr = tmpstr.replace('|','')
    tmpstr = tmpstr.replace('?','')
    tmpstr = tmpstr.replace('*','')
    tmpstr = tmpstr.replace('<','')
    tmpstr = tmpstr.replace('>','')
    tmpstr = tmpstr.replace('$','')
    tmpstr = tmpstr.replace('%','')
    tmpstr = tmpstr.replace('&','')
    tmpstr = tmpstr.replace('^','')
    tmpstr = tmpstr.replace('`','')
    tmpstr = tmpstr.replace(',','')
    tmpstr = tmpstr.replace(':','')
    tmpstr = tmpstr.replace('[','')
    tmpstr = tmpstr.replace(']','')
    tmpstr = tmpstr.replace('{','')
    tmpstr = tmpstr.replace('}','')
    tmpstr = tmpstr.replace('=','-')
    tmpstr = tmpstr.replace('(','-')
    tmpstr = tmpstr.replace(')','-')
    tmpstr = tmpstr.replace('#','')
    tmpstr = tmpstr.replace('@','')
    tmpstr = tmpstr.replace('!','')
    tmpstr = tmpstr.replace('‘','')
    tmpstr = tmpstr.replace('’','')
    # /'  '?'  '*'  ':'  '|'  '\'  '<'  '>'
    return tmpstr
def downloadWithURL(pURL = 'https://www.youtube.com/watch?v=cmSbXsFE3l8',outpth = 'out'):
    if msgtool:
        msgtool.uitool.showDownStart()
    showMsg('开始获取,视频网址')
    showMsg(pURL)
    showMsg('的视频信息...')
    
    yt = YouTube(pURL)
    alllist = yt.streams.all()
    for x in alllist:
        showMsg(str(x))

    p1080 = yt.streams.filter(res='1080p', file_extension='mp4').first()
    p720 = yt.streams.filter(res='720p', file_extension='mp4').first()
    p480 = yt.streams.filter(res='480p', file_extension='mp4').first()
    p360 = yt.streams.filter(res='360p', file_extension='mp4').first()
    p240 = yt.streams.filter(res='240p', file_extension='mp4').first()
    p144 = yt.streams.filter(res='144p', file_extension='mp4').first()


    abr128k = yt.streams.filter(abr="128kbps", file_extension='mp4').first()

    # print p1080.player_config_args['title'].encode('utf-8')
    # print abr128k.player_config_args['title'].encode('utf-8')
    title = ''
    audiopth = ''

    if abr128k:
        # abr128k.player_config_args['title'] = abr128k.player_config_args['title'].encode('utf-8')
        # 
        if not os.path.exists('audio'):
            os.mkdir('audio')

        
        audiopth = 'audio/audio.mp4'

        # if os.path.exists(audiopth):
            # os.remove(audiopth)

        title = abr128k.player_config_args['title'].encode('utf-8')
        oletitle = str(title)
        title = titleRename(title)
        
        if isHeaveMp4File(title, outpth):
            tmpstr = '(%s) 要下载的视频已存，请查找文件夹:\n %s'%(title,outpth)
            showMsg(tmpstr)
            return
        if isHeaveMp4FileInMTVDir(title):
            showMsg('(%s) title is heave in MTV dir(/Volumes/mage/moive/mtv)'%(title)) 
            return


        try:
            abr128k.player_config_args['title'] = 'audio'

            tmppth = 'audio' + os.sep + 'audio.mp4'
            if msgtool:
                msgtool.uitool.showDownAudio(tmppth)

            tmpstr = '开始下载音频文件...'

            showMsg(tmpstr)

            tmpstr = u'视频名称:%s'%(oletitle)
            showMsg(tmpstr)
            tmpstr = '正在下载码率为128kbps的音频文件...'

            showMsg(tmpstr)

            abr128k.download('audio')

        except Exception as e:

            print(e)
            showMsg('128kbps音频不存在，将下载其他码率音频文件')

            abr128k = yt.streams.filter(mime_type="audio/mp4", file_extension='mp4').first()

            abr128k.player_config_args['title'] = 'audio'

            showMsg('开始下音频文件...')
            tmppth = 'audio' + os.sep + 'audio.mp4'
            if msgtool:
                msgtool.uitool.showDownAudio(tmppth)

            abr128k.download('audio')
        
    else:

        videoandaudio = yt.streams.first()
        title = videoandaudio.player_config_args['title'].encode('utf-8')
        oletitle = str(title)
        title = titleRename(title)

        tmpstr = '视频名称:' + oletitle
        showMsg(tmpstr)
        if isHeaveMp4File(title, outpth):
            strtmp = '(%s) 要下载的文件已存在,%s'%(title,outpth)
            showMsg(strtmp)
            return
        if isHeaveMp4FileInMTVDir(title):
            print('(%s) title is heave in MTV dir(/Volumes/mage/moive/mtv)'%(title))
            return

        videoandaudio.player_config_args['title'] = title

        strtmp = '开妈下载视频和音频文件。。。'
        showMsg(strtmp)

        tmppth = outpth + os.sep + title
        if msgtool:
            msgtool.uitool.showDownVideo(tmppth)

        videoandaudio.download(outpth)

        return

    strtmp = '开始下载视频文件...'
    showMsg(strtmp)

    videopth = ''
    if p1080:
        if not os.path.exists('1080p'):
            os.mkdir('1080p')
        videopth = '1080p/video.mp4'
        if msgtool:
            msgtool.uitool.showDownVideo(videopth)

        tmpstr = '下载1080p的视频...'
        showMsg(tmpstr)
        
        title +='_1080p'

        p1080.player_config_args['title'] = 'video'

        if os.path.exists(videopth):
            os.remove(videopth)

        p1080.download('1080p')

        makeMoive(title,'1080p',outpth)

    elif p720:
        if not os.path.exists('720p'):
            os.mkdir('720p')

        videopth = '720p/video.mp4'
        if msgtool:
            msgtool.uitool.showDownVideo(videopth)
        tmpstr = '下载720p的视频...'
        showMsg(tmpstr)

        title +='_720p'

        p720.player_config_args['title'] = 'video'

        if os.path.exists(videopth):
            os.remove(videopth)

        p720.download('720p')
        
        makeMoive(title,'720p',outpth)
    elif p480:
        if not os.path.exists('480p'):
            os.mkdir('480p')

        videopth = '480p/video.mp4'
        if msgtool:
            msgtool.uitool.showDownVideo(videopth)
        tmpstr = '下载480p的视频...'
        showMsg(tmpstr)

        title +='_480p'

        p480.player_config_args['title'] = 'video'

        
        if os.path.exists(videopth):
            os.remove(videopth)

        p480.download('480p')
        
        makeMoive(title,'480p',outpth)
    elif p360:
        if not os.path.exists('360p'):
            os.mkdir('360p')

        videopth = '360p/video.mp4'
        if msgtool:
            msgtool.uitool.showDownVideo(videopth)
        tmpstr = '下载360p的视频...'
        showMsg(tmpstr)

        title +='_360p'

        p360.player_config_args['title'] = 'video'

        
        if os.path.exists(videopth):
            os.remove(videopth)

        p360.download('360p')
        
        makeMoive(title,'360p',outpth)
    elif p240:
        if not os.path.exists('240p'):
            os.mkdir('240p')

        videopth = '240p/video.mp4'
        if msgtool:
            msgtool.uitool.showDownVideo(videopth)
        tmpstr = '下载240p的视频...'
        showMsg(tmpstr)

        title +='_240p'

        p240.player_config_args['title'] = 'video'

        

        if os.path.exists(videopth):
            os.remove(videopth)

        p240.download('240p')
        
        makeMoive(title,'240p',outpth)
    elif p144:
        if not os.path.exists('144p'):
            os.mkdir('144p')

        videopth = '144p/video.mp4'
        if msgtool:
            msgtool.uitool.showDownVideo(videopth)
        tmpstr = '下载144p的视频...'
        showMsg(tmpstr)

        title +='_144p'

        p144.player_config_args['title'] = 'video'


        if os.path.exists(videopth):
            os.remove(videopth)

        p144.download('144p')
        
        makeMoive(title,'144p',outpth)
    else:
        tmpstr = '网站视频文件不存在'
        showMsg(tmpstr)

    

    tmpstr = '音频临时文件保存在:' + audiopth
    showMsg(tmpstr)
    tmpstr = '视频临时文件保存在:' + videopth
    showMsg(tmpstr)
    tmpstr = '当前视频下载完成'
    showMsg(tmpstr)

    # if os.path.exists(audiopth):
    #     os.remove(audiopth)
    # if os.path.exists(videopth):
    #     os.remove(videopth)

# https://www.youtube.com/watch?v=CMXiCR2gQw0
# <Stream: itag="22" mime_type="video/mp4" res="720p" fps="30fps" vcodec="avc1.64001F" acodec="mp4a.40.2">
# <Stream: itag="43" mime_type="video/webm" res="360p" fps="30fps" vcodec="vp8.0" acodec="vorbis">
# <Stream: itag="18" mime_type="video/mp4" res="360p" fps="30fps" vcodec="avc1.42001E" acodec="mp4a.40.2">
# <Stream: itag="36" mime_type="video/3gpp" res="240p" fps="30fps" vcodec="mp4v.20.3" acodec="mp4a.40.2">
# <Stream: itag="17" mime_type="video/3gpp" res="144p" fps="30fps" vcodec="mp4v.20.3" acodec="mp4a.40.2">

# <Stream: itag="313" mime_type="video/webm" res="2160p" fps="30fps" vcodec="vp9">

# <Stream: itag="264" mime_type="video/mp4" res="144p" fps="30fps" vcodec="avc1.640032">
# <Stream: itag="271" mime_type="video/webm" res="144p" fps="30fps" vcodec="vp9">
# <Stream: itag="137" mime_type="video/mp4" res="1080p" fps="30fps" vcodec="avc1.640028">
# <Stream: itag="248" mime_type="video/webm" res="1080p" fps="30fps" vcodec="vp9">
# <Stream: itag="136" mime_type="video/mp4" res="720p" fps="30fps" vcodec="avc1.4d401f">
# <Stream: itag="247" mime_type="video/webm" res="720p" fps="30fps" vcodec="vp9">
# <Stream: itag="135" mime_type="video/mp4" res="480p" fps="30fps" vcodec="avc1.4d401f">
# <Stream: itag="244" mime_type="video/webm" res="480p" fps="30fps" vcodec="vp9">
# <Stream: itag="134" mime_type="video/mp4" res="360p" fps="30fps" vcodec="avc1.4d401e">
# <Stream: itag="243" mime_type="video/webm" res="360p" fps="30fps" vcodec="vp9">
# <Stream: itag="133" mime_type="video/mp4" res="240p" fps="30fps" vcodec="avc1.4d4015">
# <Stream: itag="242" mime_type="video/webm" res="240p" fps="30fps" vcodec="vp9">
# <Stream: itag="160" mime_type="video/mp4" res="144p" fps="30fps" vcodec="avc1.4d400c">
# <Stream: itag="278" mime_type="video/webm" res="144p" fps="30fps" vcodec="vp9">
# <Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2">
# <Stream: itag="171" mime_type="audio/webm" abr="128kbps" acodec="vorbis">
# <Stream: itag="249" mime_type="audio/webm" abr="50kbps" acodec="opus">
# <Stream: itag="250" mime_type="audio/webm" abr="70kbps" acodec="opus">
# <Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="opus">

def makeMoiveFor4k(ptitle,videoType = '1080p',outpth = 'out',videoFmt = '.webm'):

    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    if (not os.path.exists('out')) and outpth == 'out':
        os.mkdir('out')
        
    # savename = ptitle.replace('"','').replace("'","").replace('“','').replace('”', '').replace('’', '')
    cmd = u'%s -i "%s/video%s" -i "audio/audio.mp4" -vcodec copy -acodec copy "tmp/output%s"'%(ffmpegpth,videoType,videoFmt,videoFmt)

    showMsg(cmd)
    os.system(cmd)

    cmd = 'mv "tmp/output%s" "%s/%s%s"'%(videoFmt,outpth,ptitle,videoFmt)
    showMsg(cmd)
    os.system(cmd)

    if os.path.exists('tmp/output.mp4'):
        os.remove('tmp/output.mp4')


def downloadWithURLFor4K(pURL = 'https://www.youtube.com/watch?v=cmSbXsFE3l8',outpth = 'out'):
    tmpstr = 'now loading vide message from web...'
    showMsg(tmpstr)
    yt = YouTube(pURL)
    alllist = yt.streams.all()

    videowebms = {}
    videomp4s = {}

    # streamstmp = [s for s in alllist]
    for x in alllist:
        showMsg(x)
        time.sleep(0.1)
        if x.resolution and x.resolution[-1] == 'p' and x.mime_type == 'video/webm':
            videowebms[int(x.resolution[:-1])] = x

        if x.resolution and x.resolution[-1] == 'p' and x.mime_type == 'video/mp4':
            videomp4s[int(x.resolution[:-1])] = x

    ks = list(videowebms.keys())
    ks.sort(reverse = True)
    showMsg(ks)

    ks2 = list(videomp4s.keys())
    ks2.sort(reverse = True)
    showMsg(ks2)

    pvalue = max(ks[0], ks2[0])

    videoStream = None

    videopstr = ''
    vodeotype = ''

    if ks2[0] >= ks[0]:
        videopstr = str(ks2[0]) + 'p'
        vodeotype = '.mp4'
        videoStream = videomp4s[ks2[0]]
    else:
        videopstr = str(ks[0]) + 'p'
        vodeotype = '.webm'
        videoStream = videowebms[ks[0]]

    abr128k = yt.streams.filter(abr="128kbps", file_extension='mp4').first()

    # print p1080.player_config_args['title'].encode('utf-8')
    # print abr128k.player_config_args['title'].encode('utf-8')
    title = ''
    audiopth = ''

    if abr128k:
        # abr128k.player_config_args['title'] = abr128k.player_config_args['title'].encode('utf-8')
        # 
        if not os.path.exists('audio'):
            os.mkdir('audio')

        
        audiopth = 'audio/audio.mp4'

        title = abr128k.player_config_args['title'].encode('utf-8')

        title = titleRename(title)
        
        if isHeaveMp4File(title, outpth):
            tmpstr = '(%s) title is heave in %s'%(title,outpth)
            showMsg(tmpstr)
            return
        if isHeaveMp4FileInMTVDir(title):
            print ('(%s) title is heave in MTV dir(/Volumes/mage/moive/mtv)'%(title))
            return

        if os.path.exists(audiopth):
            os.remove(audiopth)

        try:
            abr128k.player_config_args['title'] = 'audio'

            tmpstr = 'video name:%s'%(title)
            showMsg(tmpstr)
            tmpstr = 'start download audio with 128kbps ...'
            showMsg(tmpstr)

            abr128k.download('audio')

        except Exception as e:

            print('download 128 erro,and redownload with other mp4 type')

            abr128k = yt.streams.filter(mime_type="audio/mp4", file_extension='mp4').first()

            abr128k.player_config_args['title'] = 'audio'

            print('start downloading audio other mp4 type ...')

            abr128k.download('audio')
        
    else:

        videoandaudio = yt.streams.first()
        title = videoandaudio.player_config_args['title'].encode('utf-8')

        title = titleRename(title)

        print('title:',title)

        if isHeaveMp4File(title, outpth):
            print('(%s) title is heave in %s'%(title,outpth))
            return
        if isHeaveMp4FileInMTVDir(title):
            print('(%s) title is heave in MTV dir(/Volumes/mage/moive/mtv)'%(title))
            return

        videoandaudio.player_config_args['title'] = title

        print('start downloading voide and audio to out ...')

        videoandaudio.download(outpth)

        return

    videopth = ''
    if videoStream:
        if not os.path.exists(videopstr):
            os.mkdir(videopstr)
        print('start downloading video %s...'%(videopstr))
        
        title +='_%s'%(videopstr)

        videoStream.player_config_args['title'] = 'video'

        videopth = '%s/video%s'%(videopstr,vodeotype)

        if os.path.exists(videopth):
            os.remove(videopth)

        videoStream.download(videopstr)

        makeMoiveFor4k(title,videopstr,outpth,vodeotype)
    else:
        print('not video')


def downloadWithURL1Stream(pURL = 'https://www.youtube.com/watch?v=cmSbXsFE3l8',outpth = 'out'):
    yt = YouTube(pURL)
    downvideo = yt.streams.first()

    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    title = downvideo.player_config_args['title'].encode('utf-8')

    title = titleRename(title)
        
    savetmppth = 'tmp/out.mp4'

    if isHeaveMp4File(title, outpth):
        tmpstr = '(%s) Video already exists, please look up under the next directory:\n %s'%(title,outpth)
        showMsg(tmpstr)
        return
    if isHeaveMp4FileInMTVDir(title):
        print('(%s) title is heave in MTV dir(/Volumes/mage/moive/mtv)'%(title))
        return    

    try:
        downvideo.player_config_args['title'] = 'out'
        tmpstr = '下载的视频名称:%s'%(title)
        showMsg(tmpstr)
        tmpstr = '开始下载视频和音频...'
        showMsg(tmpstr)

        downvideo.download('tmp')

    except Exception as e:

        downvideo.player_config_args['title'] = 'out'

        print('start downloading Video and Audio erro and redownload...')

        downvideo.download('tmp')

    print(savetmppth)

    cmd = 'mv \"tmp/out.mp4\" \"%s/%s.mp4\"'%(outpth,ptitle)
    print(cmd)
    os.system(cmd)

    if os.path.exists(savetmppth):
        os.remove(savetmppth)
        
#下载一个文件中的所有视频,每一个视频地址一行
def downLoadWithList(turlsFilePth,outpth = 'out'):
    if not os.path.exists(turlsFilePth):
        tmpstr = '.txe file path erro:%s'%(turlsFilePth)
        if isWinSystem:
            print(tmpstr.decode('utf-8').encode('gb2312'))
        else:
            print(tmpstr)
        return
    f = open(turlsFilePth,'r')
    lines = f.readlines()
    f.close()

    turls = []
    for l in lines:
        ltmp = l.replace('\r','')
        ltmp = ltmp.replace('\n','')
        if len(ltmp) > 10 and (ltmp[:7] == 'http://' or ltmp[:8]) == 'https://':
            print(ltmp)
            turls.append(ltmp)
    count = len(turls)
    downcount = 0
    for u in turls:
        downcount += 1
        print('strat downloading %d/%d'%(downcount,count))
        print(u)
        downloadWithURL(u,outpth)


def downLoadWithStrList(liststr,countCallBack,outpth = 'out'):
    print('downLoadWithStrList')
    print(liststr)
    lines = liststr.split('\n')
    turls = []
    for l in lines:
        ltmp = l.replace('\r','')
        ltmp = ltmp.replace('\n','')
        if len(ltmp) > 10 and (ltmp[:7] == 'http://' or ltmp[:8]) == 'https://':
            showMsg(ltmp)
            time.sleep(0.1)
            turls.append(ltmp)
    count = len(turls)
    downcount = 0
    for u in turls:
        downcount += 1
        countstr = '%d/%d'%(downcount,count)
        countCallBack(countstr)
        downloadWithURL(u,outpth)
    if msgtool:
        msgtool.uitool.downLoadComplet()

def main(args):
    turl = ''
    if len(args) == 1:
        tmpstr = "please input vide web address:"
        showMsg(tmpstr)

        isNotURL = True

        while isNotURL:
            turl = raw_input()
            print(turl)
            if turl[:7] != 'http://' and turl[:8] != 'https://' and turl[-4:] != '.txt':
                isNotURL = True
                tmpstr = "parameter erro,web address is start with http:// or https://"
                showMsg(tmpstr)
            else:
                tmpstr = 'start download video from web.....'
                showMsg(tmpstr) 
                print(turl)
                isNotURL = False

        if turl[:7] == 'http://' or turl[:8] == 'https://':
            downloadWithURL(turl)
        elif turl[-4:] == '.txt':
            downLoadWithList(turl)
        else:
            tmpstr = 'parameter erro!'
            showMsg(tmpstr)

    elif len(args) == 2:
        turl = args[1]
        print(turl)
        if turl[:7] == 'http://' or turl[:8] == 'https://':
            downloadWithURL(turl)
        elif turl[-4:] == '.txt':
            downLoadWithList(turl)
        
    elif len(args) == 3:
        turl = args[1]
        outpth = args[2]
        print(turl)
        print(outpth)
        if outpth == '1':
            downloadWithURL1Stream(turl)
        elif outpth == '4k':
            downloadWithURLFor4K(turl)
        else:
            if turl[:7] == 'http://' or turl[:8] == 'https://':
                downloadWithURL(turl,outpth)
            elif turl[-4:] == '.txt':
                downLoadWithList(turl,outpth)
            else:
                tmpstr = 'video address erro:%s'%(turl)
                showMsg(tmpstr)
    else:
        tmpstr = 'parameter erro!'
        showMsg(tmpstr)

if __name__ == '__main__':
    msgtool = None
    # tmpstr = 'if you heave any quest,you can content me(gp@woodcol.com)。this tool form:\n\nhttps://fengmm521.taobao.com/\n'
    # showMsg(tmpstr)
    try:
        main(sys.argv)
    except Exception, e:
        print(e)

    tmpstr = 'all download complite!'
    showMsg(tmpstr)
    
    # tmpstr = 'voide is download ok,you can find is in out dir.input any key to end.'
    # showMsg(tmpstr)
    # raw_input()
    # print sys.argv[0]
    # pth = sys.argv[0]
    # print os.path.splitext(pth)
    # print os.path.split(pth)
    # downloadWithURL()
    # makeMoive(u'Anna Kendrick - Cups (Pitch Perfect’s “When I’m Gone”)','1080p','out')
    

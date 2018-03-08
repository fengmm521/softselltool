#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-25 01:37:37
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
from time import sleep, time
import sys, threading
import socket


class KThread(threading.Thread):
    """A subclass of threading.Thread, with a kill()

    method.



    Come from:

    Kill a thread in Python:

    http://mail.python.org/pipermail/python-list/2004-May/260937.html

    """

    def __init__(self, *args, **kwargs):

        threading.Thread.__init__(self, *args, **kwargs)

        self.killed = False

    def start(self):

        """Start the thread."""

        self.__run_backup = self.run

        self.run = self.__run  # Force the Thread to install our trace.

        threading.Thread.start(self)

    def __run(self):

        """Hacked run function, which installs the

        trace."""

        sys.settrace(self.globaltrace)

        self.__run_backup()

        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):

        if why == 'call':

            return self.localtrace

        else:

            return None

    def localtrace(self, frame, why, arg):

        if self.killed:

            if why == 'line':
                raise SystemExit()

        return self.localtrace

    def kill(self):

        self.killed = True

class Timeout(Exception):
    """function run timeout"""

def timeoutTool(seconds):
    """超时装饰器，指定超时时间

    若被装饰的方法在指定的时间内未返回，则抛出Timeout异常"""

    def timeout_decorator(func):

        """真正的装饰器"""

        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):

            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        def _(*args, **kwargs):

            result = []

            new_kwargs = {  # create new args for _new_func, because we want to get the func return val to result list

                'oldfunc': func,

                'result': result,

                'oldfunc_args': args,

                'oldfunc_kwargs': kwargs

            }

            thd = KThread(target=_new_func, args=(), kwargs=new_kwargs)

            thd.start()

            thd.join(seconds)

            alive = thd.isAlive()

            thd.kill()  # kill the child thread
            if alive:
                return None
            else:
                if result:
                    return result[0]
                else:
                    return None

        _.__name__ = func.__name__

        _.__doc__ = func.__doc__

        return _

    return timeout_decorator

def main():
    #shutil.rmtree(dbDir)#删除目录下所有文件
    @timeoutTool(5)  # 限定下面的slowfunc函数如果在5s内不返回就强制抛TimeoutError Exception结束
    def slowfunc(sleep_time):
        a = 1
        import time
        time.sleep(sleep_time)
        return a
     
     
    # print slowfunc(3) #sleep 3秒，正常返回 没有异常

    print slowfunc(6)  # 被终止
 
    
if __name__ == '__main__':  
    main()
    
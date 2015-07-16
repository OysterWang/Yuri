#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import time
import urllib.request
from threading import Thread

class MulThreadDownload(Thread, urllib.request.FancyURLopener):
    """MultiThread download class.

    继承Thread, urllib.request.FancyURLopener
    """
    def __init__(self, threadname, url, filename, blocks_range=0, proxies={}):
        """Init class.

        Args:
            threadname:线程名
            url:下载url
            filename:下载临时文件名
            blocks_range:各线程下载byte范围,例如(0,1024)
            proxies:代理ip

        Returns:
            No return.
        """
        Thread.__init__(self, name=threadname)
        urllib.request.FancyURLopener.__init__(self, proxies)
        self.name = threadname
        self.url = url
        self.filename = filename
        self.blocks_range = blocks_range
        self.downloaded = 0 #各线程已下载size

    def run(self):
        try:
            self.downloaded = os.path.getsize( self.filename )  #检查本线程已经下载的size 
        except OSError: 
            self.downloaded = 0
        
        # rebuild start point
        self.startpoint = self.blocks_range[0] + self.downloaded

        # This part is completed
        if self.startpoint >= self.blocks_range[1]:
            print ('Part %s has been downloaded over.' % self.filename)
            return

        self.oneTimeSize = 16384    #16kByte/time
        print ('Task %s will download from %d byte to %d byte' % (self.name, self.startpoint, self.blocks_range[1]))

        self.addheader("Range", "bytes=%d-%d" % (self.startpoint, self.blocks_range[1]))
        self.urlhandle = self.open( self.url )

        data = self.urlhandle.read( self.oneTimeSize )

        #testfile = open(self.filename+"_test",'ab+')

        while data:
            #testfile.write(data+("\nthis is for "+self.filename+"_test\n").encode())
            filehandle = open( self.filename, 'ab+' )
            filehandle.write(data)
            filehandle.close()
            self.downloaded += len(data)
            data = self.urlhandle.read( self.oneTimeSize )

        #testfile.close()

def getUrlFileSize(url, proxies={}):
    """Get file size

    Args:
        url:下载url
        proxies:代理ip

    Return:
        File size.
    """
    urlHandler = urllib.request.urlopen( url, proxies)
    headers = urlHandler.info()
    totalsize = int(headers.get('Content-Length'))

    return totalsize

def spliteToBlocks(totalsize, blocknumber):
    """Get blocks_ranges
    得到各线程下载的byte范围

    Args:
        totalsize:文件大小
        blocknumber:分多少个block下载，即有多少线程

    Return:
        Blocks_ranges的list.
    """
    blocksize = int(totalsize/blocknumber)
    blocks_ranges = []
    for i in range(0, blocknumber-1):
        blocks_ranges.append((i*blocksize, i*blocksize +blocksize - 1))
    blocks_ranges.append(( blocksize*(blocknumber-1), totalsize -1 ))

    return blocks_ranges

def islive(tasks):
    """Judge whether any thread is live
    仍然有线程在run则返回true

    Args:
        tasks:线程list

    Return:
        有live的线程返回true
    """
    for task in tasks:
        if task.isAlive():
            return True
    return False

class GetStats(object):
    """多线程下载类
    """
    def __init__(self):
        pass
    def download(self, url, output, thread_num, proxies):
        """Download file.

        Download file from url to output local file.

        Args:
            url:下载url
            output:下载生成文件名（不带路径默认在本文件夹中生成）
            thread_num:创建线程数
            proxies:代理ip（比如proxies = {'http': 'http://x.x.x.x:8080'}）

        Return:
            No return.
        """
        totalsize = getUrlFileSize( url, proxies )  #totalsize得到待下载文件大小
        blocks_ranges = spliteToBlocks( totalsize, thread_num ) #创建blocks_ranges list，存放各线程要下载的byte范围

        #初始化和线程数一致数量的threadnames list和filenames list，
        threadnames = [ "thread_%d" % i for i in range(0, thread_num) ] #初始化和线程数一致数量的threadnames list
        filenames = [ "tmpfile_%d" % i for i in range(0, thread_num) ]  #初始化和线程数一致数量的filenames list
        tasks = []  #tasks为线程list

        print('The URL: %s.\nTotal size: %d bytes.\n%d section(s) to be downloaded.\n' %(url, totalsize, thread_num))

        #创建线程run，并存入tasks list中
        for i in range(0,thread_num):
            task = MulThreadDownload( threadnames[i], url, filenames[i], blocks_ranges[i] )
            task.setDaemon( True )
            task.start()
            tasks.append( task )

        time.sleep( 2 )

        #在线程run期间显示下载进度
        while islive(tasks):
            downloaded = sum( [task.downloaded for task in tasks] )
            process = downloaded/float(totalsize)*100
            show = '\rFilesize:%d bytes, Downloaded:%d bytes, Completed:%.2f%%' % (totalsize, downloaded, process)
            sys.stdout.write(show)
            sys.stdout.flush()
            time.sleep( 0.5 )

        #下载线程结束后，循环将临时file写进output文件中
        filehandle = open( output, 'wb+' )
        for i in filenames:
            f = open( i, 'rb' )
            filehandle.write( f.read() )
            f.close()
            try:
                os.remove(i)
                pass
            except:
                pass
        filehandle.close()

if __name__ == '__main__':
    url = "ftp://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
    output = '../data_ref/delegated-apnic-latest.txt'
    getStats = GetStats()
    getStats.download(url, output, 1, {})
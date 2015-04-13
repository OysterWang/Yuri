#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import time
import urllib.request
from threading import Thread

#===============================================================================
# def download(url, output, blocks=6, proxies=local_proxies)
# output:输出文件的全路径，不带路径默认在本文件夹中生成
# blocks:分几块，开几个线程
# proxies:代理地址
#===============================================================================

#代理地址
#local_proxies = {'http': 'http://x.x.x.x:8080'}
'''
其他例子
url = 'ftp://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'  
with urllib.request.urlopen(url,timeout=40) as f:
	print(f.read())
'''
class AxelPython(Thread, urllib.request.FancyURLopener):

    def __init__(self, threadname, url, filename, ranges=0, proxies={}):
        Thread.__init__(self, name=threadname)
        urllib.request.FancyURLopener.__init__(self, proxies)
        self.name = threadname
        self.url = url
        self.filename = filename
        self.ranges = ranges
        self.downloaded = 0

    def run(self):
        try:
            self.downloaded = os.path.getsize( self.filename )
        except OSError:
            self.downloaded = 0

        # rebuild start poind
        self.startpoint = self.ranges[0] + self.downloaded

        # This part is completed
        if self.startpoint >= self.ranges[1]:
            print ('Part %s has been downloaded over.' % self.filename)
            return

        self.oneTimeSize = 16384 #16kByte/time
        print ('task %s will download from %d byte to %d byte' % (self.name, self.startpoint, self.ranges[1]))

        self.addheader("Range", "bytes=%d-%d" % (self.startpoint, self.ranges[1]))

        self.urlhandle = self.open( self.url )

        data = self.urlhandle.read( self.oneTimeSize )
        while data:
            filehandle = open( self.filename, 'ab+' )
            filehandle.write( data )
            filehandle.close()

            self.downloaded += len( data )
            #print ("%s") % (self.name)
            #progress = u'\r...'

            data = self.urlhandle.read( self.oneTimeSize )

def GetUrlFileSize(url, proxies={}):
    urlHandler = urllib.request.urlopen( url, proxies)
    headers = urlHandler.info()
    length = int(headers.get('Content-Length'))
    print('Content-Length is %d bytes' % length)
    return length

def SpliteBlocks(totalsize, blocknumber):
    blocksize = totalsize/blocknumber
    ranges = []
    for i in range(0, blocknumber-1):
        ranges.append((i*blocksize, i*blocksize +blocksize - 1))
    ranges.append(( blocksize*(blocknumber-1), totalsize -1 ))

    return ranges

def islive(tasks):
    for task in tasks:
        if task.isAlive():
            return True
    return False

#blocks=6,proxies=local_proxies
def download(url, output, blocks=1, proxies={}):
    size = GetUrlFileSize( url, proxies )
    ranges = SpliteBlocks( size, blocks )

    threadname = [ "thread_%d" % i for i in range(0, blocks) ]
    filename = [ "tmpfile_%d" % i for i in range(0, blocks) ]

    tasks = []

    print('The URL: %s.\nTotal size: %d bytes.\n%d sections to download.\n' %(url, size, blocks))

    for i in range(0,blocks):
        task = AxelPython( threadname[i], url, filename[i], ranges[i] )
        task.setDaemon( True )
        task.start()
        tasks.append( task )

    time.sleep( 2 )

    while islive(tasks):
        downloaded = sum( [task.downloaded for task in tasks] )
        process = downloaded/float(size)*100
        show = '\rFilesize:%d bytes, Downloaded:%d bytes, Completed:%.2f%%' % (size, downloaded, process)
        sys.stdout.write(show)
        sys.stdout.flush()
        time.sleep( 0.5 )

    filehandle = open( output, 'wb+' )
    for i in filename:
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
    output = 'delegated-apnic-latest'
    download( url, output, blocks=1, proxies={} )
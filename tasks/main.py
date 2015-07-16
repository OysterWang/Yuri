#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

#导入相关包
import get_stats.download_delegated_apnic_latest
import dbutil.importMysql

#其他导入包的方式：

#from get_stats.download_delegated_apnic_latest import GetStats
#此种方法只引入class GetStats(),只需要: 
#getStats = GetStats()

#from get_stats import download_delegated_apnic_latest
#此种方法需要:
#getStats = download_delegated_apnic_latest.GetStats()

"""
主程序入口

"""
if __name__ == '__main__':
    print("sys.path:\n%s" %sys.path)

    url = "ftp://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
    output = "../data_ref/delegated-apnic-latest.txt"
    lineType = "APNIC_CN_IPv4"

    getStats = get_stats.download_delegated_apnic_latest.GetStats()
    getStats.download(url, output, 1, {})	#下载开始
 
    im = dbutil.importMysql.ImportMysql()
    im.importToMysql(output, lineType)		#导入mysql

#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

from get_stats import download_delegated_apnic_latest
from dbutil import importMysql

if __name__ == '__main__':
    url = "ftp://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
    output = "../stats/delegated-apnic-latest"
    lineType = "APNIC_CN_IPv4"
    getStats = download_delegated_apnic_latest.GetStats()
    getStats.download(url, output, 1, {})
 
    im = importMysql.ImportMysql()
    im.importToMysql(output, lineType)
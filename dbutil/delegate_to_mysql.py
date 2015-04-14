#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time

#正则表达式
#registry|cc|type|start|value|date|status[|extensions...]
#例子apnic|JP|ipv4|111.119.0.0|8192|20090702|allocated
pattern = r'^apnic\|CN\|ipv4\|(\d|.)*\|\d*\|\d*\|[a-z]*'
prog = re.compile(pattern)
starttime =time.clock()

#读取下载好的delegated-apnic-latest到lines中，创建新的newlines
with open("../get_stats/delegated-apnic-latest") as f:
    lines = f.readlines()
total_lines = len(lines)
newlines = []

#匹配中的CN ipv4加入到newlines中
ipv4_total = 0
for line in lines:
	if prog.match(line):
		ipv4_total += 1
		#print ("%s\n" %line)
		newlines.append(line)

endtime = time.clock()
print ("Total origin lines: %d rows" %total_lines)
print ("CN IPv4 lines: %d rows." %ipv4_total)
print ("Total cost time: %.3f seconds" %(endtime - starttime))

time.sleep(2)
print ("Begin to import to Mysql")
for line in newlines:
	pass
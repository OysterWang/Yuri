#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time

class DealLines(object):
	"""DealLines
	处理delegated-apnic-latest，得到符合条件的条目list
	"""
	def __init__(self,url,lineType):
		self.url = url
		self.lineType =lineType

	def getFileLines(self):
		"""Get origin lines
		读取下载好的delegated-apnic-latest到lines中。

		Args:

		return:
			originLines。
		"""
		with open(self.url) as f:
		    originLines = f.readlines()
		return originLines

	def useRegex(self):
		"""Regex
		正则表达式匹配：
		registry|cc|type|start|value|date|status[|extensions...]
		例子apnic|JP|ipv4|111.119.0.0|8192|20090702|allocated

		Args:
			self:根据self的lineType决定正则表达式是什么
		Return:
			prog。
		"""
		prog = None
		if self.lineType == "APNIC_CN_IPv4":
			pattern = r'^apnic\|CN\|ipv4\|(\d|.)*\|\d*\|\d*\|[a-z]*'
			prog = re.compile(pattern)
		return prog

	def extractNewlines(self,originLines,needNum):
		"""extractNewlines
		匹配中的CN ipv4加入到newlines中

		Args:
			originLines:原始lines
			needNum:需要的行数，<=0时为全部提取

		Return:
			新的newlines。
		"""
		newlines = []
		prog = self.useRegex()
		flag = 0
		for line in originLines:
			if prog.match(line):	#匹配中的line
				print (line.strip())
				newlines.append(line)	#加入到newlines中
				flag += 1
				if needNum <= 0:
					continue
				elif flag>=needNum:
					print ("Need %d lines." %needNum)
					break
		return newlines

if __name__ == '__main__':
	url = "../stats/delegated-apnic-latest"
	lineType = "APNIC_CN_IPv4"
	
	starttime =time.clock()

	dealLines = DealLines(url,lineType)
	newlines = dealLines.extractNewlines(dealLines.getFileLines(),0)

	endtime = time.clock()

	print ("Total origin lines: %d rows" %len(originLines))
	print ("%s: %d rows." %(lineType, len(newlines)))
	print ("Total cost time: %.3f seconds" %(endtime - starttime))

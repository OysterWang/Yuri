#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
class Analysis(object):
	"""
	"""
	def __init__(self):
		pass

	def anaMaskNum(self,hostnum):
		"""
		#64, 255.255.255.192, 26
		#128, 255.255.255.128, 25
		#256, 255.255.255.0, 24
		#512, 255.255.254.0, 23
		#1024, 255.255.252.0, 22
		#2048, 255.255.248.0, 21
		#
		"""
		if hostnum <= 4294967296:	#2的32次方，IPv4最多能表示的host数量
			return (32 - math.ceil(math.log(hostnum,2)))
		else:
			print ("Host number out of range")
			return -1

	def anaSubnetMask(self,maskNum):
		"""
		"""
		subnetMask = ""
		if maskNum <= 32 and maskNum > 24:
			subnetMask = "255.255.255." + str(256 - 2**(32 - maskNum))
		elif maskNum <= 24 and maskNum > 16:
			subnetMask = "255.255." + str(256 - 2**(24 - maskNum)) + ".0"
		elif maskNum <= 16 and maskNum > 8:
			subnetMask = "255." + str(256 - 2**(16 - maskNum)) + ".0.0"
		elif maskNum <= 8 and maskNum >= 0:
			subnetMask = str(256 - 2**(8 - maskNum )) + ".0.0.0"
		else:
			print ("MaskNum out of range")
			return None
		return subnetMask

if __name__ == '__main__':
	analysis = Analysis()
	print (analysis.anaSubnetMask(analysis.anaMaskNum(8192)))

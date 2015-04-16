#!/usr/bin/python
#-*- coding: utf-8 -*-
import configparser

class Config(object):
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read("../configs/configs.ini")
	def get(self,args1,args2):
		return self.config.get(args1,args2)

if __name__ == "__main__":
	print (Config().get("Mysql","user"))
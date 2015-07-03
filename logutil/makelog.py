import logging

class Makelog():
	"""
	创建日志
	filemode = w 新的，a追加,

	####################
	其他模块引用，只需要
	1.
	from logutil import makelog
	2.
	在其__init__中加入：
	self.ml = makelog.Makelog()
	3.
	方法中加入：
	self.ml.debug(Str)	#或info, warning

	"""
	def __init__(self):
		logging.basicConfig(
			level = logging.DEBUG, 
			format = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s', 
			datefmt = '%a, %d %b %Y %H:%M:%S', 
			filename='../logutil/yuri.log', 
			filemode = 'w')	
	
	def debug(self, debugStr):
		logging.debug(debugStr)

	def info(self, infoStr):
		logging.debug(infoStr)

	def warning(self, warningStr):
		logging.debug(warningStr)


if __name__ == '__main__':
	makelog = Makelog()
	makelog.debug("my makelog")

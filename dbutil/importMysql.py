#!/usr/bin/python
# -*- coding: utf-8 -*-
import mysql.connector
import time

#导入相关包
import analysis.analysis
import dbutil.dealLines
import configs.getConfig
import logutil.makelog

class ImportMysql(object):
    """
    导入mysql类。
    连接数据库部分用##注释。
    导入前需要extractNewlines方法抽取符合条件的条目，并用analysis类计算相应子网掩码。最后数据导入mysql中。
    """

    def __init__(self):
        config = configs.getConfig.Config()
        user = config.get("Mysql","user")
        password = config.get("Mysql","password")
        host = config.get("Mysql","host")
        db = config.get("Mysql","db")
        self.ml = logutil.makelog.Makelog()
        self.dl = None
        ##插入mysql，无数据库时注释掉
        ##self.cnx = mysql.connector.connect(user=user, password=password, host=host, database=db)
        ##self.cursor = self.cnx.cursor()

    def extractNewlines(self, file_url, lineType):
        dl = dbutil.dealLines.DealLines(file_url, lineType)
        newlines = dl.extractNewlines(dl.getFileLines(), 0)   #后边的数字是想要多少符合条件的行,0为所有
        return newlines

    def importToMysql(self, file_url, lineType):        
        #INSERT INTO `delegate_apnic_latest` VALUES 
        #('', 'apnic', 'CN', 'ipv4', '103.251.248.0', '1024', '2013-08-07 00:00:00', 'allocated');

        starttime =time.clock()
        ana = analysis.analysis.Analysis()
        newlines = self.extractNewlines(file_url, lineType)

        print ("Begin to import into Mysql.")
        for line in newlines:
            myset = line.strip().split("|")
            sql = "INSERT INTO delegate_apnic_latest VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}')".format('', myset[0], myset[1], myset[2], myset[3], ana.anaSubnetMask(ana.anaMaskNum(int(myset[4]))), myset[4], myset[5], myset[6])
            print (sql)
            self.ml.debug(sql)
            try:
                pass
                ##self.cursor.execute(sql)   //插入mysql，无数据库时注释掉
            except mysql.connector.Error as err:
                print("insert table 'delegate_apnic_latest' -- failed.")
                print("Error: {}".format(err.msg))
                sys.exit()
        ##插入mysql，无数据库时注释掉
        ##self.cnx.commit()
        ##self.cursor.close()
        ##self.cnx.close()
        endtime = time.clock()
        print ("%d rows." %len(newlines))
        print ("Total cost time: %.3f seconds" %(endtime - starttime))

'''
try:
    cursor.execute(select_sql)
    for (primarykey, registry, cc, linetype, start, linevalue, date, status) in cursor:
        print("primarykey:{}  registry:{}  cc:{} linetype:{} start:{} linevalue:{} date:{} status:{}".format(primarykey, registry, cc, linetype,start, linevalue, date, status))
except mysql.connector.Error as err:
    print("query table 'delegate_apnic_latest' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()
'''
if __name__ == '__main__':
    file_url = "../data_ref/delegated-apnic-latest.txt"
    lineType = "APNIC_CN_IPv4"
    im = ImportMysql()
    im.importToMysql(file_url, lineType)

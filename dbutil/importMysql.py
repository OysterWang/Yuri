import mysql.connector
import sys,os
import time
import sys
sys.path.append('..')

from analysis import analysis
from dbutil import dealLines
from configs import getConfig

class ImportMysql(object):
    dl = None
    def __init__(self):
        config = getConfig.Config()
        user = config.get("Mysql","user")
        password = config.get("Mysql","password")
        host = config.get("Mysql","host")
        db = config.get("Mysql","db")
        self.cnx = mysql.connector.connect(user=user, password=password, host=host, database=db)
        self.cursor = self.cnx.cursor()

    def extractNewlines(self, file_url, lineType):
        dl = dealLines.DealLines(file_url, lineType)
        newlines = dl.extractNewlines(dl.getFileLines(),0)   #后边的数字为想要多少行,0为所有
        return newlines

    def importToMysql(self, file_url, lineType):        
        #INSERT INTO `delegate_apnic_latest` VALUES 
        #('', 'apnic', 'CN', 'ipv4', '103.251.248.0', '1024', '2013-08-07 00:00:00', 'allocated');

        starttime =time.clock()
        ana = analysis.Analysis()
        newlines = self.extractNewlines(file_url, lineType)

        print ("Begin to import into Mysql.")
        for line in newlines:
            myset = line.strip().split("|")
            sql = "INSERT INTO delegate_apnic_latest VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}')".format('', myset[0], myset[1], myset[2], myset[3], ana.anaSubnetMask(ana.anaMaskNum(int(myset[4]))), myset[4], myset[5], myset[6])
            print (sql)
            try:
                self.cursor.execute(sql)
            except mysql.connector.Error as err:
                print("insert table 'delegate_apnic_latest' -- failed.")
                print("Error: {}".format(err.msg))
                sys.exit()

        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()
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
    file_url = "../stats/delegated-apnic-latest"
    lineType = "APNIC_CN_IPv4"
    im = ImportMysql()
    im.importToMysql(file_url, lineType)

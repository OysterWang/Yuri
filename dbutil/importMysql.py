import mysql.connector
import sys,os
import time
from dealLines import DealLines

user = 'root'
pwd = 'Comeonbaby'
host = '123.57.58.85'
db = 'yuri'

select_sql = "SELECT * FROM delegate_apnic_latest"
 
cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

url = "../stats/delegated-apnic-latest"
lineType = "APNIC_CN_IPv4"

dealLines = DealLines(url,lineType)
newlines = dealLines.extractNewlines(dealLines.getFileLines(),0)

#INSERT INTO `delegate_apnic_latest` VALUES 
#('', 'apnic', 'CN', 'ipv4', '103.251.248.0', '1024', '2013-08-07 00:00:00', 'allocated');

starttime =time.clock()
print ("Begin to import into Mysql.")

for line in newlines:
    myset = line.strip().split("|")
    sql = "INSERT INTO delegate_apnic_latest VALUES ('{}', '{}', '{}', '{}', '{}', {}, '{}', '{}')".format('', myset[0], myset[1], myset[2], myset[3], myset[4], myset[5], myset[6])
    print (sql)
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print("insert table 'delegate_apnic_latest' -- failed.")
        print("Error: {}".format(err.msg))
        sys.exit()
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
cnx.commit()
cursor.close()
cnx.close()

endtime = time.clock()
print ("%d rows." %len(newlines))
print ("Total cost time: %.3f seconds" %(endtime - starttime))

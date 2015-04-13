import urllib  
import urllib2  
import requests

print "downloading delegated-apnic-latest" 
url = 'ftp://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'  
urllib.urlretrieve(url, "delegated-apnic-latest")


import urllib2 
print "downloading with urllib2"
url = 'ftp://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest' 
f = urllib2.urlopen(url)  
data = f.read()  
with open("delegated-apnic-latest", "wb") as code:      
    code.write(data)
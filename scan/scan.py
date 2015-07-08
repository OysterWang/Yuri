#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket, sys, thread, time

openPortNum = 0
socket.setdefaulttimeout(3)

def usage():
    print '''Usage:
    Scan the port of one IP: python port_scan_multithread.py -o <ip>
    Scan the port of one IP: python port_scan_multithread.py -m <ip1, ip2, ip3, ip4 ...>
    '''
    print 'Exit'
    sys.exit(1)

def socket_port(ip, PORT):
    global openPortNum
    if PORT > 65535:
        print 'Port scanning beyond the port range, interrupt to scan'
        sys.exit(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ##s.settimeout(0.1)
    result = s.connect_ex((ip, PORT))
    if(result == 0):
        print ip, PORT,'is open'
        openPortNum += 1
    s.close()

def start_scan(IP):
    for port in range(0, 65535+1):
        thread.start_new_thread(socket_port, (IP, int(port)))
        time.sleep(0.006)

if __name__ == '__main__':
    t = 0
    if len(sys.argv)<2 or sys.argv[1] == '-h':
        usage()
    elif sys.argv[1] == '-o':
        ONE_IP = raw_input('Please input ip of scanning: ')
        t = time.time()
        start_scan(ONE_IP)
    elif sys.argv[1] == '-m':
        MANY_IP = raw_input('Please input many ip of scanning: ')
        IP_SEG = MANY_IP.split(',')
        t = time.time()
        for i in IP_SEG:
            start_scan(i)

    print
    print 'total open port is %s, scan used time is: %f ' % (openPortNum, time.time()-t)

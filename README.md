1.
tasks/main.py程序入口

2.
configs配置文件

3.
logutil日志功能，日志存放位置

4.
stats存放下载相关文档delegated-apnic-latest.txt

5.
自动下载ftp://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest
相关：download_delegated_apnic_latest.py

6.
抽取apnic|CN|ipv4|202.97.16.0|4096|19980322|allocated 类型的条目，并计算出子网掩码，存入mysql
相关：dbutil


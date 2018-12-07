#!/usr/bin/env python
# -*- coding: utf_8 -


# import Pyro.core
# import Pyro.naming
# Pyro.core.initClient(banner = 0)
# obj = Pyro.core.getProxyForURI("PYROLOC://192.168.2.136:8888/GetFiles")

# print "start",obj

# data = obj.getFiles()

# print "end",data

# file = obj.makeFile("b.txt")


import requests
import os
import json
from config import config
import requests_toolbelt
import time
import os
import sys
import datetime
total = os.path.getsize(config["file_name"])
 
def humanbytes(B):
    'Return the given bytes as a human friendly KB, MB, GB, or TB string'
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776
 
    if B < KB:
        return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B/KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B/MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B/GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B/TB)
 
def progres(num, Sum):
    """
    显示上传进度条
    num：已上传大小
    Sum：文件总大小
    #l：定义进度条大小
    """
    bar_length = 50 # 定义进度条大小
    percent = float(num) / float(Sum)
    hashes = '=' * int(percent * bar_length)  # 定义进度显示的数量长度百分比
    spaces = ' ' * (bar_length - len(hashes))  # 定义空格的数量=总长度-显示长度
 
    sys.stdout.write(
        "\rsend: [%s] %d%%  %s/%s " % (hashes + spaces, percent * 100, humanbytes(num), humanbytes(Sum)))  # 输出显示进度条
    sys.stdout.flush()  # 强制刷新到屏幕

def my_callback(monitor):
    # Your callback function
    print monitor.bytes_read
    progres(monitor.bytes_read,total)

#上传文件到服务器
print "upload..."
m = requests_toolbelt.MultipartEncoder(fields={'file': ('file.zip',open(config["file_name"], 'rb'))},boundary='---------------------------7de1ae242c06ca')
m = requests_toolbelt.MultipartEncoderMonitor(m, my_callback)
#file = {'file': open(config["file_name"],'rb')}
req_headers = {'Content-Type': m.content_type,'path':'2016/07/09/5ASD5SDFASDFASDF/{}.zip'.format(time.time()),}
starttime = datetime.datetime.now()
r = requests.post(config["upload_url"], data=m, headers=req_headers)
endtime = datetime.datetime.now()
print ""
print "==================total: "+str((endtime - starttime).seconds)+" seconds"
#r = requests.post(config["upload_url"], files=file)
print "deploy..."
r = requests.post(config["deploy_url"], data = r.text)
print(r.text)
raw_input("success..")
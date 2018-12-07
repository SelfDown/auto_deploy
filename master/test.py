#!/usr/bin/env python
# -*- coding: utf_8 -
import requests
import requests_toolbelt
from config import config

m = requests_toolbelt.MultipartEncoder(fields={'file': ('filename',open(config["file_name"], 'rb'))},boundary='---------------------------7de1ae242c06ca')

import time
import os
import sys

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

m = requests_toolbelt.MultipartEncoderMonitor(m, my_callback)

req_headers = {'Content-Type': m.content_type,'path':'2016/07/09/5ASD5SDFASDFASDF/{}.zip'.format(time.time()),}

r = requests.post(config["upload_url"], data=m, headers=req_headers)
# 
# This is misc functions
# 
import os, sys
import urllib.parse, urllib.request
import time
import re

def baiduSearch(keyword):
    p = {'wd': keyword}
    return "http://www.baidu.com/s?"+urllib.parse.urlencode(p)

def note(Str):
    fileDir = '/home/mark/lab/bread/log/notes.txt'
    thisTime = time.strftime('[%Y-%m-%d %H:%M:%S] ',time.localtime())
    text = thisTime + Str
    f = open(fileDir,'a')
    f.write(text + '\n')
    f.close()
    return text

def printLog(Str): 
    thisTime = time.strftime('[%Y-%m-%d %H:%M:%S] ',time.localtime())
    print(thisTime + str(Str))

def get_home_ip():
    reg = 'fk="\d+\.\d+\.\d+\.\d+" '
    url = 'http://www.baidu.com/s?wd=gongwangip'
    result = re.search(reg, str(urllib.request.urlopen(url).read())).group(0)
    result = re.search('\d+\.\d+\.\d+\.\d+',result).group(0)
    return result

def translate(word):
    result1 = os.popen('sdcv -n ' + word).readlines()
    if not re.match(u'^Found 1 items.*', result1[0]):
        return '[Not Found]'
    res = ''
    for i in range(4,len(result1)):
        res += result1[i]
    res = re.sub(u'\[.+\]','',res) 
    res = res.replace('\n','')
    res = res.replace('//','\r')
    return res

# coding=utf-8
import datetime
import re

if "1[0-7]:" in str(datetime.datetime.now()):
    print datetime.datetime.now()

cp = re.compile('0[0-6]:')
group = re.findall(cp, str(datetime.datetime.now()))
print group
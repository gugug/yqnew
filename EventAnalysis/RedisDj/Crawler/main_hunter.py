# coding=utf-8
import datetime

from EventAnalysis.RedisDj.Crawler.down_username import *
from MoblieWeibo import MoblieWeibo
from put_username import *


def main_hunter():
    account = {1: ('gwcrawler1@126.com', '321456'),
               2: ('shuqunkeji@sina.com', 'shujuwajue'),
               3: ('zgryejmd@sina.cn', 'tttt5555'), 4: ('nowccqpq@sina.cn', 'tttt5555'),
               5: ('odlmyfbw@sina.cn', 'tttt5555'), 6: ('ajjqbwkm@sina.cn', 'tttt5555'),
               7: ('coiarurd@sina.cn', 'tttt5555'), 8:('zcsicrod@sina.cn', 'tttt5555'),
               9: ('cjmnkaok@sina.cn', 'tttt5555')
               }
    # 2: ('iydt30@mailnesia.com', 'pp9999'), 4: ('gdufsiiip@sina.com', 'shujuwajue'), 11: ('oaax1n@mailnesia.com', 'pp9999')
    # 12: ('nrrfdzpc@sina.cn', 'tttt5555'), 14: ('fwg4cp@mailnesia.com', 'pp9999'),
    # 15: ('gxyb5w@mailnesia.com', 'pp9999'), 16: ('agfpuo@mailnesia.com', 'pp9999')

    main_put()
    # MoblieWeibo().login(account[1][0], account[1][1])
    start_time = datetime.datetime.now()
    # 主机会put, 其他机器只管down就好
    main_down_stats(7, 1)  # 分机数目, 机器编号
    print '总共用时间为： ', datetime.datetime.now() - start_time

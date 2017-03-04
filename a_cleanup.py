#coding=utf-8
import redis

__author__ = 'yc'

from db_connection import *
import shutil
import re
import chardet



class Clean(Database):
    def __init__(self):
        Database.__init__(self)
        self.path_list = ['../yqnew/documents/topic','../yqnew/documents/topic1','../yqnew/static/data']

    def clean(self):
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql1 = "DELETE FROM event"
            cur.execute(sql1)

        for i in self.path_list:
            if os.path.exists(i):
                print 'cleaning', i
                shutil.rmtree(i)
        os.mkdir(JSON_DIR)
        # os.mkdir(DOC_DIR)
        # os.mkdir(DOC_DIR.replace('topic','topic1'))
        # shutil.rmtree('../yqproject/static/sna')

        db = redis.Redis(host='192.168.235.21', port=6379, db=0)  #
        db.flushdb()




Clean().clean()
# print JSON_DIR




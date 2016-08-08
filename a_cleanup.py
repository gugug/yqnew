__author__ = 'yc'

from db_connection import *
import shutil

class Clean(Database):
    def __init__(self):
        Database.__init__(self)

    def clean(self):
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql1 = "DELETE FROM event"
            cur.execute(sql1)
        shutil.rmtree('../yqnew/documents/topic')
        # shutil.rmtree('../yqproject/static/sna')

Clean().clean()
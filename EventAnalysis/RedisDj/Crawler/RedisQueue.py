# coding=utf-8
__author__ = 'gu'

import redis

class RedisQueue(object):

    def __init__(self, name, namespace=''):
        """
        链接数据库
        :param name:
        :param namespace:
        :return:
        """
        self.__db = redis.Redis(host='192.168.235.21', port=6379, db=0)   #  192.168.235.21  127.0.0.1
        self.key = '%s%s' % (namespace, name)
        print self.key

    def qsize(self):
        """
        对应键的大小
        :return:
        """
        return self.__db.llen(self.key)

    def empty(self):
        """
        是否为空
        :return:
        """
        return self.qsize() == 0

    def put(self, item):
        """
        放进对应键的值
        :param item:
        :return:
        """
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):

        """Remove and return an item from the queue.
        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""

        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
            # Redis Blpop 命令移出并获取列表的第一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。
            # 如果列表为空，返回一个 nil 。 否则，返回一个含有两个元素的列表，第一个元素是被弹出元素所属的 key ，第二个元素是被弹出元素的值。
        else:
            # Redis Lpop 命令用于移除并返回列表的第一个元素。
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]

        return item

    # def get_nowait(self):
    #
    #     """Equivalent to get(False)."""
    #     return self.get(False)

    def get_lrange(self, start, end):
        """
        取对应位置的值
        :param end:
        :return:
        """
        return self.__db.lrange(self.key, start, end)

    def del_key(self):
        """
        删除键
        :return:
        """
        self.__db.delete(self.key)

    def exists_key(self, keys):
        return self.__db.exists(keys) == 1

    def get_key(self,key_pattern):
        return self.__db.keys(key_pattern)

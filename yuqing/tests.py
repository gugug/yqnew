#coding=utf-8
from django.test import TestCase

# Create your tests here.
import os

print os.path.dirname(os.path.abspath(__file__))
#/home/yc/PycharmProjects/yqnew/yuqing,多个dirname即逐级递减,__file__即本文件
#abspath为/home/yc/PycharmProjects/yqnew/yuqing/test.py
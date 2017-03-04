# coding=utf-8
import re
from multiprocessing import Manager
from yqnew.settings import *

__author__ = 'gu'


class StatsAll:

    manager = Manager()
    default_area_dict = manager.dict()
    default_age_dict = manager.dict()
    default_sex_dict = manager.dict()

    def __init__(self):
        self.set_dict()

    def set_dict(self):
        """
        设置地区字典
        :return:
        """
        area_num_dict = {
            '北京': 0, '上海': 0, '天津': 0, '重庆': 0,
            '安徽': 0, '福建': 0, '甘肃': 0, '广东': 0,
            '广西': 0, '贵州': 0, '海南': 0, '河北': 0,
            '河南': 0, '湖北': 0, '湖南': 0, '黑龙江': 0,
            '江苏': 0, '江西': 0, '吉林': 0, '内蒙古': 0,
            '辽宁': 0, '宁夏': 0, '青海': 0, '山西': 0,
            '山东': 0, '四川': 0, '西藏': 0, '新疆': 0,
            '云南': 0, '浙江': 0, '陕西': 0, '台湾': 0,
            '香港': 0, '澳门': 0, '海外': 0, '其他': 0
        }

        age_num_dict = {
            '80年以前': 0,
            '80-85': 0,
            '86-90': 0,
            '91-95': 0,
            '95以后': 0,
            '未知年龄': 0
        }
        sex_num_dict = {
            '男': 0,
            '女': 0,
            '未知性别': 0
        }
        for area_key, area_value in area_num_dict.items():
            self.default_area_dict.setdefault(area_key, area_value)
        for age_key, age_value in age_num_dict.items():
            self.default_age_dict.setdefault(age_key, age_value)
        for sex_key, sex_value in sex_num_dict.items():
            self.default_sex_dict.setdefault(sex_key, sex_value)

    def stats_area(self, area):
        """
        只对省份进行统计
        :param area:
        :return:
        """
        result = re.split(' ', area)
        province = result[0]
        if province in self.default_area_dict.keys():
            self.default_area_dict[province] += 1
        else:
            province = '其他'
            self.default_area_dict[province] += 1

    def stats_age(self, age):
        result = re.split('-', age)
        if str.isdigit(result[0]):
            year = int(result[0])
            if year == 0 or year == 1:
                self.default_age_dict['未知年龄'] += 1
            elif year < 1980:
                self.default_age_dict['80年以前'] += 1
            elif year <= 1985:
                self.default_age_dict['80-85'] += 1
            elif year <= 1990:
                self.default_age_dict['86-90'] += 1
            elif year <= 1995:
                self.default_age_dict['91-95'] += 1
            else:
                self.default_age_dict['95以后'] += 1
        else:
            self.default_age_dict['未知年龄'] += 1

    def stats_sex(self, sex):
        if sex == '男':
            self.default_sex_dict['男'] += 1
        elif sex == '女':
            self.default_sex_dict['女'] += 1
        else:
            self.default_sex_dict['未知性别'] += 1

    def print_all(self):
        """
        打印统计结果
        :return:
        """
        for area_key, area_value in self.default_area_dict.items():
            print area_key, area_value
        for age_key, age_value in self.default_age_dict.items():
            print age_key, age_value
        for sex_key, sex_value in self.default_sex_dict.items():
            print sex_key, sex_value

    def save_all(self, path, YOURID):
        """
        保存txt文本
        :param event:
        :return:
        """
        time = re.split('/', path)
        file_name = path.replace('/'+time[-1], '')
        if os.path.exists(file_name):
            pass
        else:
            os.mkdir(file_name)
        stats_txt = open(file_name + '/stats' + str(YOURID) + '.txt', 'w+')

        for sex_key, sex_value in self.default_sex_dict.items():
            # print sex_key,sex_value
            stats_txt.write(str(sex_key) + ',' + str(sex_value) + '\n')

        for area_key, area_value in self.default_area_dict.items():
            # print area_key, area_value
            stats_txt.write(str(area_key) + ',' + str(area_value) + '\n')

        for age_key, age_value in self.default_age_dict.items():
            # print age_key, age_value
            stats_txt.write(str(age_key) + ',' + str(age_value) + '\n')

        stats_txt.close()
        print '统计文本写入完毕 '

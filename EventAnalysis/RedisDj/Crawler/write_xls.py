# coding=utf-8
import json

__author__ = 'gu'

import xlwt
import xlrd
import os

def write_data_to_excel(file_name, result_list, name):
    """

    :param file_name: xls所在的路径
    :param result_list: 嵌套元组的形式[(,), (,),]
    :param name: 生成的名字和sheet名字 map, age
    :return:
    """

    wbk = xlwt.Workbook('utf-8')
    sheet = wbk.add_sheet(name, True)
    for i in xrange(len(result_list)):
        for j in xrange(len(result_list[i])):
            sheet.write(i,j,result_list[i][j])
    xls_file = os.path.join(file_name, name+'.xls')
    print xls_file
    wbk.save(xls_file)
    return xls_file



def dump_map_json(file_name, xls_file):
    """
    生成age distribution ,map的json文件
    :param xls_file: xls文件的路径
    :return:
    """
    map_list = []
    xls = xlrd.open_workbook(xls_file)
    table = xls.sheet_by_index(0)
    name_list = table.col_values(0, 0)
    value_list = table.col_values(1, 0)
    for i in range(0, len(name_list)):
        map_dict = {'name': name_list[i], 'value': value_list[i]}
        map_list.append(map_dict)
    data_dict = {'map': map_list}
    map_json = json.dumps(data_dict, separators=(',', ':'))
    map_file = open(os.path.join(file_name,'map.json'), 'w+')
    map_file.writelines(map_json)
    map_file.close()
    print 'finish writing map json'
    return True


def dump_age_json(file_name, age_num_list):
    """
    :param file_name: 保存json的路径，
    :param age_num_list: 年龄对应的数据, 顺序为：
    ['80年以前',    '80-85',    '86-90',    '91-95',    '95以后',    '未知年龄']
    :return:
    """

    age_dict = {}
    age_dict.setdefault('ageDistribution', age_num_list)
    age_json = json.dumps(age_dict, separators=(',', ':'))
    age_file = open(os.path.join(file_name, 'age_distribution.json'), 'w+')
    age_file.writelines(age_json)
    age_file.close()
    print 'finish writing age json'
    return True

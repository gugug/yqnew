# coding=utf-8
import os
import re
from time import sleep
from yqnew.settings import BASE_DIR
import sys
from write_xls import *
sys.setrecursionlimit(1000000)  # 设置为一百万次递归


__author__ = 'gu'


word_num_dict = {

    '男': 0,
    '女': 0,
    '未知性别': 0,

    '北京': 0, '上海': 0, '天津': 0, '重庆': 0,
    '安徽': 0, '福建': 0, '甘肃': 0, '广东': 0,
    '广西': 0, '贵州': 0, '海南': 0, '河北': 0,
    '河南': 0, '湖北': 0, '湖南': 0, '黑龙江': 0,
    '江苏': 0, '江西': 0, '吉林': 0, '内蒙古': 0,
    '辽宁': 0, '宁夏': 0, '青海': 0, '山西': 0,
    '山东': 0, '四川': 0, '西藏': 0, '新疆': 0,
    '云南': 0, '浙江': 0, '陕西': 0, '台湾': 0,
    '香港': 0, '澳门': 0, '海外': 0, '其他': 0,

    '80年以前': 0,
    '80-85': 0,
    '86-90': 0,
    '91-95': 0,
    '95以后': 0,
    '未知年龄': 0
}
word_list = [

    '男',
    '女',
    '未知性别',

    '北京', '上海', '天津', '重庆',
    '安徽', '福建', '甘肃', '广东',
    '广西', '贵州', '海南', '河北',
    '河南', '湖北', '湖南', '黑龙江',
    '江苏', '江西', '吉林', '内蒙古',
    '辽宁', '宁夏', '青海', '山西',
    '山东', '四川', '西藏', '新疆',
    '云南', '浙江', '陕西', '台湾',
    '香港', '澳门', '海外', '其他',

    '80年以前',
    '80-85',
    '86-90',
    '91-95',
    '95以后',
    '未知年龄'
]

# def read_txt(file_name):
#     sum = 0
#     participants_txt = os.path.join(BASE_DIR, 'documents', file_name)
#     print participants_txt
#     txt = open(participants_txt, 'r')
#     words = txt.readlines()
#     for i in range(len(words)):
#         words[i] = words[i].replace('\n','')
#         words[i] = re.sub('.*?,','',words[i])
#         sum += int(words[i])
#     print sum


def combine_txt(file_name, slave_num):
    """
    等全部slave的txt上传完毕后，master进行统计生成总的txt，如果没有上传完全，则等待上传
    :param file_name:txt对应的文件夹目录
    :param slave_num:slave的数量
    :return:
    """
    stats_txt = os.path.join(BASE_DIR, 'documents', file_name)
    print stats_txt
    no_time_path = ''
    group = file_name.split('/')
    for i in range(1,len(group)-1,1):
        no_time_path += '/'+group[i]
    print no_time_path
    file_num = len(get_file_list(no_time_path, []))

    print "文本数目",file_num
    if file_num == slave_num:
        for t in range(1,file_num+1):
            txt = open(no_time_path + '/stats' + str(t)+'.txt', 'r')
            words = txt.readlines()
            for i in range(len(words)):
                words[i] = words[i].replace('\n', '')
                wn = words[i].split(',')
                if wn[0] in word_num_dict.keys():
                    word_num_dict[wn[0]] += int(wn[1])
                else:
                    pass
    else:
        print "休眠60s, 等待其他上传...."
        sleep(30)
        combine_txt(file_name, slave_num)

    areas_list = []
    age_list = []
    sex_list = []
    age_json_list = []
    for w in word_list[0:3]:
        sex_list.append((w, word_num_dict[w]))
    for w in word_list[3:39]:
        areas_list.append((w, word_num_dict[w]))
    for w in word_list[39:-1]:
        age_num = word_num_dict[w]
        age_list.append((w, age_num))
        age_json_list.append(age_num)

    map_xls_file = write_data_to_excel(file_name,areas_list,'map')
    write_data_to_excel(file_name,age_list,'age')

    json_path = no_time_path.replace('documents/topic1','static/data')
    print 'json_path', json_path
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    dump_map_json(json_path, map_xls_file)
    dump_age_json(json_path, age_json_list)
    print "统计文本整合成xls, json完毕完毕"


def get_file_list(dir, file_list):
    """
    获取事件参与人的绝对路径
    :param dir: 缩小范围查找的路径
    :param file_list: 绝对路径
    :return:
    """
    new_dir = dir
    if os.path.isfile(dir):
        file_list.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹
            if s == "repost_path.txt" or s == "comment.txt" or s == 'age.xls' or s == 'map.xls':
                continue
            new_dir = os.path.join(dir, s)
            get_file_list(new_dir, file_list)
    return file_list


# combine_txt('/home/monkeys/PycharmProjects/yqnew/documents/topic1/【婆婆因儿媳未能生下男孩 定期坐高铁上门打人】/', 4)
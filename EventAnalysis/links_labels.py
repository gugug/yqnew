# coding=utf-8
"""
Author = Eric_Chan
Create_Time = 2016/03/25
introduction:
分析博文的转发趋势,获得用户之间的关系权值
"""

import re
import xlrd
import xlwt
import os
import chardet
import random
import json
from yqnew.settings import *
import datetime


def walk_path(root_dir):
    """
    :param root_dir: 文件夹路径
    :return: 子文件路径以及子文件对应的上一级路径
    """
    path_tuple_list = []
    list_dirs = os.walk(root_dir)
    for root, dirs, files in list_dirs:
        print files
        if "label_link.xls" in files:  # 若存在该excel表 表示已分析过 跳过该文件夹
            continue
        for f in files:
            # if f.startswith('.'):  # 排除隐藏文件
            #     continue
            if f.startswith('repost'):
                path_tuple_list.append((root, os.path.join(root, f)))
    print 'walk_path', path_tuple_list
    return path_tuple_list


def load_data_old(file_name):
    """
    :param file_name:
    :return:首发博文,首发博文的用户,路径用户名列表,最后发表言论博文
    """
    file1 = open(file_name)
    # line = file1.readline().decode('utf-8')
    lines = file1.readlines()
    road_list = []
    # print lines
    for line in lines[:-1]:
        if line.replace('\n', ''):
            road_list.append(line.strip().decode('utf-8'))
    # for i in road_list:
    #     print i
    # #
    # # while line:
    # #     if line.strip():
    # #         road_list.append(line.strip())
    # #         line = file1.readline().decode('utf-8')
    # #     else:
    # #         line = file1.readline().decode('utf-8')
    # print road_list, "*****"
    return road_list


def write_data(file_name, label_list, link_list, size_list):
    """
    把转发路径txt的数据写入xls文件,在create_xls中使用
    :param file_name: xls文件名
    :param label_list: 昵称列表
    :param link_list: 链接列表
    :param size_list: 规模列表
    :return:
    """
    file_rpt = xlwt.Workbook('utf-8')
    nodes = file_rpt.add_sheet('nodes')
    edges = file_rpt.add_sheet('edges')
    nodes.write(0, 0, 'id')
    nodes.write(0, 1, 'x')
    nodes.write(0, 2, 'y')
    nodes.write(0, 3, 'label')
    nodes.write(0, 4, 'size')
    edges.write(0, 0, 'sourceId')
    edges.write(0, 1, 'targetId')
    print len(label_list)
    print len(link_list)
    print len(size_list)
    for i in range(len(label_list)):
        nodes.write(i + 1, 0, i)
        nodes.write(i + 1, 1, random.normalvariate(1, 5))
        nodes.write(i + 1, 2, random.normalvariate(1, 5))
        nodes.write(i + 1, 3, label_list[i])
        nodes.write(i + 1, 4, size_list[i])
    for i in range(len(link_list)):
        edges.write(i + 1, 0, link_list[i][0])
        edges.write(i + 1, 1, link_list[i][1])
    file_rpt.save(file_name)
    return file_name

# 暂时没用,仅保留
def write_data_old(file_name, label_list, link_list):
    """
    将 节点对应的用户名列表 和 节点-节点-权值列表 分别写入一个 xls 的 2个sheet
    :param file_name: xls的文件名
    :param label_list: 标签列表
    :param link_list: 节点-节点-权值列表
    """
    file_0 = xlwt.Workbook(encoding='utf-8')
    table_0 = file_0.add_sheet('label')
    table_1 = file_0.add_sheet('link')
    table_0.write(0, 0, 'node')
    table_0.write(0, 1, 'label')
    for i in range(label_list.__len__()):
        table_0.write(i + 1, 0, label_list.index(label_list[i]))
        table_0.write(i + 1, 1, label_list[i])
    table_1.write(0, 0, 'from')
    table_1.write(0, 1, 'to')
    table_1.write(0, 2, 'weight')
    for i in range(link_list.__len__()):
        table_1.write(i + 1, 0, link_list[i][0])
        table_1.write(i + 1, 1, link_list[i][1])
        table_1.write(i + 1, 2, link_list[i][2])
    file_0.save(file_name)


def link_label(road_list):
    """
    处理txt数据,获取昵称,链接,规模的列表
    :param road_list: txt的上级目录
    :return:
    """
    pattern_name = re.compile(u'@([^@]*?)[ |:|：]')  # 匹配转发路径中出现的用户名
    link_list = []
    label_list = []
    size_list = []
    for road in road_list:
        # print 'road', road, '\n'
        name_list = re.findall(pattern_name, road)
        # print '\n'.join(name_list)
        # for i in name_list:
        # print 'name',i
        if len(name_list) > 1:
            if name_list[0] not in label_list:
                size = 7
                label_list.append(name_list[0])
                size_list.append(size)
            else:
                index = label_list.index(name_list[0])
                size_list[index] += 2

            if name_list[1] not in label_list:
                size = 7
                label_list.append(name_list[1])
                link_list.append([label_list.index(name_list[0]), label_list.index(name_list[1]), 20])
                size_list.append(size)
            else:
                index = label_list.index(name_list[1])
                size_list[index] += 2

            for i in range(2, len(name_list)):
                # print i
                if name_list[i] not in label_list:
                    size = 7
                    label_list.append(name_list[i])
                    size_list.append(size)
                    num1 = label_list.index(name_list[i])
                    num0 = label_list.index(name_list[i - 1])
                    # print 'from', name_list[i - 1], num0, 'to', name_list[i], num1
                    # if name_list[1] not in label_list:
                    #     label_list.append(name_list[1])
                    #     print chardet.detect(label_list[0])
                    #     print chardet.detect(name_list[i])
                    temp_list = [num0, num1, 20]
                    # print temp_list
                    link_list.append(temp_list)
                else:
                    index = label_list.index(name_list[i])
                    size_list[index] += 2

    for i in range(len(size_list)):
        if size_list[i]>70:
            size_list[i] = 70
    return link_list, label_list, size_list


def create_xls(topic_time_path):
    """
    根据txt创建xls文件
    :param topic_time_path: txt文件的上级目录
    :return:
    """
    # paths = walk_path('../documents/topic')
    file_name = ''
    paths = walk_path(topic_time_path)
    print 'paths', paths
    for path in paths:
        print path[1],
        # try:
        blog_roads = load_data_old(path[1])
        links, labels, size = link_label(blog_roads)
        # except:
        #     print "这个txt的格式有问题"
        #     continue
        # for l in labels:
        #     print labels.index(l), l
        # for l in links:
        #     print l
        # print 'done'
        file_name = write_data(path[0] + '/label_link.xls', labels, links, size)
    return file_name


def load_data(file_name, sheet_index=None):
    """
    读取xls文件,获得矩阵.
    :param file_name: xls文件路径
    :param sheet_index: xls 打开的sheet序号
    :return: 除去表头后的二元列表
    """
    if sheet_index is None:
        sheet_index = 0
    data = xlrd.open_workbook(file_name)  # 打开xls
    table = data.sheet_by_index(sheet_index)  # 打开sheet1
    all_data = table._cell_values  # 将所有数据 以二元列表进行构造
    all_data = all_data[1:]  # 除去表头
    for i in range(all_data.__len__()):  # 将表中数据的整数转化为int类型
        for j in range(all_data[0].__len__()):

            try:
                if all_data[i][j] == int(all_data[i][j]):
                    all_data[i][j] = int(all_data[i][j])
            except ValueError:
                continue
    return all_data

def write_history_json(path):
    """
    用于写入7个网络图
    :return:
    """
    print "writing history json"
    count = 0
    event_title = path.split('/')[-2]
    folder_path = os.path.join(JSON_DIR,event_title)
    if os.path.exists(folder_path):
        for paths, folders, files in os.walk(folder_path):
            for f in files:
                if f.startswith('repost'):
                    count += 1
        low = 7- count
        if low == 0:
            low = 1
        for i in range(low, 7):
            print 'writing json No.',i
            older_file = open(os.path.join(JSON_DIR,event_title, 'repost_path%s.json' % str(i)),'w+')
            newer_file = open(os.path.join(JSON_DIR,event_title, 'repost_path%s.json' % str(i+1)),'r+')
            content = newer_file.readlines()
            # print older_file, newer_file,content
            older_file.writelines(content)
            newer_file.close()
            older_file.close()
    else:
        os.mkdir(folder_path)

    return True


def write_json(file_name, path):
    """
    读xls数据生成json数据(repost_path1-7.json和name_list.json)
    :param file_name:
    :return:
    """
    print 'name list json', file_name
    print 'json path', path
    nodes_list = []
    edges_list = []
    name_list = []
    cate_list = []
    event_title = path.split('/')[-2]
    data = xlrd.open_workbook(file_name)
    nodes_sheet = data.sheet_by_index(0)
    edges_sheet = data.sheet_by_index(1)
    id = nodes_sheet.col_values(0, 1)  # lists
    x = nodes_sheet.col_values(1, 1)
    y = nodes_sheet.col_values(2, 1)
    label = nodes_sheet.col_values(3, 1)
    size = nodes_sheet.col_values(4, 1)
    source_id = edges_sheet.col_values(0, 1)
    target_id = edges_sheet.col_values(1, 1)
    for i in range(len(size)):
        if size[i]>40:
            name_list.append(label[i])
            cate_dict = {'id':id[i],'name':label[i]}
            cate_list.append(cate_dict)
    if len(cate_list) < 1:
        cate_list.append({'id':0,'name':'默认分组'})

    for i in range(len(id)):
        a = random.randint(0,len(cate_list)-1)
        nodes_dict = {'id': id[i], 'x': x[i], 'y': y[i], 'label': label[i], 'size': size[i],'cateNum':a}
        nodes_list.append(nodes_dict)

    for j in range(len(source_id)):
        edges_dict = {'sourceID': source_id[j], 'targetID': target_id[j]}
        edges_list.append(edges_dict)
    view_dict = {'view': {'time':str(datetime.datetime.date(datetime.datetime.now())),
                          'cates':cate_list,'nodes': nodes_list, 'edges': edges_list}}
    encode_json = json.dumps(view_dict, separators=(',', ':'))
    json_file = open(os.path.join(JSON_DIR, event_title,'repost_path7.json'), 'w+')
    json_file.writelines(encode_json)
    json_file.close()
    print 'finish writing repost_path json'

    name_dict = {'nameList':name_list}
    name_json = json.dumps(name_dict,separators=(',',':'))
    name_file = open(os.path.join(JSON_DIR,event_title,'name_list.json'),'w+')
    name_file.writelines(name_json)
    name_file.close()
    print 'finish writing name list json'
    return True


def main_network(topic_time_path):
    path_list = []
    dir_list = []
    create_xls(topic_time_path)
    # print file_name

    for root, dir, file in os.walk(topic_time_path):
        if "label_link.xls" in file:
            dir_list.append(root)
            path = os.path.join(root, 'label_link.xls')
            path_list.append(path)
    # # print path_list[0]


    write_history_json(topic_time_path)
    for i in range(len(path_list)):
        write_json(path_list[i],topic_time_path)
        #     # print 'pc',pic_dir_list[i]
        #     #     print path_list[i],'op'
        #     labels = dict(load_data(path_list[i], 0))  # 标签列表
        #     links = load_data(path_list[i], 1)  # 节点连接列表
        #     if links.__len__() == 0:
        #         print "分析的路径为空,跳过"
        #         continue
        #         # print path_list[i]


# if __name__ == '__main__':
#     create_xls('../documents/topic/香格里拉对话：美国防长对中国“又打又拉”/2016-06-06 22:44:48')
# main_network('../documents/topic/2016-08-01 12:51/王毅：奉劝日方不要一错再错，没完没了')
# test('../documents/topic/2016-08-01 12:51/王毅：奉劝日方不要一错再错，没完没了/label_link.xls')

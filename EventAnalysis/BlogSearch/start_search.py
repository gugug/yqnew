# coding=utf-8

import multiprocessing
from multiprocessing import Manager
from MoblieWeibo import *
from write_everything import *
from create_file import *
from search_topic import SearchTopic as st
__author__ = 'gu'

"""
result_dict 全局变量作为输出结果。
"""

manager = Manager()
result_dict = manager.dict()  # 全局变量接收多进程的结果


def search_list(blog_list):
    """
    传入一个博文标题列表，然后多进程对每一个元素进行搜索
    :return:
    """
    if len(blog_list) != 0:
        event_name = blog_list[0]
        print 'en', event_name

        pool = multiprocessing.Pool(processes=4)
        for blog in blog_list:
            pool.apply(start_search, (blog, event_name))
        pool.close()
        pool.join()

        # threads = []
        # for blog in blog_list:
        #     search_process = multiprocessing.Process(target=start_search, args=(blog, event_name))  # 搜索每一个blog
        #     search_process.start()
        #     threads.append(search_process)
        #
        # for j in range(len(threads)):
        #     threads[j].terminate()
        #
        # for j in range(len(threads)):
        #     threads[j].join()



def start_search(one_blog, event_name, flag=0):  # flag =1,one_blog=keywords
    """
    对一个博文在微博平台进行搜索
    :return:
    """
    try:
        # using blog to search
        if flag == 0:
            print "正在进行新事件搜索并爬取..."
            total_result_list, total_reason_list, total_comment_list, total_participants_list = st().search_topic(one_blog)
        # using keywords to search
        else:
            print "正在用 ", event_name, " 的关键词进行搜索..."
            total_result_list, total_reason_list, total_comment_list, total_participants_list = st().search_topic(one_blog)

        print 'len_total_result_list', len(total_result_list)
        if len(total_result_list) > 0:

            # [[blog_id, content, user_name, user_id, ptime, topic, like_num, rpt_num, cmt_num]]
            blog_id = total_result_list[0][0]
            content = total_result_list[0][1]
            originator = total_result_list[0][2]
            originator_id = total_result_list[0][3]
            post_time = total_result_list[0][4]
            topic = total_result_list[0][5]
            like_num = total_result_list[0][6]
            repost_num = total_result_list[0][7]
            comment_num = total_result_list[0][8]


            time_dir = create_time_file()
            event_news = event_name+'/'+ topic
            total_dir = create_topic_file(event_news, time_dir)

             # 写入内容
            write_forward(total_dir, total_reason_list)
            write_comment(total_dir, total_comment_list)
            write_participants(total_dir, total_participants_list)


            print 'total_dir0', total_dir

            total_result_list[0].append(total_dir)
            print "result_dict[0][9]", total_result_list[0][9]

            print "博文id ", blog_id
            print "博文内容 ", content
            print "发源者昵称 ", originator
            print "发源者id ", originator_id
            print "发表时间 ", post_time
            print "话题 ", topic
            print "点赞数 ", like_num
            print "转发数 ", repost_num
            print "评论数 ", comment_num
            print "参与人评论转发文本的路径total_dir1---------------------", total_dir


            result_dict[one_blog] = total_result_list[0]

            # return blog_id, content, originator, post_time,topic,like_num,repost_num,comment_num,total_dir
            # [blog_id,content,originator,originator_id,post_time,topic,like_num,repost_num,comment_num,total_dir])
        else:
            print "爬取失败"
            return None
    except:
        pass




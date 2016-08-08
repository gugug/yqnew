# coding=utf-8

from crawl_weibo import *
import urllib2
import re

__author__ = 'gu'

"""
7.27
测试完毕,会出现掉线的问题,可能是频率太高
"""

class SearchTopic(WeiboPage):
    """
    继承父类的一些公共方法
    进行搜索并爬取路径
    """

    def is_topic(self, tpw):
        """
        此方法用来判断搜索的是否有结果，有结果返回true,否则false
        :param： 要搜索的内容，既是话题
        :return:
        """
        topic_words = tpw
        print "正在搜索话题: ", topic_words
        hot_url = 'http://weibo.cn/search/mblog/?keyword=' + str(
            urllib2.quote(topic_words)) + '&sort=hot'
        req = urllib2.Request(url=hot_url, headers=self.header)
        result_page = urllib2.urlopen(req).read()

        if "抱歉，未找到" not in result_page:
            return True
        else:
            req = urllib2.Request(url=hot_url, headers=self.header)
            result_page = urllib2.urlopen(req).read()
            if "抱歉，未找到" in result_page:
                return False
            else:
                return True

    def get_id_name(self, item):
        """
        大v博文用户id和名字
        :param item:一个人的全部待匹配源代码
        :return:大v的id,大v的名字
        """
        issuer_id_name_patterns = re.compile('<a class="nk" href="http://weibo.cn/(.*?)">(.*?)</a>')  # 匹配一段里面的名字和id
        issuer_id_name = issuer_id_name_patterns.findall(item)
        clean_issuer_id_patterns = re.compile('u/')
        cleaned_issuer_id_name = re.sub(clean_issuer_id_patterns, '', issuer_id_name[0][0])
        return cleaned_issuer_id_name, issuer_id_name[0][1]

    def get_blog_id(self, item):
        """
        博文id
        :param item:一个人的全部待匹配源代码
        :return:博文id
        """
        issuer_blog_id_pattern = re.compile('id="(.*?)">')
        issuer_blog_id = issuer_blog_id_pattern.findall(item)
        return issuer_blog_id[0]

    def get_content(self, item):
        """
        博文内容
        :param item:一个人的全部待匹配源代码
        :return:博文内容
        """
        issuer_blog_pattern = re.compile('<span class="ctt">:(.*?)>赞')
        issuer_blog_unclean = issuer_blog_pattern.findall(item)
        issuer_blog = self.cleaned_weibo(issuer_blog_unclean[0])
        extra1 = re.compile('&nbsp;.*$')
        cleaned_issuer_blog = re.sub(extra1, '', issuer_blog)
        return cleaned_issuer_blog

    def get_nums_link(self, item):
        """
        :param item:一个人的全部待匹配源代码
        :return:点赞 转发 评论 转发路径
        # print "点赞", like_forward_comment[0][0]
        # print "转发", like_forward_comment[0][2], like_forward_comment[0][1]
        # print "评论", like_forward_comment[0][4], like_forward_comment[0][3]
        """
        like_forward_comment_pattern = re.compile(
            '>赞\[(\d+)]</a>&nbsp;<a href="(.*?)">转发\[(\d+)]</a>&nbsp;<a href="(.*?)" class="cc">评论\[(\d+)]</a>')
        like_forward_comment = like_forward_comment_pattern.findall(item)
        return like_forward_comment[0][0], like_forward_comment[0][2], like_forward_comment[0][4], \
               like_forward_comment[0][1], like_forward_comment[0][3]

    def get_time(self, item):
        """
        :param item:一个人的全部待匹配源代码
        :return:发表时间
        """
        try:
            blog_time_pattern = re.compile('<!---->&nbsp;<span class="ct">(.*?)&nbsp;')
            informality_blog_time = blog_time_pattern.findall(item)
            if len(informality_blog_time) == 0:
                blog_time_pattern1 = re.compile('<span class="ct">(.*?)</span>')
                informality_blog_time = blog_time_pattern1.findall(item)
            today_pattern = re.compile('今天')
            minago_pattern = re.compile('\d+分钟前')
            t = time.strftime('%m' + '月' + '%d' + '日', time.localtime())
            t = t.decode('utf-8')
            formality_blog_time = re.sub(today_pattern, t, informality_blog_time[0])
            formality_blog_time = re.sub(minago_pattern, t, formality_blog_time)
            if not formality_blog_time:
                formality_blog_time = '0000-00-00'
            return formality_blog_time
        except:
            pass

    def get_topic(self, content):
        """
        :param content:博文内容
        :return:博文主题
        """
        topic_patternts = re.compile('【(.*?)】')
        topic = topic_patternts.findall(content)
        if len(topic) > 0:
            topic_clean_pattern = re.compile('(\[.*?])')
            topic = re.sub(topic_clean_pattern, '', topic[0])
            topic_clean3_pattern = re.compile('#')
            topic = re.sub(topic_clean3_pattern, '', topic)
            topic_clean2_pattern = re.compile('\\s')
            topic_result = re.sub(topic_clean2_pattern, '', topic)
        else:
            # print "这篇博文没有话题，检测不到事件"
            topic_result = '未知'
        return topic_result

    def get_forward(self, fwd_num, fwd_link):
        """
        :param fwd_num:转发数
        :param fwd_link:转发链接
        :return:forward_list, forward_participants，转发路径和参与转发的人
        """
        print "爬取转发路径>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        link_pattern = re.compile("(http://weibo.cn/repost/.*?)&amp")
        link = link_pattern.findall(fwd_link)
        fwd_link = link[0]

        if int(fwd_num) > 1500:
            forward_pages = 150  # ps
        elif int(fwd_num) <= 10:
            forward_pages = 1
        else:
            if int(fwd_num) % 10 > 0:
                forward_pages = int(fwd_num) / 10 + 1
            else:
                forward_pages = int(fwd_num) / 10

        forward_list = []
        forward_participants = []
        for f_page in range(1, forward_pages):
            forward_url = str(fwd_link) + '&page=' + str(f_page)
            reason_list, f_participants = self.get_forward_common(forward_url)  # 爬取转发路径
            forward_list += reason_list
            forward_participants += f_participants

        return forward_list, forward_participants

    def get_comment(self, cmt_num, cmt_link):
        """
        :param cmt_num: 评论数，来决定页数
        :param cmt_link: 评论页面的链接
        :return:评论的内容和参与人
        comment_list = []  昵称：评论内容
        comment_participants = []  昵称
        """
        print "爬取评论>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        link_pattern = re.compile("(http://weibo.cn/.*?)&amp")
        link = link_pattern.findall(cmt_link)
        cmt_link = link[0]

        if int(cmt_num) > 15000:
            cmt_pages = 1500  # ps
        elif int(cmt_num) <= 10:
            cmt_pages = 1
        else:
            if int(cmt_num) % 10 > 0:
                cmt_pages = int(cmt_num) / 10 + 1
            else:
                cmt_pages = int(cmt_num) / 10

        comment_list = []
        comment_participants = []
        for c_page in range(1, cmt_pages):
            cmt_url = str(cmt_link) + '&page=' + str(c_page)
            comment, participants = self.get_comment_common(cmt_url)
            comment_list += comment
            comment_participants += participants
        return comment_list, comment_participants

    def get_participants(self, forward_participants, comment_participants):
        """
        去重返回全部参与人
        :param forward_participants: 转发参与人
        :param comment_participants: 评论参与人
        :return: 全部参与人
        """
        all_participants = forward_participants + comment_participants
        participants = list(set(all_participants))
        return participants

    def search_topic(self, search_content):

        """
        传入一个搜索的内容
        :param search_content 要搜索的内容
        :return:
        total_result_list = [[博文id,博文时间,标题,博文,首发者的id,首发者的名字,点赞,转发,评论]]
        total_reason_list = [[asd@fadsf@人民日报, safagr@人民日报, yutsfa@人民日报]]
        total_comment_list = [[哈哈，呵呵]]  搜索结果的评论的列表
        total_participants = [[阿猫,阿狗]] 搜索结果的转发评论的参与人
        """
        try:
            topic_words = search_content

            total_result_list = []
            total_reason_list = []
            total_comment_list = []
            total_participants = []
            big_v_num = 0

            page_num = self.is_topic(topic_words)
            if page_num:
                page = 1
                pageurl = 'http://weibo.cn/search/mblog?keyword=' + str(
                    urllib2.quote(topic_words)) + '&sort=hot&page=' + str(page)
                req = urllib2.Request(url=pageurl, headers=self.header)
                result_turn_page = urllib2.urlopen(req).read()

                issuer_pattern = re.compile('<div class="c" (id.*?)<div class="s"></div>')  # 把每个人的一个整个匹配下来
                issuer = issuer_pattern.findall(result_turn_page)
                rpt_reason_list = []
                if len(issuer) > 0:
                    item = issuer[0]  # 对第一个结果处理
                    if 'alt="V"/>' in item:
                        big_v_num += 1
                        user_id, user_name = self.get_id_name(item)
                        blog_id = self.get_blog_id(item)
                        content = self.get_content(item)
                        topic = self.get_topic(content)
                        like_num, rpt_num, cmt_num, forward_url, comment_url = self.get_nums_link(item)
                        ptime = self.get_time(item)
                        no_repeat_reason_list, forward_participants = self.get_forward(rpt_num, forward_url)
                        comment_list, comment_participants = self.get_comment(cmt_num, comment_url)
                        participants = self.get_participants(forward_participants, comment_participants)

                        result_list = [blog_id, content, user_name, user_id, ptime, topic,
                                       like_num, rpt_num, cmt_num]
                        total_result_list.append(result_list)

                        total_comment_list.append(comment_list)
                        total_participants.append(participants)

                        for reason in no_repeat_reason_list:
                            rpt_reason_list.append(str(reason) + '//@' + user_name + ":")
                        total_reason_list.append(rpt_reason_list)

                    else:
                        # issuer_id_name_pattern = re.compile(
                        #     '<a class="nk" href="http://weibo.cn/(.*?)">(.*?)</a>')  # 匹配一段里面的名字和id
                        # issuer_id_name = issuer_id_name_pattern.findall(item)
                        # print "非大v博文用户id和名字", issuer_id_name[0][0], issuer_id_name[0][1]
                        pass
                else:
                    pass
            else:
                pass
            return total_result_list, total_reason_list, total_comment_list, total_participants
        except:
            pass

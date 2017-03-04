# coding=utf-8

import datetime
import random
from time import sleep
import urllib2
import re
from yqnew.settings import *
import multiprocessing
__author__ = 'gu'



class Sina():
    """
    本类爬取新浪的用户的首页信息和资料页的信息
    可以传入的参数为 ： /n/%E4%BB%99%E5%89%91%E6%8E%A2%E4%BA%91?vt=4、 /n/人民日报、 id（数字或者引文）
    """
    manager = multiprocessing.Manager()
    area_list = manager.list()
    age_list = manager.list()
    sex_list = manager.list()

    def __init__(self, uid):

        """
        :param uid: 用户的id，可能是英文或者数字
        :return: null
        """
        self.header = {'User-Agent': 'Mozilla/' + str(
            float(int(random.uniform(1, 6)))) + '(X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/' + str(
            float(int(random.uniform(29, 36))))}
        self.uid = str(uid)
        self.data_dir = os.path.join(BASE_DIR, 'documents', 'data/')

        # 首页
        index_url = "http://weibo.cn/" + self.uid  # 猎头的首页
        req = urllib2.Request(url=index_url, headers=self.header)
        self.homepage = urllib2.urlopen(req).read()
        # print self.homepage
        # 资料页
        sleep(random.randint(3, 7))

        info_url = 'http://weibo.cn/' + str(self.get_uid()) + '/info'  # 资料页
        req = urllib2.Request(url=info_url, headers=self.header)
        self.info_page = urllib2.urlopen(req).read()

    # 以下是爬取用户的首页信息
    def get_homepage_information(self):
        """
            爬取猎头的id name 性别 微博数 关注数 粉丝数
            匹配用户首页的id name 微博数 关注数 粉丝数
        :return:uid_all (list)
        """
        user_patterns = re.compile(
            '<span class="ctt">(.*?)<.*?uid=(.*?)&.*?span class="tc">微博\[(.*?)].*?关注\[(.*?)].*?粉丝\[(.*?)]'
        )
        uid_all = user_patterns.findall(self.homepage)
        return uid_all

    def isbig_v(self):
        """
        判断是否大v
        :return: true/false(str)
        """
        big_v_patetrns_splits = re.compile('<div class="u">(.*?)<div class="u">')
        big_v = big_v_patetrns_splits.findall(self.homepage)
        try:
            if 'alt="V"/' in big_v[0]:
                return str(True)
            else:
                return str(False)
        except:
            pass

    def get_name(self):
        """
        首页上取到用户名
        :return: 用户名(str)
        """
        name_pattern = re.compile('<span class="ctt">(.*?)<.*?uid=.*?>私信')
        name = name_pattern.findall(self.homepage)
        label_pattern = re.compile('&nbsp.*?$')
        name = re.sub(label_pattern, '', name[0])
        return name

    def get_uid(self):
        """
        获取用户的id
        :return: 用户id(str)
        """
        try:
            uid_pattern = re.compile('私信</a>&nbsp;<a href="/(.*?)/info')
            uid = uid_pattern.findall(self.homepage)
            return uid[0]
        except:
            pass

    def get_weibo_num(self):
        """
        获取用户的微博数
        :return: weibo_num[0] (str)
        """
        weibo_num_pattern = re.compile('微博\[(.*?)]')
        weibo_num = weibo_num_pattern.findall(self.homepage)
        return weibo_num[0]

    def get_follows_num(self):
        """
            # 爬取用户的关注
        :return:follows_num[0] (str)
        """
        follows_num_pattern = re.compile('关注\[(.*?)]')
        follows_num = follows_num_pattern.findall(self.homepage)
        return follows_num[0]

    def get_fans_num(self):
        """
            # 爬取用户的粉丝
        :return:fans_num[0] (str)
        """
        fans_num_pattern = re.compile('粉丝\[(.*?)]')
        fans_num = fans_num_pattern.findall(self.homepage)
        return fans_num[0]

    # 以下是爬取用户的资料信息
    def get_nickname(self):
        """
        爬取资料页的昵称
        :return:nickname[0] (str)
        """
        nickname_pattern = re.compile('基本信息</div><div class="c">(昵称:.*?)<br/>')
        nickname = nickname_pattern.findall(self.info_page)
        return nickname[0]

    def get_authentication(self):
        """
        爬取用户资料页的认证
        :return:authen(str)
        """
        auth_pattern = re.compile('<br/>认证:(.*?)<br/>')
        authen = auth_pattern.findall(self.info_page)
        if len(authen) > 0:
            return authen[0]
        else:
            return '非认证用户'

    def get_sex(self):
        """
        爬取用户资料页的性别
        :return:sex(str)
        """
        sex_pattern = re.compile('<br/>性别:(.*?)<br/>')
        sex = sex_pattern.findall(self.info_page)
        if len(sex) > 0:
            return sex[0]
        else:
            return '未知'

    def get_area(self):
        """
        爬取用户资料页的地区
        :return:area(str)
        """
        area_pattern = re.compile('<br/>地区:(.*?)<br/>')
        area = area_pattern.findall(self.info_page)
        if len(area) > 0:
            return area[0]
        else:
            return '其他'

    def get_birthday(self):
        """
        爬取用户资料页的生日
        :return:birthday(str)
        """
        birthday_pattern = re.compile('<br/>生日:(.*?)<br/>')
        birthday = birthday_pattern.findall(self.info_page)
        if len(birthday) > 0:
            return birthday[0]
        else:
            return '0000-00-00'

    def get_authentic_info(self):
        """
        爬取用户资料页的认证信息
        :return:authentic_info（str）
        """
        authentic_info_pattern = re.compile('<br/>认证信息：(.*?)<br/>')
        authentic_info = authentic_info_pattern.findall(self.info_page)
        if len(authentic_info) > 0:
            return authentic_info[0]
        else:
            return '非认证用户'

    def get_brief_intro(self):
        """
        爬取用户资料页的简介
        :return:brief_intro(str)
        """
        brief_intro_pattern = re.compile('<br/>简介:(.*?)<br/>标签')
        brief_intro = brief_intro_pattern.findall(self.info_page)
        if len(brief_intro) > 0:
            return brief_intro[0]
        else:
            return '未添加'

    def get_tags(self):
        """
        爬取全部标签，如果有返回全部标签，一串字符串；如果没有则返回None
        :return: tags(tsr)/None(str)
        """
        url = 'http://weibo.cn/account/privacy/tags/?uid=' + self.get_uid()
        req = urllib2.Request(url=url, headers=self.header)
        tags_page = urllib2.urlopen(req).read()
        tags_pattern = re.compile('<div class="c">.*?的标签:<br/>(.*?)&nbsp;</div>')
        tags_result = tags_pattern.findall(tags_page)
        if len(tags_result) > 0:
            label_pattern = re.compile('<.*?>')
            other_pattern = re.compile('&nbsp;')
            tags_result = re.sub(label_pattern, '', tags_result[0])
            tags = re.sub(other_pattern, ' ', tags_result)
            return tags
        else:
            return '无'

    # def write_data_sql(self):
    #     """
    #     把资料页的全部信息重新整合到一个列表, 写入数据库
    #     :return:all_data(list)
    #     """
    #     dt = Database()
    #     dt.save_headhunter(self.get_uid(),self.get_name(),self.get_sex(),self.get_birthday(),self.get_authentic_info(),
    #                     self.get_area(),self.get_brief_intro(),self.get_tags(),self.get_fans_num(),self.get_follows_num(),
    #                        self.get_weibo_num())
    #
    #     return 0

    # def save_txt(self):
    #     """
    #     写入txt文档
    #     """
    #     try:
    #         # if os.path.exists(self.data_dir):
    #         #     pass
    #         # else:
    #         #     os.mkdir(self.data_dir)
    #         print self.data_dir + self.get_name() + '.txt'
    #         # data_file = open(self.data_dir + self.get_name() + '.txt', 'w+')
    #         data_file = open(self.data_dir + self.uid + '.txt', 'w+')
    #         data_file.write(
    #             '用户名: ' + str(self.get_name())
    #             + '\nid: ' + str(self.get_uid())
    #             + '\n微博数: ' + str(self.get_weibo_num())
    #             + '\n关注数: ' + str(self.get_follows_num())
    #             + '\n粉丝数: ' + str(self.get_fans_num())
    #             + '\n是否大v： ' + str(self.isbig_v())
    #             + '\n性别： ' + str(self.get_sex())
    #             + '\n地区： ' + str(self.get_area())
    #             + '\n生日： ' + str(self.get_birthday())
    #             + '\n认证： ' + str(self.get_authentication())
    #             + '\n认证信息： ' + str(self.get_authentic_info())
    #             + '\n简介： ' + str(self.get_brief_intro())
    #             + '\n用户标签: ' + str(self.get_tags())
    #             + '\n'
    #         )
    #         data_file.close()
    #     except Exception, e:
    #         print e
    #         pass

    # def print_all(self):
    #     try:
    #         print '用户名: ', self.uid
    #         print 'id: ', self.get_uid()
    #         print '微博数: ', self.get_weibo_num()
    #         print '关注数: ', self.get_follows_num()
    #         print '粉丝数: ', self.get_fans_num()
    #         print '是否大v： ', self.isbig_v()
    #         print '性别： ', self.get_sex()
    #         print '地区： ', self.get_area()
    #         print '生日： ', self.get_birthday()
    #         print '认证： ', self.get_authentication()
    #         print '认证信息： ', self.get_authentic_info()
    #         print '简介： ', self.get_brief_intro()
    #         print '用户标签:', self.get_tags()
    #         print
    #     except:
    #         pass

    # def hunter_account(self):
    #     account = {
    #         "人民日报": 2803301701, "新浪新闻": 2028810631, "凤凰周刊": 1267454277,
    #         "网易新闻客户端": 1974808274, "北京晨报": 1646051850, "头条新闻": 1618051664,
    #         "人民网": 2286908003, "财经网": 1642088277, "新京报": 1644114654,
    #         "中国新闻网": 1784473157, "三联生活周刊": 1191965271, "法制晚报": 1644948230,
    #         "新闻晨报": 1314608344, "中国之声": 1699540307, "中国新闻周刊": 1642512402,
    #         "澎湃新闻": 5044281310, "中国日报": 1663072851, "北京青年报": 1749990115,
    #         "新快报": 1652484947, "华西都市报": 1496814565, "凤凰网": 2615417307,
    #         "FT中文网": 1698233740, "环球时报": 1974576991
    #     }
    #     return account
    #
    # def process_control(self, uid):
    # a = Sina(uid)
    # a.save_txt()

    def get_result(self):
        # print self.uid
        area = self.get_area()
        # print area
        birth = self.get_birthday()
        # print birth
        sex = self.get_sex()
        # print sex
        self.area_list.append(area)
        self.age_list.append(birth)
        self.sex_list.append(sex)

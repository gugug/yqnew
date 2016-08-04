#!/usr/bin/env python
# coding:utf-8


'''
@version:2.7.6
@date:2016-07-24
@function:
'''

import re
import urllib2
import urllib
import cookielib
import threading               #threading模块用于实现多线程
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


class MoblieWeibo:
    """
    #模拟登陆手机版微博  定义一个类
    """
    def __init__(self):
        """
        # __init__是python中一个特殊的函数名，用于根据类的定义创建实例对象
        # self 参数指向了这个正在被创建的对象本身
        #注意：在类声明里定义__init__()方法时，第一个参数必须是self.
        # self.cap = None
        """
        self.cj = cookielib.LWPCookieJar()
        """
        if cookie_j.load(cookie_filename)
        将一个保存cofilename is not None:
        self.cj.load(cookie_filename)
        将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
        """
        self.cookie_processor = urllib2.HTTPCookieProcessor(self.cj)
        """
        创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的URL的打开
        """
        self.opener = urllib2.build_opener(self.cookie_processor,urllib2.HTTPHandler)
        """
        将包含了cookie、http处理器、http的handler的资源和urllib2对象绑定在一起
        build_opener函数支持以下功能：验证，cookie或其他的HTTP高级功能
        可用build_opener函数创建自己的自定义Opener对象
        """
        urllib2.install_opener(self.opener)

    def getArgs(self):          # 定义一个函数
        """

        :return:
        """
        ArgsRequest = urllib2.Request('http://login.weibo.cn/login/', headers=headers)
        response = urllib2.urlopen(ArgsRequest)
        text = response.read()

                                # print "获取post数据中的vk的值:"
        vkPattern = re.compile('<input type="hidden" name="vk" value="(.*?)" />')
        self.vk = re.search(vkPattern, text).group(1)
        # print 'self.vk:',self.vk
                                # print "获取post数据中的backURL的值:"
        self.BackUrlPattern = re.compile("<input type=\"hidden\" name=\"backURL\" value=\"(.*?)\" />")
        #数据预处理
        self.BackUrl = re.search(self.BackUrlPattern, text).group(1)
        # print 'self.BackUrl:',self.BackUrl

                                # print "获取post数据中的rand的值:"
        randPattern = re.compile('<form action="\?rand=(.*?)&')
        self.rand = re.search(randPattern, text).group(1)
        # print 'self.rand',self.rand

                                # print "获取post数据中的passwd变量的值:"
        pwdPattern = re.compile('<input type="password" name="(.*?)" size="30" />')
        self.passwd = re.search(pwdPattern, text).group(1)
        # print 'self.passwd:',self.passwd

        capPattern = re.compile('<input type="hidden" name="capId" value=\"(.*?)\" />')
        self.cap = re.search(capPattern, text).group(1)
        # print 'self.cap',self.cap

        Img = re.compile('<img src="(.*?)" alt="请打开图片显示" />')
        img = re.search(Img, text).group(1)
        print img
        code = raw_input('请输入验证码')
        self.text = code

    def login(self, username, password):
                                # print username,password
        self.getArgs()
                                # print "生成post数据,向网址Url提交post:"
        PostData = {
            "mobile": username,
            str(self.passwd): password,
            'code': self.text,      #self.text中self为getArg()函数中的一个参数
            'submit': "登录",
            'remember': "checked",
            'backURL': self.BackUrl,
            'vk': self.vk,
            'tryCount': '',
            'capId': self.cap,
            'rand': self.rand
        }
                                    # print PostData
        PostData = urllib.urlencode(PostData)
                                    # print "输出调交post返回的主页:"
        request = urllib2.Request('http://login.weibo.cn/login/', PostData, headers)
        response = urllib2.urlopen(request)
        text = response.read()
        while '我的首页' not in text: # 检验验证码是否正确
            print '验证码错误，请重输'
            m = MoblieWeibo()
            m.login(username, password)
            break


class NewsTitles:

    def __init__(self, media_name, media_link, diction):
        """
        初始化，媒体名称以及媒体首页网址。传入一个空的字典名称。
        """
        self.media_name = media_name
        self.media_link = media_link
        self.diction = diction

    def get_source_data(self):
        """
        获取网页源代码
        :return:
        """
        request = urllib2.Request(self.media_link, headers=headers)
        response = urllib2.urlopen(request)
        data = response.read()                  #data为源代码全文
        return data

    def get_news_titles(self):
        """
        运用类中的其他函数，获取微博原文新闻标题，将媒体名称以及所获取的微博标题列表写入字典中
        :return:
        """
        data = self.get_source_data()
        pattern = re.compile('<span class="ctt">.*?(【.*?】).*?赞.*?转发')
        titles = re.findall(pattern, data)
        titles = set(titles)
        list_news = []
        for title in titles:
            title = re.sub('<.*?>', '', title)
            list_news.append(title)
        self.diction[self.media_name ] = list_news


class ThreadingNewsTitles(NewsTitles):

    def __init__(self):
        """
        初始化一个空字典
        初始化所要获取的猎头的信息即昵称以及首页网址
        :return:
        """
        self.dictionary = {}
        self.media_all =\
               [('今日头条',      'http://weibo.cn/headlineapp?page=',  self.dictionary ),
                ('头条新闻',      'http://weibo.cn/breakingnews?page=', self.dictionary ),
                ('百度新闻',      'http://weibo.cn/baidunews?page=',    self.dictionary ),
                ('央视新闻',      'http://weibo.cn/cctvxinwen?page=',    self.dictionary ),
                ('新浪新闻',      'http://weibo.cn/sinapapers?page=',    self.dictionary ),
                ('南方都市报',    'http://weibo.cn/nddaily?page=',       self.dictionary ),
                ('网络新闻联播',   'http://weibo.cn/cntv2011lh?page=',    self.dictionary ),
                ('中国新闻周刊',   'http://weibo.cn/chinanewsweek?page=', self.dictionary ),
                ('腾讯新闻客户端', 'http://weibo.cn/u/2806170583?page=',  self.dictionary ),
                ('新浪新闻客户端', 'http://weibo.cn/58371?page=',         self.dictionary ),
                ('搜狐新闻客户端', 'http://weibo.cn/sohuexpress?page=',   self.dictionary ),
                ('网易新闻客户端', 'http://weibo.cn/newsapp?page=',       self.dictionary ),
                ('凤凰新闻客户端', 'http://weibo.cn/ifengapps?page=',     self.dictionary ),
                ('中国网新闻中心', 'http://weibo.cn/newsnewschina?page=', self.dictionary ),
                ('全球头条新闻事件','http://weibo.cn/372835471?page=',    self.dictionary )]

    def threading(self):
        """
        实例化（将猎头信息传入类中）
        创建线程并启动线程
        返回所获取到的字典
        :return:
        """
        threads = []
        length = range(len(self.media_all))
        for i in length:    #实例化
            test = NewsTitles(self.media_all[i][0], self.media_all[i][1], self.media_all[i][2])#实例化
            t = threading.Thread(target=test.get_news_titles())
            threads.append(t)
        for i in length:
            threads[i].start()
        for i in length:
            threads[i].join()
        return self.dictionary


class NewsDetection:

    def __init__(self):
        self.dic_news = NewsDetection.detect_news()

    @staticmethod
    def detect_news():
        user = MoblieWeibo()
        user.login('70705420yc@sina.com','1234567') #('451650276@qq.com', '19950602')
        threading_news_titles = ThreadingNewsTitles()
        dic_news = threading_news_titles.threading()
        return dic_news

    def get_dic_news(self):
        return self.dic_news



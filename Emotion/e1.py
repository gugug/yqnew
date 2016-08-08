__author__ = 'kalin'
# coding=utf-8
import os
import re
import jieba
import collections
import json
from yqnew.settings import *

class Emotion:
    def __init__(self, comment_file):
        self.comment_file = comment_file
        self.contents_list = []  # 评论列表
        self.contents_dict = {}   # 评论字典, key为从0开始的数字,表示第几条评论,value为评论内容
        self.feeling_dict = {}  # 情感词典,include (angry,anxious......8种情感词)
        self.num_feel_dict = {0: "愤怒", 1: "焦虑", 2: "厌恶", 3: "憎恨", 4: "喜欢", 5: "愉悦", 6: "哀伤", 7: "同情", 8:"其他"}
        self.stopword_list = []  # 停用词列表
        self.content_feeling_dict = {}   # 每条评论对应的情感
        self.feeling_proportion_dict = {}  # 情感比例字典

    def read_data(self):
        """
        function: 获取评论数据(comment.txt)
        数据样例：
            0邪邪0 : 我去当甲方管理的也比这个强，出现这么多问题不单单是没钱的原因了
            用户yv9480i6zt : 其实这都是套路，间接发展当地酒店业[doge]
        :return: contents_list 评论列表
        """
        contents_list = list()
        files = open(self.comment_file, "r")
        comment_lines = files.readlines()
        for line in comment_lines:
            match = re.findall(r'[^:]+$', line)  # 除去昵称
            contents_list.append("".join(match))  # 添加至评论列表
        return contents_list

    # def get_stopword(self):
    #     """
    #     function: 获取停用词列表
    #     :return:
    #     """
    #     base_dir = os.path.dirname(__file__)
    #     file_path = os.path.join(base_dir, 'stopwords.txt')
    #     files = open(file_path, "r")
    #     self.stopword_list = map(str.strip, files.readlines())
    #     return self.stopword_list

    @staticmethod
    def load_file(emotion_class):
        """
        function:加载字典
        :param emotion_class: 情感类别
        :return: data: 特定类别的词典
        """
        filename = emotion_class + '.txt'
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, filename)
        f = open(file_path, "r")
        data = map(str.strip, f.readlines())
        return data

    def get_feeling_dicts(self):
        """
        function: 获取情感词典
        :return:
        """
        emotion_list = ['angry', 'anxious', 'dislike', 'hate', 'like', 'pleasure', 'sad', 'sympathy']
        for i in range(emotion_list.__len__()):
            self.feeling_dict[i] = self.load_file(emotion_list[i])
        return self.feeling_dict

    def word_segment(self):
        """
        function: 将评论分词
        :return:contents_dict:获取评论字典, key为从0开始的数字,表示第几条评论,value为评论内容
        """
        self.contents_list = self.read_data()
        for i in range(len(self.contents_list)):
            content = list(jieba.cut(self.contents_list[i]))
            list_word_segment = [s.encode('utf-8') for s in content]   #turn type(unicode) to (string)
            list_word_segment = map(str.strip, list_word_segment)
            list_word_segment.remove('')
            self.contents_dict[i] = list_word_segment
        return self.contents_dict

    def emotion_detect(self):
        """
        function:#得到每条评论对应的情感类别
        :return:　
        """
        self.feeling_dict = self.get_feeling_dicts()
        self.contents_dict = self.word_segment()
        content_num = len(self.contents_dict)  # 评论数
        for i in range(content_num):  # 将每条评论按情感词分不同的情感类别
            li = []
            for s in self.contents_dict[i]:
                if s in self.feeling_dict[0]:
                    li.append(0)
                elif s in self.feeling_dict[1]:
                    li.append(1)
                elif s in self.feeling_dict[2]:
                    li.append(2)
                elif s in self.feeling_dict[3]:
                    li.append(3)
                elif s in self.feeling_dict[4]:
                    li.append(4)
                elif s in self.feeling_dict[5]:
                    li.append(5)
                elif s in self.feeling_dict[6]:
                    li.append(6)
                elif s in self.feeling_dict[7]:
                    li.append(7)
            self.content_feeling_dict[i] = list(set(li))
        return self.content_feeling_dict

    def proportion(self):
        """
        function: 统计每类情感的比例
        :return: feeling_proportion_dict :　每类情感（包括无情感词）的比例
        """
        self.content_feeling_dict = self.emotion_detect()
        values = self.content_feeling_dict.values()
        all_emotion = []
        none_emotion = 0      # 情感none的次数
        for v in values:
            if len(v) == 0:
                none_emotion += 1
            else:
                for i in v:
                    all_emotion.append(i)
        all_num = float(none_emotion + len(all_emotion))   # 感情的总次数
        counts = collections.Counter(all_emotion)  # 统计每种感情的次数
        valid_num = all_num - none_emotion
        for i in range(8):
            self.feeling_proportion_dict[self.num_feel_dict[i]] = counts[i]/valid_num
        # self.feeling_proportion_dict[self.num_feel_dict[8]] = none_emotion/all_num
        return self.feeling_proportion_dict

def dump_json(dict_emotion,path):
    """
    生成emotion.json
    :param dict_emotion: 情绪字典
    :return:
    """
    emotion_list = []
    event_title = path.split('/')[-2]
    for i in dict_emotion:
        dict_emotion[i] = '%.2f' % dict_emotion[i]
        emotion_dict = {'value':dict_emotion[i],'name':i}
        emotion_list.append(emotion_dict)
    data_dict = {'socialEmotion':emotion_list}
    encode_json = json.dumps(data_dict,separators=(',',':'))
    json_file = open(os.path.join(JSON_DIR,event_title,'social_emotion.json'),'w+')
    json_file.writelines(encode_json)
    json_file.close()
    print 'finish writing social emotion json'
    return True

def main_emotion(path):
    comment_file = os.path.join(path,'comment.txt')
    dict_emotion = Emotion(comment_file).proportion()
    dump_json(dict_emotion,path)
    for emotion_class in dict_emotion:
        print emotion_class, ':', dict_emotion[emotion_class]

# if __name__ == "__main__":
#     main_emotion('comment.txt')
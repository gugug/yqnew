# coding=utf-8
__author__ = 'gu'
"""
写转发路径，评论内容，参与者昵称
"""


def write_forward(file_name, reason_list):
    print "正在写入转发路径"
    respost_path_dir = file_name + '/' + 'repost_path.txt'
    respost_path_txt = open(respost_path_dir, 'w+')
    for reasons in reason_list:
        for reason in reasons:
            respost_path_txt.write(reason + '\n')
    respost_path_txt.close()
    print "转发路径写入完毕"


def write_comment(file_name, comment_list):
    print "正在写入评论内容"

    comment_dir = file_name + '/' + 'comment.txt'
    comment_txt = open(comment_dir, 'w+')
    for comments in comment_list:
        for comment in comments:
            comment_txt.write(comment + '\n')
    comment_txt.close()
    print "评论内容写入完毕"

def write_participants(file_name, participants_list):
    print "正在写入参与者昵称"

    participants_dir = file_name + '/' + 'participants.txt'
    participants_txt = open(participants_dir, 'w+')
    for participants in participants_list:
        for participant in participants:
            participants_txt.write(participant + '\n')
    participants_txt.close()
    print "参与者昵称写入完毕"
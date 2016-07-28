运行main_crawler.py

def run():
    """
        :return:
    """

    MoblieWeibo().login('1939777358@qq.com', '123456a')
    # '70705420yc@sina.com', '1234567') ('meilanyiyou419@163.com','aaa333') 'odlmyfbw@sina.cn','tttt5555'
    serach_list(["王毅：奉劝日方不要一错再错，没完没了"])  #




返回结果为  result_dict
    for key, values in result_dict.items():
        print key
        print '***********_____________***^^^^^^^^^^^^^^'
        for value in values:
            print value





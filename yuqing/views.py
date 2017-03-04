#coding=utf-8
from django import forms
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from db_connection import *

# Create your views here.

def test(request):
    return render_to_response('graphs.html')

def repost(request,topic =''):
    # topic = 'example'
    return render_to_response('allGraph.html',{'topic':topic})

class SearchForm(forms.Form):
    input_words = forms.CharField(max_length=100)


def all_graph(request,topic=''):
    db = Database()
    eid_tuple = ()
    # print 'topic', topic
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            search_words = sf.cleaned_data['input_words']
            print search_words
            eid_tuple = db.search_vague_topic(search_words)  # ({eid,etp},{})

        else:
            print 'invalid form'

    else:  # GET
        eid_tuple = db.search_exact_topic(topic)



    if len(eid_tuple) == 0:
        print 'no result'
        return render_to_response('error.html')
        # scale_list = [11, 11, 15, 13, 12, 13, 10,13,12,9]
        #
        # return render_to_response('graph.html',{'g1_data':scale_list,'topic':topic})
    elif len(eid_tuple) > 1:
        print 'many events'
        event_list = []
        for i in eid_tuple:
            event_list.append(i)
        return render(request, 'list.html', {'event_list': event_list})
    else:
        topic = eid_tuple[0]['topic']
        print 'one event'
        event_id = eid_tuple[0]['event_id']
        scale_list = db.get_scale(event_id)
        db.get_keyword(event_id)
        db.get_news(event_id)
        return render_to_response('graphs.html',{'g1_data':scale_list,'topic':topic})


def graph(request):
    g1_data = [11, 11, 15, 13, 12, 13, 10,13,12,9]

    return render_to_response('graph.html',{'g1_data':g1_data})

def index(request):
    data=[]
    # eve=Event()
    db = Database()
    result = db.get_tiemline()
    # result = []
    if len(result) == 0:
        month_list = [4,4,4,4,4,4,4,4]
        day_list = ['1','5','10','20','23','25','27','30']
        event_list = ['科比告别战','山东疫苗案','常州外国语污染事件','日本熊本县地震','网络主播18日起实名认证','东莞坍塌',
                       '泛亚有色涉嫌非法集资','巴萨猝死']
        for i in range(len(month_list)):
            event_dict ={'month':month_list[i],'day':day_list[i],'topic':event_list[i]}
            data.append(event_dict)
    else:
        for j in range(len(result)):
            event_dict = result[j]
            data.append(event_dict) #[{}{}]
    # for i in data:
        # print 'data',i
    # print data
    # data = [{'topic':u'烧鸡公双方了时间','month':4L,'day':30L},{'topic':u'222','month':4L,'day':15L},{'topic':u'111','month':4,'day':1}]
    # data = [{'a':'aaa'},{'b':'bbb'}]
    return render_to_response('index.html', {'data': data})
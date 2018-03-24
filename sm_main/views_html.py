#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
import json
from itertools import islice
import datetime
from django.db.models import Max
from sm_main.models import settings as sm_settings
from django.conf import settings
# Create your views here.
def sample_upload_html(request):
    return render(request,'sample_manage/sample_upload.html')


def sample_distribute_html(request):

    database_list = []
    for database_name in settings.DATABASES.keys():
        database_list.append(database_name)

    database_list.remove('sm_main')
    database_list.remove('default')
    database_list.remove('sample_double_check')

    result_settings = sm_settings.objects.using('sm_main').only("id", "name").order_by('-id')
    result_list = []
    for item in result_settings:
        id = item.id
        name = item.name
        tMp_dict = {}
        tMp_dict["id"] = id
        tMp_dict["id2name"] = str(id) + "_" + str(name)
        result_list.append(tMp_dict)
    content ={
        'databases':database_list,
        'result_list':result_list
    }

    return render(request,'sample_manage/sample_distribute.html',content)


def sample_compare_html(request):
    result_settings = sm_settings.objects.using('sm_main').only("id","name").order_by('-id')
    result_list = []
    for item in result_settings:
        id = item.id
        name = item.name
        tMp_dict={}
        tMp_dict["id"]=id
        tMp_dict["id2name"]=str(id)+"_"+str(name)
        result_list.append(tMp_dict)
    content ={
        "result_list" :result_list
    }
    return render(request,'sample_manage/sample_compare.html',content)

def sample_merge_html(request):
    result_settings = sm_settings.objects.using('sm_main').only("id", "name").order_by('-id')
    result_list = []
    for item in result_settings:
        id = item.id
        name = item.name
        tMp_dict = {}
        tMp_dict["id"] = id
        tMp_dict["id2name"] = str(id) + "_" + str(name)
        result_list.append(tMp_dict)
    content = {
        "result_list": result_list
    }
    return render(request, 'sample_manage/sample_merge.html', content)

def sample_statistics_html(request):
    result_settings = sm_settings.objects.using('sm_main').only("id", "name").order_by('-id')
    result_list = []
    for item in result_settings:
        id = item.id
        name = item.name
        tMp_dict = {}
        tMp_dict["id"] = id
        tMp_dict["id2name"] = str(id) + "_" + str(name)
        result_list.append(tMp_dict)
    content = {
        "result_list": result_list
    }
    return render(request, 'sample_manage/sample_statistics.html', content)


def sample_download_html(request):
    result_settings = sm_settings.objects.using('sm_main').only("id", "name").order_by('-id')
    result_list = []
    for item in result_settings:
        id = item.id
        name = item.name
        tMp_dict = {}
        tMp_dict["id"] = id
        tMp_dict["id2name"] = str(id) + "_" + str(name)
        result_list.append(tMp_dict)
    content = {
        "result_list": result_list
    }
    return render(request, 'sample_manage/sample_download.html', content)

def sample_label_html(request):
    return render(request,'sample_manage/sample_label.html')
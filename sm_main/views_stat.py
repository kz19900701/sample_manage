#!/usr/bin/env python
#-*- coding=utf-8 -*-


from django.shortcuts import render
from sm_main.models import content as sm_content,content_group as sm_group,settings as sm_setting
from .models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from xlwt import *
import os
import io
import datetime
from itertools import islice
import json
from django.http import JsonResponse
from django.http import HttpResponseRedirect
#用于setting change时候
def stat_status_query_api(request):

    if request.method =="POST":
        settings_id = request.POST['setting_id']
        # to_database_list = json.loads(settings.objects.get(id=settings_id).to_database)
        # db1 = to_database_list[0]
        # db2 = to_database_list[1]
        result={}
        try:
            filedir_name = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'download_file',"stat",settings_id)
            db_list = os.listdir(filedir_name)
            print(filedir_name)
            if os.path.exists(filedir_name):

                result['is_finish_stat']=True
                result["fpm_in"] = db_list[0]
                result["fpm_out"] = db_list[1]
        except:
            result['is_finish_stat'] = False
        print(result)
        return JsonResponse(result)


# 开始统计
def sample_stat_api(request):

    if request.method =='POST':
        settings_id = request.POST['settings_id']
        sm_groups = sm_group.objects.using('sm_main').filter(settings_id=settings_id)
        sm_settings = sm_setting.objects.using('sm_main').get(id=int(settings_id))
        settings_name = sm_settings.name
        databases = json.loads(sm_settings.to_database)

        tmp_dict = {}
        for db in databases:
            tmp_dict[db] = {}
            for item in sm_groups:
                count = sm_content.objects.using('sm_main').filter(group_id=item.id).count()
                tmp_dict[db][item.id]={}
                tmp_dict[db][item.id]['sum_count'] = int(count)
                tmp_dict[db][item.id]['count'] = int(count)

        print(tmp_dict)
        # 计算每组的正确率
        double_check_contents = sm_content.objects.using('sample_double_check').filter(settings_id=settings_id).only('id','comments','key_positions','class_list')
        for db in databases:
            for double_check_item in double_check_contents:
                # id = double_check_item.comments
                id = double_check_item.id
                db_content = sm_content.objects.using(db).get(id=id)
                group_id = db_content.group_id

                if double_check_item.key_positions != db_content.key_positions or double_check_item.class_list!=db_content.class_list:
                    tmp_dict[db][group_id]['count'] -= 1

        # 计算每组的正确率
        user_dict={}
        for source,items in tmp_dict.items():
            user_dict[source] = []
            for group_id,score in items.items():
                userid = sm_group.objects.using(source).get(id=group_id).user_id
                tmp = {}
                tmp['user_id']=userid
                tmp['user_name'] = User.objects.using(source).get(id=userid).username
                tmp['group_name'] = content_group.objects.using('sm_main').filter(settings_id=settings_id).get(id=group_id).name
                tmp['group_id'] = group_id
                tmp['accuracy'] = round(tmp_dict[source][group_id]['count']/tmp_dict[source][group_id]['sum_count'],2)
                tmp['accuracy_count'] = round(tmp_dict[source][group_id]['count'])
                tmp['sum_count'] = tmp_dict[source][group_id]['sum_count']
                tmp['settings_id']=settings_id
                tmp['database'] = source
                user_dict[source].append(tmp)

        print(user_dict)
        #
        statistic_info.objects.using('sm_main').filter(settings_id=settings_id).delete()

        objs = ""
        batch_size = 100
        for database,items_list in user_dict.items():
            objs = (statistic_info(
                user_id = item_dict['user_id'],
                group_id = item_dict['group_id'],
                group_name = item_dict['group_name'],
                accuracy = item_dict['accuracy'],
                accuracy_count = item_dict['accuracy_count'],
                sum_count = item_dict['sum_count'],
                settings_id = settings_id,
                database = database
            ) for item_dict in items_list)

            while True:
                batch = list(islice(objs, batch_size))
                if not batch:
                    break
                statistic_info.objects.using('sm_main').bulk_create(batch, batch_size)

        content = {}
        # 创建工作薄
        for database, items in user_dict.items():
            ws = Workbook(encoding='utf-8')
            w = ws.add_sheet(database)
            w.write(0, 0, "批次名称")
            w.write(0, 1, "用户名")
            w.write(0, 2, "任务组名称")
            w.write(0, 3, "正确率")
            w.write(0, 4, "正确条数")
            w.write(0, 5, "完成条数")
            excel_row = 1
            w.write(excel_row, 0, settings_name)
            for item in items:
                w.write(excel_row, 1, item['user_name'])
                w.write(excel_row, 2, item["group_name"])
                w.write(excel_row, 3, item["accuracy"])
                w.write(excel_row, 4, item["accuracy_count"])
                w.write(excel_row, 5, item["sum_count"])
                excel_row += 1
            today = str(datetime.date.today())
            filename =  settings_name+"_"+database + "_result.xls"
            filedir_name = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'download_file',"stat",settings_id,database)
            if not os.path.exists(filedir_name):
                os.makedirs(filedir_name)
            filedir_name = os.path.join(filedir_name,filename)
            print(filedir_name)
            ws.save(filedir_name)

        content['is_finish_stat']=True
        print(content)
        # return render(request, 'sample_manage/sample_statistics.html', content)
        return HttpResponseRedirect('sample_statistics_html')


def stat_download_api(request,a,b):

    filedir_name = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'download_file', "stat", a,b)
    file_path = os.listdir(filedir_name)[0]
    the_file_name = os.path.join(filedir_name, file_path)
    from django.http import StreamingHttpResponse
    file = open(the_file_name, 'rb')
    response = StreamingHttpResponse(file)
    response['Content-Type']='application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment; filename='+file_path
    return response


def file_iterator(file, chunk_size=512):
    with open(file) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def get_excel_stream(file):
    # StringIO操作的只能是str，如果要操作二进制数据，就需要使用BytesIO。
    excel_stream = io.BytesIO()
    # 这点很重要，传给save函数的不是保存文件名，而是一个BytesIO流（在内存中读写）
    file.save(excel_stream)
    # getvalue方法用于获得写入后的byte将结果返回给re
    res = excel_stream.getvalue()
    excel_stream.close()
    return res

# def stat_download_api(request):
#     if request.method =='POST':
#         settings_id = request.POST['settings_id']
#         s = settings.objects.using('sm_main').get(id=settings_id)
#         name = s.name
#         filedir_name = os.path.join(os.path.dirname(os.path.abspath('__file__')),'download_file','sample',str(datetime.date.today()),name)
#         if not os.path.exists(filedir_name):
#             os.makedirs(filedir_name)
#         contents  =content.objects.using('sm_main').filter(settings_id=settings_id).only('id',"content",'group_id',"key_positions",'class_list')
#         total_count = contents.count()
#         page_size = 100
#         page = total_count / page_size
#         if page <1:
#             page=1
#         # save
#         file_map={}
#
#         for i in range(int(page)):
#             start = i*100
#             end = (i+1)*100
#             part_contents = contents[start:end]
#             for row in part_contents:
#                 obj = {
#                     "id": row.id,
#                     "content": row.content,
#                     "group_id": row.group_id,
#                     "class_list": row.class_list,
#                     "key_postiions":row.key_positions
#                 }
#                 if not obj['group_id'] in file_map.keys():
#                     file_name = os.path.join(filedir_name,str(obj['group_id']) + '.txt')
#                     fw_temp = codecs.open(file_name, 'w', 'utf-8')
#                     file_map[obj['group_id']] = fw_temp
#                 fw = file_map[obj['group_id']]
#                 fw.write(json.dumps(obj=obj, ensure_ascii=False) + "\n")
#
#         for key in file_map.keys():
#             file_map[key].flush()
#             file_map[key].close()
#         print("completed!")
#         z_name = 'export.zip'
#         z_name = os.path.join(os.path.dirname(os.path.abspath('__file__')), z_name)
#         z_file = zipfile.ZipFile(z_name, 'w')
#         file_list= os.listdir(filedir_name)
#         for file_path in file_list:
#             file = os.path.join(filedir_name,file_path)
#             z_file.write(file)
#         z_file.close()
#
#         z_file = open(z_name, 'rb')
#         data = z_file.read()
#         z_file.close()
#
#         response = HttpResponse(data, content_type='application/zip')
#         response['Content-Disposition'] = 'attachment;filename=' + str(settings_id)+"_"+name+".zip"
#         return response

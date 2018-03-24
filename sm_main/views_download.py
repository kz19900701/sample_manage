#!/usr/bin/env python
#-*- coding=utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from sm_main.models import content,settings
import codecs,os,json,zipfile
import datetime

def sample_download_api(request):
    if request.method =='POST':
        settings_id = request.POST['settings_id']
        s = settings.objects.using('sm_main').get(id=settings_id)
        name = s.name
        filedir_name = os.path.join(os.path.dirname(os.path.abspath('__file__')),'download_file','sample',str(datetime.date.today()),name)
        if not os.path.exists(filedir_name):
            os.makedirs(filedir_name)
        contents  =content.objects.using('sm_main').filter(settings_id=settings_id).only('id',"content",'group_id',"key_positions",'class_list')
        total_count = contents.count()
        page_size = 100
        page = total_count / page_size
        if page <1:
            page=1
        # save
        file_map={}

        for i in range(int(page)):
            start = i*100
            end = (i+1)*100
            part_contents = contents[start:end]
            for row in part_contents:
                obj = {
                    "id": row.id,
                    "content": row.content,
                    "group_id": row.group_id,
                    "class_list": row.class_list,
                    "key_positions":row.key_positions
                }
                if not obj['group_id'] in file_map.keys():
                    file_name = os.path.join(filedir_name,str(obj['group_id']) + '.txt')
                    fw_temp = codecs.open(file_name, 'w', 'utf-8')
                    file_map[obj['group_id']] = fw_temp
                fw = file_map[obj['group_id']]
                fw.write(json.dumps(obj=obj, ensure_ascii=False) + "\n")

        for key in file_map.keys():
            file_map[key].flush()
            file_map[key].close()
        print("completed!")
        z_name = 'export.zip'
        z_name = os.path.join(os.path.dirname(os.path.abspath('__file__')),z_name)
        z_file = zipfile.ZipFile(z_name, 'w')
        file_list= os.listdir(filedir_name)
        for file_path in file_list:
            file = os.path.join(filedir_name,file_path)
            z_file.write(file)
        z_file.close()

        z_file = open(z_name, 'rb')
        data = z_file.read()
        z_file.close()

        response = HttpResponse(data, content_type='application/zip')
        response['Content-Disposition'] = 'attachment;filename=' + str(settings_id)+"_"+name+".zip"
        return response


def file_iterator(file_name, chunk_size=512):
    with open(file_name,'r',encoding='utf-8') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
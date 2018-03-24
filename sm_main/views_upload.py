from django.shortcuts import render
from django.http import JsonResponse

import json
import datetime
from django.db.models import Max
from sm_main.models import content as sm_content,content_group as sm_group,settings as sm_settings
# from fpm_in.models import content as fpm_in_content, content_group as fpm_in_group,settings as fpm_in_settings
# from fpm_out.models import content as fpm_out_content,content_group as fpm_out_group,settings as fpm_out_settings
# from sample_double_check.models import content as double_check_content,content_group as double_check_group,settings as double_check_settings
from .forms import upload_form
import json

# api 上传到样本数据库
def sample_upload_api(request):
    if request.method=='POST':
        f = upload_form(request.POST,request.FILES)
        if f.is_valid():
            name = f.cleaned_data['name']
            settings = json.dumps(f.cleaned_data['settings'], ensure_ascii=False).replace('"',"'")
            setting_type = f.cleaned_data['setting_type']
            doc_file_path = f.cleaned_data['doc_file']
            is_single = f.cleaned_data['is_single']
            # # save settings,get setting_id and filename
            settings_id = save_settings_return_id(name, settings, setting_type,doc_file_path,is_single)
            file_path = f.cleaned_data['upload_file'].temporary_file_path()

            group_id_start = sm_group.objects.using('sm_main').only("id").aggregate(Max('id'))['id__max']
            content_id_start = sm_content.objects.using('sm_main').only("id").aggregate(Max('id'))['id__max']
            if not content_id_start:
                content_id_start = 0
            if not group_id_start:
                group_id_start=0
            group_id = group_id_start+1
            content_id= content_id_start+1
            # insert2Model
            rollback_str_list = []
            count,group_id = handle_uploaded_file(file_path,settings_id,name,group_id,content_id,rollback_str_list)

        else:
            content = {
                "form":f,
                "error":f.errors
            }
            print(content)
            return render(request,'sample_manage/sample_upload.html',content)
        content = {
            "content": {
                "setting_name": name,
                "sum_count": count,
                "group_count": group_id - group_id_start,
                'rollback_str_list':rollback_str_list
            }
        }

        return render(request, 'sample_manage/sample_upload.html',content)



def save_settings_return_id(name,settings_str,setting_type,doc_file_path,is_single):# 上传setting
    settings_id_start = sm_settings.objects.using('sm_main').only("id").aggregate(Max('id'))['id__max']
    if not settings_id_start:
        settings_id_start =0
    settings_id = settings_id_start+1

    # model
    sm = sm_settings.objects.using('sm_main').create(id=settings_id,
                                    name=name,
                                    settings=settings_str,
                                    setting_type=setting_type,
                                    is_single=is_single,
                                    doc_file_path=doc_file_path,
                                    to_database=[])
    print(sm.doc_file_path)
    settings_id = sm.id
    return settings_id

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.newdata = ""

    def handle_starttag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_endtag(self, tag):
        print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('<%s/>' % tag)

    def handle_data(self, data):
        self.newdata = data

    def handle_comment(self, data):
        print('<!--', data, '-->')

    def handle_entityref(self, name):
        print('&%s;' % name)

    def handle_charref(self, name):
        print('&#%s;' % name)

def handle_uploaded_file(file_path,settings_id,name,group_id,content_id,rollback_str_list): # 分发数据给3个mysql
    count = 0
    sampple_content_tmplist=[]
    batch_size = 100
    today = str(datetime.datetime.today())
    # 获取当前最大的group_id
    name = name+"_"+str(settings_id)+"_"  # group_name
    parser = MyHTMLParser()
    with open(file_path,'r',encoding='utf-8') as f:
        line = f.readline()
        line = line.strip().replace("'", "\\'")
        while line:
            count += 1
            parser.feed(line)
            content = parser.newdata
            sampple_content = sm_content(
                                        id=content_id,
                                        content=content,
                                        create_datetime=today,
                                        last_update_datetime=today,
                                        last_update_user=1,
                                        group_id=group_id,
                                        is_labeled=False,
                                        settings_id=settings_id,
                                        is_dirty_data=False)
            sampple_content_tmplist.append(sampple_content)
            if count %batch_size==0:
                    sm_content.objects.using('sm_main').bulk_create(sampple_content_tmplist,batch_size)
                    sm_group.objects.using('sm_main').create(id=group_id,
                                        name=name+str(group_id),
                                        create_datetime=today,
                                        last_update_datetime=today,
                                        last_update_user=1,
                                        settings_id=settings_id)
                    index_list = []
                    sampple_content_tmplist=[]
                    group_id += 1

            content_id+=1
            line = f.readline()
        if sampple_content_tmplist:
            sm_content.objects.using('sm_main').bulk_create(sampple_content_tmplist, batch_size)
            sm_group.objects.using('sm_main').create(id=group_id,
                                     name=name + str(group_id),
                                     create_datetime=today,
                                     last_update_datetime=today,
                                     last_update_user=1,
                                     settings_id=settings_id)

    f.close()
    parser.close()

    return count,group_id

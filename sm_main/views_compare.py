from django.shortcuts import render
from django.http import JsonResponse
from itertools import islice
import json
from itertools import islice
import datetime
from django.db.models import Max
import time
from sm_main.models import content as sm_content,content_group,settings

# api complete
def sample_compare_api(request):
    if request.method=='POST':
        settings_id = request.POST['settings_id']
        print(request.POST)
        # 初始化数据
        sm_content.objects.using("sm_main").filter(settings_id=settings_id).update(is_labeled=False,key_positions='',class_list='')
        sm_content.objects.using("sample_double_check").filter(settings_id=settings_id).delete()
        content_group.objects.using('sample_double_check').filter(settings_id=settings_id).delete()
        settings.objects.using('sample_double_check').filter(id=settings_id).delete()

        compare_main(settings_id) # compare and back and return diff ids_list
        # bulk_demo2(tmp_list,double_check_group_id) # insert into double check table
        sum_count = sm_content.objects.using('sm_main').filter(settings_id=settings_id).count()
        same_count = sm_content.objects.using('sm_main').filter(settings_id=settings_id).filter(is_labeled=True).count()
        diff_count = sm_content.objects.using('sm_main').filter(settings_id=settings_id).filter(is_labeled=False).count()
        print(sum_count,same_count,diff_count)
        # same
        content={
            "result":{
                "settings_id":settings_id,
                "sum_count": sum_count,
                "same_count": same_count,
                "diff_count": diff_count,
                "distribute":True
            }
        }
        return render(request,'sample_manage/sample_compare.html',content)

def bulk_demo2(tmp_list,double_check_group_id):
    batch_size =100
    objs = (sm_content(content=item.content,
                                 comments=item.id,
                                 group_id=double_check_group_id,
                                 settings_id=item.settings_id,
                                 )for item in sm_content.objects.using("sm_main").filter(id__in=tmp_list))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        sm_content.objects.using('sample_double_check').bulk_create(batch, batch_size)



# 对比逻辑
def compare_main(settings_id):
    to_database_list = json.loads(settings.objects.get(id=settings_id).to_database)
    db1 = to_database_list[0]
    db2 = to_database_list[1]
    t1_contents = sm_content.objects.using(db1).filter(settings_id=settings_id)
    for t1_content in t1_contents:
        t2_content = sm_content.objects.using(db2).get(id=t1_content.id)
        s = sm_content.objects.using('sm_main').get(id=t1_content.id)
        if t1_content.is_dirty_data==t2_content.is_dirty_data and t1_content.key_positions==t2_content.key_positions and t1_content.class_list==t2_content.class_list and t1_content.is_labeled==True and t2_content.is_labeled==True and t1_content.settings_id==t2_content.settings_id:
            s.is_labeled=True
            s.key_positions=t1_content.key_positions
            s.class_list=t1_content.class_list
            s.class_list = t1_content.is_dirty_data
            s.save(using="sm_main")


    # content_group.objects.using('sample_double_check').create(
    #     id=double_check_group_id,
    #     name="double_check_"+str(settings_id)+"_"+str(double_check_group_id),
    #     create_datetime=str(datetime.datetime.today()),
    #     last_update_datetime=str(datetime.datetime.today()),
    #     last_update_user=1,
    #     is_complete=False,
    #     settings_id=settings_id
    # )

def sample_double_check_distribute_api(request):

    if request.method=="POST":
        settings_id = request.POST['settings_id']
        print(settings_id)
        settings_id = request.POST['settings_id']
        need_double_check_list = sm_content.objects.using('sm_main').filter(settings_id=int(settings_id)).filter(is_labeled=False)
        max_id_group = content_group.objects.using('sample_double_check').order_by("-id").first()
        if max_id_group:
            max_id = max_id_group.id+1
        else:
            max_id =1
        settings_main = settings.objects.using('sm_main').get(id=settings_id)
        settings.objects.using('sample_double_check').create(
            id=settings_id,
            name = settings_main.name,
            settings = settings_main.settings,
            comments = settings_main.comments,
            setting_type = settings_main.setting_type,
            is_single = settings_main.is_single,
            doc_file_path = settings_main.doc_file_path,
        )
        content_group.objects.using('sample_double_check').create(
            id = max_id,
            name = settings_main.name,
            user_id = None,
            create_datetime = str(datetime.datetime.today()),
            last_update_datetime = str(datetime.datetime.today()),
            last_update_user =1,
            settings_id = int(settings_id),
        )
        count = 0
        sampple_content_tmplist = []
        batch_size =100
        for item in need_double_check_list:

            sampple_content = sm_content(
                id=item.id,
                content = item.content,
                key_positions = None,
                create_datetime = item.create_datetime,
                last_update_datetime = item.last_update_datetime,
                last_update_user = item.last_update_user,
                cost_time = item.cost_time,
                group_id = max_id,
                is_labeled = False,
                comments = item.comments,
                settings_id = item.settings_id,
                class_list = None
            )
            count += 1
            sampple_content_tmplist.append(sampple_content)
            if count % 100 == 0:
                sm_content.objects.using('sample_double_check').bulk_create(sampple_content_tmplist, batch_size)
                sampple_content_tmplist = []
        sm_content.objects.using("sample_double_check").bulk_create(sampple_content_tmplist, batch_size)

        content = {
            "result":"分发成功"
        }
        return render(request,'sample_manage/show_result.html',content)
        # return JsonResponse(content)

# 查看已选批次数据情况
def sample_compare_query_data(request):
    if request.method=="POST":
        print(request.POST)
        settings_id = request.POST['settings_id']
        to_database_list = json.loads(settings.objects.get(id=settings_id).to_database)
        content_list =[]
        for db in to_database_list:
            is_complete = content_group.objects.using(db).filter(is_complete=True).filter(settings_id=settings_id).count()
            is_not_complete = content_group.objects.using(db).filter(is_complete=False).filter(
                settings_id=settings_id).count()
            sum_count = content_group.objects.using(db).filter(settings_id=settings_id).count()
        # fpm_is_complete = content_group.objects.using('fpm_in').filter(is_complete=True).filter(settings_id=settings_id).count()
        # fpm_is_not_complete = content_group.objects.using('fpm_in').filter(is_complete=False).filter(settings_id=settings_id).count()
        # fpm_sum_count = content_group.objects.using('fpm_in').filter(settings_id=settings_id).count()
        # test_is_complete = content_group.objects.using('fpm_out').filter(is_complete=True).filter(settings_id=settings_id).count()
        # test_is_not_complete = content_group.objects.using('fpm_out').filter(is_complete=False).filter(settings_id=settings_id).count()
        # test_sum_count = content_group.objects.using('fpm_out').filter(settings_id=settings_id).count()
            result={
                "db":db,
                "Count_sum":sum_count,
                "is_complete":is_complete,
                "is_not_complete":is_not_complete
            }
            content_list.append(result)

        content = {
            "result":content_list,
        }
        return JsonResponse(content)


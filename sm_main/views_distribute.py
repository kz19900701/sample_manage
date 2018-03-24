from django.shortcuts import render
from django.http import JsonResponse
from .models import content as Content,content_group as ContentGroup,settings as Settings
import json
def sample_distribute_api(request):

    if request.method =='POST':
        database_list = request.POST.getlist('database')
        settings_id = request.POST['settings_id']

        distribute2otherDB(settings_id, database_list)

        ss = Settings.objects.using('sm_main').get(id=settings_id)
        ss.to_database = json.dumps(database_list, ensure_ascii=False)
        ss.save()
        content = {
            "result":"分发成功"
        }
        return render(request,'sample_manage/show_result.html',content)

# 分发逻辑
def distribute2otherDB(settings_id,database_list):
    sampple_content_tmplist = []
    count = 0
    sm_content_ids = Content.objects.using('sm_main').filter(settings_id=settings_id).only('id')
    batch_size =100
    # sm_content_ids_start = sm_content_ids.first()
    # sm_content_ids_count = sm_content_ids.count()
    # content
    for item in sm_content_ids:
        sm_content = Content.objects.using('sm_main').get(id=int(item.id))
        count += 1
        sampple_content = Content(
                        id=sm_content.id,
                        content=sm_content.content,
                        create_datetime=sm_content.create_datetime,
                        last_update_datetime=sm_content.last_update_datetime,
                        last_update_user=1,
                        group_id=sm_content.group_id,
                        is_labeled=False,
                        settings_id=sm_content.settings_id,
                        is_dirty_data=False)

        sampple_content_tmplist.append(sampple_content)
        if count % 100 == 0:
            for database in database_list:
                Content.objects.using(database).bulk_create(sampple_content_tmplist, batch_size)
            sampple_content_tmplist = []
    for database in database_list:
        Content.objects.using(database).bulk_create(sampple_content_tmplist, batch_size)


    sm_groups = ContentGroup.objects.using('sm_main').filter(settings_id=int(settings_id))
    for sm_group in sm_groups:
        for database in database_list:
            ContentGroup.objects.using(database).create(
                id=sm_group.id,
                name = sm_group.name,
                user_id = sm_group.user_id,
                create_datetime = sm_group.create_datetime,
                last_update_datetime = sm_group.last_update_datetime,
                last_update_user = sm_group.last_update_user,
                is_complete = sm_group.is_complete,
                settings_id = sm_group.settings_id
            )

    sm_settings = Settings.objects.using('sm_main').get(id=int(settings_id))

    for database in database_list:
        Settings.objects.using(database).create(
            id=sm_settings.id,
            name =sm_settings.name,
            settings = sm_settings.settings,
            comments = sm_settings.comments,
            setting_type = sm_settings.setting_type,
            is_single = sm_settings.is_single,
            doc_file_path = sm_settings.doc_file_path
        )

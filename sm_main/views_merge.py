#!/usr/bin/env python
#-*- coding=utf-8 -*-
from django.http import JsonResponse
from sm_main.models import content as sm_content,content_group as sm_group,settings as sm_settings
from django.shortcuts import render


def sample_merge_api(request):

    if request.method=='POST':
        settings_id = int(request.POST['settings_id'])

        # merge main
        merge_main(settings_id)

        sum_count = sm_content.objects.using('sm_main').filter(settings_id=settings_id).count()
        is_labeled = sm_content.objects.using('sm_main').filter(settings_id=settings_id).filter(is_labeled=True).count()
        is_not_labeled = sm_content.objects.using('sm_main').filter(settings_id=settings_id).filter(is_labeled=False).count()

        if not is_not_labeled:
            sm_group.objects.using('sm_main').filter(settings_id=settings_id).filter(is_complete=False).update(is_complete=True)
        content = {
            "result": {
                "settings_id": settings_id,
                "sum_count": sum_count,
                "is_labeled": is_labeled,
                "is_not_labeled": is_not_labeled
            }
        }
        return render(request, 'sample_manage/sample_merge.html', content)
# 主方法
def merge_main(settings_id):
    unmerge_contents = sm_content.objects.using('sample_double_check').filter(settings_id=settings_id).filter(is_labeled=True)
    for item in unmerge_contents:
        s = sm_content.objects.using('sm_main').get(id=item.id)
        s.key_positions=item.key_positions
        s.class_list=item.class_list
        s.is_labeled=True
        s.is_dirty_data = item.is_dirty_data
        s.save(using="sm_main")

#  查看按钮
def sample_merge_query_data(request):
    if request.method == "POST":
        settings_id = request.POST['settings_id']
        sm_content_labeled = sm_content.objects.using('sm_main').filter(settings_id=settings_id).filter(is_labeled=True).count()
        sm_content_not_labeled = sm_content.objects.using('sm_main').filter(settings_id=settings_id).filter(is_labeled=False).count()
        sm_content_sum_count = sm_content.objects.using('sm_main').filter(settings_id=settings_id).count()
        double_check_content_labeled = sm_content.objects.using('sample_double_check').filter(settings_id=settings_id).filter(is_labeled=True).count()
        double_check_content_not_labeled = sm_content.objects.using('sample_double_check').filter(settings_id=settings_id).filter(is_labeled=False).count()
        double_check_content_sum_count = sm_content.objects.using('sample_double_check').filter(settings_id=settings_id).count()
        result_fpm_in = {
            "Count_sum": sm_content_sum_count,
            "is_complete": sm_content_labeled,
            "is_not_complete": sm_content_not_labeled
        }
        result_fpm_out = {
            "Count_sum": double_check_content_sum_count,
            "is_complete": double_check_content_labeled,
            "is_not_complete": double_check_content_not_labeled
        }
        content = {
            "result_db1": result_fpm_in,
            "result_db2": result_fpm_out
        }
        return JsonResponse(content)

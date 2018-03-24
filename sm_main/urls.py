#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views_upload,views_html,views_compare,views_merge,views_download,views_stat,views_distribute,views_delete
app_name = 'sample_manage'

urlpatterns = [
    # go2跳转页面
    url(r'^$', views_html.sample_upload_html, name="sample_upload_html"),
    url(r'^sample_upload_html', views_html.sample_upload_html, name="sample_upload_html"),
    url(r'^sample_distribute_html',views_html.sample_distribute_html,name='sample_distribute_html'),
    url(r'^sample_compare_html', views_html.sample_compare_html, name="sample_compare_html"),
    url(r'^sample_merge_html', views_html.sample_merge_html, name="sample_merge_html"),
    url(r'^sample_statistics_html', views_html.sample_statistics_html, name="sample_statistics_html"),
    url(r'^sample_download_html', views_html.sample_download_html, name="sample_download_html"),
    url(r'^sample_delete_html', views_html.sample_delete_html, name="sample_delete_html"),

    # api
    url(r'^sample_delete_api$',views_delete.sample_delete_api,name="sample_delete_api"),
    url(r'^sample_upload_api$', views_upload.sample_upload_api, name="sample_upload_api"),
    url(r'^sample_distribute_api$', views_distribute.sample_distribute_api, name="sample_distribute_api"),
    url(r'^sample_compare_api$', views_compare.sample_compare_api, name="sample_compare_api"),
    url(r'^sample_merge_api$', views_merge.sample_merge_api, name="sample_merge_api"),
    url(r'^sample_download_api$', views_download.sample_download_api, name="sample_download_api"),
    url(r'^sample_stat_api$',views_stat.sample_stat_api,name="sample_stat_api"),
    url(r'^sample_double_check_distribute_api$',views_compare.sample_double_check_distribute_api, name="sample_double_check_distribute_api"),
    # url(r'^stat_download_api',views_stat.stat_download_api,name="stat_dow/nload_api"),
    url(r'^stat_status_query_api',views_stat.stat_status_query_api,name='stat_status_query_api'),
    # 查询数据情况api
    url(r'^sample_compare_query_data$',views_compare.sample_compare_query_data,name="sample_compare_query_data"),
    url(r'^sample_merge_query_data$', views_merge.sample_merge_query_data, name="sample_merge_query_data"),
    # url(r'^sample_compare_api$', test_views.test, name="sample_compare_api"),
    url(r'^download_stat_file-(?P<a>\w+)-(?P<b>\w+)$',views_stat.stat_download_api,name="stat_download_api")
]
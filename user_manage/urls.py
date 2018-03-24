#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views
app_name = 'user_manage'

urlpatterns = [
    # go2跳转页面
    url(r'^$', views.user_manage_html, name="user_manage_html"),

]
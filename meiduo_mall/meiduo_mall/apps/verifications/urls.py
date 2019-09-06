#!/usr/bin/env python
# coding:utf-8
# Created by  on 18-12-22
# Copyright (c) 2018 $USER.ALL rights reserved.
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view()),
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
]
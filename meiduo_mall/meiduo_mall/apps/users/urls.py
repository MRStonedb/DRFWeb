#!/usr/bin/env python
# coding:utf-8
# Created by  on 18-12-22
# Copyright (c) 2018 $USER.ALL rights reserved.
from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    url(r'^users/$', views.UserView.as_view()), # 注册
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),  # 判断用户名是否存在接口
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),   # 判断手机号是否存在接口
    url(r'^authorizations/$', obtain_jwt_token),   # 登陆
    url(r'^user/$', views.UserDetailView.as_view()),
    url(r'^email/$', views.EmailView.as_view()),
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    url(r'^browse_histories/$', views.UserBrowsingHistoryView.as_view()),
]

router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet, base_name='addresses')

urlpatterns += router.urls



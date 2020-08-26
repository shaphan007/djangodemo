# coding=gbk

from django.contrib import admin
from django.conf.urls import url, include
from django.urls import re_path as path
from sign import views_if

urlpatterns = [
    path(r'^add_event/', views_if.add_event, name='add_event'),
    path(r'^login/', views_if.login, name='login'),
]

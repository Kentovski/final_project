# -*- coding: utf-8 -*-

from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^results/(?P<query>[\w|\W]+)/$', views.ResultsView.as_view(), name='results'),
    url(r'^statistic/$', views.StatisticView.as_view(), name='statistic'),
    url(r'^send_request/', views.SendRequestView.as_view(), name='send_request'),
    url(r'^check_task/(?P<task_id>[-\w]+)/$', views.CheckTaskView.as_view(), name='check_task'),
]

from django.conf.urls import *

import views

urlpatterns = patterns('',
    url(r'^stats/$', views.stats, name='account-stats'),
    url(r'^', views.account, name='account-detail'),
)

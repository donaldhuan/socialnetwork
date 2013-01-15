from django.conf.urls import patterns, include, url
#from socialnetwork.weibo.views import *

urlpatterns = patterns('weibo.views',
        url(r'^home$', 'home'),
        url(r'^status_fans$', 'status_fans'),
        url(r'^management_fans$', 'management_fans'),
        url(r'^weibotools$', 'weibotools'),
        )

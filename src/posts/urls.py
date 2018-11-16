from django.conf.urls import url
from django.contrib import admin
from .views import (
	posts_list,
	posts_create,
	posts_detail,
	posts_update,
	posts_delete,
	no_staff
	)


urlpatterns = [
    
    url(r'^$', posts_list, name='list'),
    url(r'^create/$', posts_create),
    url(r'^(?P<id>\d+)/$', posts_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', posts_update),
    url(r'^(?P<id>\d+)/delete/$', posts_delete),
    url(r'^nostaff/$',no_staff),
]
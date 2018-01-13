from django.conf.urls import url, include

from .views import (
	post_list,
	post_create,
	post_detail,
	post_update,
	post_delete,
	# like_count_blog, 
	# post_like,
	)

urlpatterns = [

    # url(r'^$', post_list, name='list'),
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create),    
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    # url(r'^(?P<id>\d+)/$', post_like, name='like'),
    # url(r'^like-blog/$', like_count_blog, name='like_count_blog'),

]

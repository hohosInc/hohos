from django.conf.urls import url
from .views import (
	basics,
	effects,
	interactions,
	widgets, 
	file_upload,
	test,
	)
from . import views
 
urlpatterns = [ 

	url(r'^$', basics, name='basics'),
	url(r'^effects$', effects, name='effects'),
	url(r'^interactions$', interactions, name='interactions'),
	url(r'^widgets$', widgets, name='widgets'),
	url(r'^test$', test, name='test'),
	# url(r'^file_upload$', file_upload, name='file_upload'),
	# url(r'^basic-upload/$', views.BasicUploadView.as_view(), name='basic_upload'),

]
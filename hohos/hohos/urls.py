from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
# from .views import MyRegistrationView
from newsletter.views import (
    home,
    contact,
    about,
    test,
    )
from django.contrib.auth.views import (
    password_change,
    password_change_done,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
    )
 
urlpatterns = [

    url(r'^$', home, name='home'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^about/$', about, name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^posts/', include('posts.urls',namespace='posts')), 
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^accounts/',include('accounts.urls', namespace='accounts')),
    url(r'^test/$',test, name='test'),
    url(r'^password_change/$', password_change, name='password_change'),
    url(r'^password_change/done/$', password_change_done, name='password_change_done'),
    url(r'^password_reset/$', password_reset, name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),


    
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




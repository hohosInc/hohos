from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
# from .views import MyRegistrationView
from .views import (
    registration,
    Login,
    Logout,
    )
# from django.contrib.auth.views import (
# 	password_change,
# 	password_change_done,
# 	password_reset,
# 	password_reset_done,
# 	password_reset_confirm,
# 	password_reset_complete,
# 	)

urlpatterns = [

    url(r'^register/$', registration, name='register'),
    url(r'^login/$', Login, name='login'),
    url(r'^logout/$', Logout, name='logout'),
    # url(r'^password_change/$', password_change, name='password_change'),
    # url(r'^password_change/done/$', password_change_done, name='password_change_done'),
    # url(r'^password_reset/$', password_reset, name='password_reset'),
    # url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #  			password_reset_confirm, name='password_reset_confirm'),
    # url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),

]





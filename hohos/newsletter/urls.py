from django.conf import settings
from django.conf.urls import include, url

from .views import (
		knowPeople,
		# invite_old_users,
	)
       
urlpatterns = [     
     
    url(r'^knowpeople/$', knowPeople , name='knowpeople'),
    # url(r'^inviting-old-users/$', invite_old_users, name='invite_old_users'),
	 
]


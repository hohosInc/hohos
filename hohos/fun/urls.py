from django.conf.urls import url
from .views import(

		funhome,
		fungone,
	)


urlpatterns = [

url(r'^stop_trolling_gattu$', funhome, name='funhome'),
url(r'^gattu_a_love_story_in_order_of_n3$', fungone, name='fungone'),

]  
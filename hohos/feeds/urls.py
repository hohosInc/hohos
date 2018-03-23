from django.conf.urls import url

from feeds import views  
     
     # (?P<id>\d+)/

urlpatterns = [    
    url(r'^$', views.feeds, name='feeds'),
    url(r'^(?P<id>\d+)/$', views.feed, name='feeds'),
    url(r'^response/(?P<id>\d+)/$', views.specialfeeds, name='special_feeds'), 
    # url(r'^challenge/(?P<id>\d+)/$', views.specific_challenge_feeds, name='specific_challenge_feeds'),    
    url(r'^challenge/$', views.challengefeeds, name='challenge_feeds'),
    url(r'^new_post/$', views.new_post, name='new_post'),
    url(r'^post/$', views.post, name='post'), # on profile
    url(r'^post/email/$', views.email_on_post, name='email_on_post'), # for sending mail to user on whoes profile, some user has written    

    url(r'^like/$', views.like, name='like'), 
    url(r'^profile_like/$', views.profile_like, name='profile_like'),    
    url(r'^comment/$', views.comment, name='comment'),  
    url(r'^load/$', views.load, name='load'),  
    url(r'^check/$', views.check, name='check'), 
    url(r'^load_new/$', views.load_new, name='load_new'),    
    url(r'^update/$', views.update, name='update'), 
    url(r'^profile_update/$', views.profile_update, name='profile_update'),    
    url(r'^track_comments/$', views.track_comments, name='track_comments'),
    url(r'^remove/$', views.remove, name='remove_feed'),  
    url(r'^(\d+)/$', views.feed, name='feed'),
    
    url(r'^userinfo/$', views.userinfo, name='userinfo'),
    url(r'^tiptest/$', views.tiptest, name='tiptest'),

    #profile feeds - openchat
    url(r'^openchat/h_h/$', views.profilefeeds_h_h, name='profilefeeds_h_h'),    
    url(r'^openchat/p_p/$', views.profilefeeds_p_p, name='profilefeeds_p_p'),
    url(r'^openchat/h_p/$', views.profilefeeds_h_p, name='profilefeeds_h_p'),
    url(r'^openchat/p_h/$', views.profilefeeds_p_h, name='profilefeeds_p_h'),

] 
      
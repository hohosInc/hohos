from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static  
from django.contrib import admin   
from django.contrib.auth import views as auth_views

from activities import views as activities_views
from authentication import views as hohos_auth_views
from core import views as core_views
from search import views as search_views
from newsletter.views import (
    about, contact, home_out, privacyPolicy, hohostos,
    )  
from django.contrib.auth.views import ( 
    password_reset,
    password_reset_done, 
    password_reset_confirm,    
    password_reset_complete,     
    )   
       

urlpatterns = [          
    # url(r'^$',core_views.wait,name='wait'),
    url(r'^googleb5ffb42fb0a2feb6.html/$', core_views.crawl, name='crawl'),
    url(r'^sitemap/$', core_views.sitemap, name='sitemap'),

    url(r'^$', core_views.home , name='home'),
    

    url(r'^interactions/', include('newsletter.urls',namespace='interactions')),
    
    url(r'^mission_ajax/', include('mission_ajax.urls', namespace='ajax')),
    url(r'^fun/', include('fun.urls', namespace='fun')),    
    url(r'^accounts/social/login/cancelled/$', core_views.login_cancelled),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^login', auth_views.login, {'template_name': 'core/cover.html'}, 
        name='login'), 
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/human$', hohos_auth_views.signup_human, name='signup_human'),
    url(r'^signup/products$', hohos_auth_views.signup_products, name='signup_products'),    

    url(r'^passwordreset/$', password_reset, name='password_reset'),
    url(r'^passwordreset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),

    url(r'^contact/$', contact, name='contact'),
    url(r'^about/$', about, name='about'),
    url(r'^privacy/$', privacyPolicy, name='privacy'),
    url(r'^terms/$', hohostos, name='tos'),
    url(r'^invite/$', core_views.invite, name='invite'), 
    url(r'^introho/$', core_views.introho, name='introho'),


    # url(r'^settings/', include('core.urls',namespace='core')),

    url(r'^settings/human/$', core_views.settings_human, name='settings_human'),
    url(r'^settings/products/$', core_views.settings_products, name='settings_products'),
    url(r'^settings/picture/$', core_views.picture, name='picture'),
    url(r'^settings/profilepicupload/$', core_views.profile_pic_upload, name='profile_pic_upload'),
    url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^settings/hohos-digest/$', core_views.hohos_digest, name='hohos_digest'),

    url(r'^peopleproducts/$', core_views.network, name='network'),  
    url(r'^networktest/$', core_views.network_test, name='network_test'),
    url(r'^feeds/', include('feeds.urls')),
    url(r'^notifications/$', activities_views.notifications,     
        name='notifications'), 
    url(r'^notifications/last/$', activities_views.last_notifications,
        name='last_notifications'),
    url(r'^notifications/check/$', activities_views.check_notifications,
        name='check_notifications'),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^searchusers/$', search_views.searchusers, name='searchusers'),
    url(r'^searchusers_simple/$', search_views.searchusers_simple, name='searchusers_simple'),

    url(r'^(?P<username>[^/]+)/$', core_views.profile, name='profile'),
    url(r'^(?P<username>[^/]+)/likers/$', core_views.profile_likers, name='profile_likers'),
    url(r'^(?P<username>[^/]+)/likesto/$', core_views.likes_to, name='likes_to'),

    url(r'^(?P<username>[^/]+)/activities/$', core_views.profile_talks_by_page_user, name='userfeeds'),
    url(r'^challenges/for/(?P<username>[^/]+)/$', core_views.challenges_for_page_user, name='challenges_for_page_user'),
    url(r'^responses/by/(?P<username>[^/]+)/$', core_views.responses_by_page_user, name='responses_by_page_user'),
    url(r'^challenges/by/(?P<username>[^/]+)/$', core_views.challenges_by_page_user, name='challenges_by_page_user'),
    url(r'^profile-talks/by/(?P<username>[^/]+)/$', core_views.profile_talks_by_page_user, name='profile_talks_by_page_user'),

    url(r'^like/$', core_views.profile, name='profile_like'),
    url(r'^(?P<username>[^/]+)/$', core_views.profile_unlike, name='profile_unlike'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),

    url(r'^iprestrict/', include('iprestrict.urls', namespace='iprestrict')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
   
#!/usr/bin/python3
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible 

import json     
import time, datetime 
from django.contrib.auth.models import User 
from os.path import splitext, basename
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)  
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse   
from django.template.context_processors import csrf  
from django.template.loader import render_to_string     
  
from activities.models import Activity 
from hohos.decorators import ajax_required    
from feeds.models import Feed      
from feeds.forms import PhotoForm,FeedForm   
from authentication.models import Profile   
from PIL import Image, ImageFile 
from authentication.models import Profile
from django.core.mail import send_mail
from django.conf import settings as django_settings
import random

         
FEEDS_NUM_PAGES = 10       
 
   
@login_required  
def feeds(request): 
    print('inside feeds, feeds.view')
    print('gonna send style_feeds via feeds.views.feeds')
    #online_users =User.objects.all()
    recent_challenge_feeds = Feed.get_feeds().filter(Q(is_challenge=1)
                                              # & Q(date=datetime.date.today())
                                                ).order_by('-date')[:5]
    most_liked_challenge_feeds = Feed.get_feeds().filter(Q(is_challenge=1)
                                              # & Q(date=datetime.date.today())
                                                ).order_by('likes').reverse()
 
    if most_liked_challenge_feeds:
        randno =random.randint(1,20)
        response_for_id = most_liked_challenge_feeds[randno].id
        response_for_feed = get_object_or_404(Feed, id=response_for_id)
    else:
        response_for_feed = None 
        response_for_id = None 

    if response_for_id:
        style_feeds = Feed.get_feeds().filter(response_for=response_for_id)
    else:
        style_feeds = []

    paginator = Paginator(style_feeds, FEEDS_NUM_PAGES)
    style_feeds = paginator.page(1)

    from_feed = -1
    if style_feeds:
        from_feed = style_feeds[0].id

    return render(request, 'feeds/feeds.html', {
        'style_feeds': style_feeds,  #all feeds for response for feed
        #'online_users' : online_users,
        'from_feed': from_feed,
        'response_for_feed' : response_for_feed,
        'recent_challenge_feeds' : recent_challenge_feeds,
        'page': 1,

        })

@login_required 
def specialfeeds(request,id):
    print('inside feeds, feeds.view')
    print('gonna send special style_feeds via feeds.views.feeds')
    #online_users = User.objects.all().exclude(is_active=True)
    recent_challenge_feeds = Feed.get_feeds().filter(Q(is_challenge=1)
                                              # & Q(date=datetime.date.today())
                                                ).order_by('-date')[:5]    
    response_for = id
    style_feeds = Feed.get_feeds().filter(response_for=response_for)# 2nd lookup excludes all challenge feeds as they have is_challenge set to 1

    paginator = Paginator(style_feeds, FEEDS_NUM_PAGES)
    style_feeds = paginator.page(1)

    from_feed = -1
    if style_feeds: 
        from_feed = style_feeds[0].id

    response_for_feed = get_object_or_404(Feed, id=response_for)
    return render(request, 'feeds/special_feeds.html', {
        'style_feeds': style_feeds, 
        #'online_users' : online_users,
        'from_feed': from_feed, 
        'response_for_feed' : response_for_feed,   
        'recent_challenge_feeds' : recent_challenge_feeds,
        'page': 1,
        })


@login_required 
def challengefeeds(request):
    challenge_feeds = Feed.get_feeds().filter(is_challenge=1)
    paginator = Paginator(challenge_feeds, FEEDS_NUM_PAGES)
    challenge_feeds = paginator.page(1)

    from_feed = -1
    if challenge_feeds:
        from_feed = challenge_feeds[0].id
    most_liked_challenge_feeds = Feed.get_feeds().filter(Q(is_challenge=1)
                                              # & Q(date=datetime.date.today())
                                                ).order_by('likes').reverse()[:6]

    return render(request, 'feeds/challenge_feeds.html', {
        'challenge_feeds': challenge_feeds, 
        'from_feed': from_feed,
        'most_liked_challenge_feeds' : most_liked_challenge_feeds,
        'page': 1,
        })


@login_required 
def profilefeeds_h_h(request):
    most_active_profile_talks_h_h = Feed.get_feeds().filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=0)
                                                        & Q(to_user__profile__is_product=0)).order_by('likes').reverse()[:7]

    trending_people = Profile.objects.all().order_by('likes').reverse()[:10]
    
    human_human_profile_feeds = Feed.get_feeds().filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=0)
                                                        & Q(to_user__profile__is_product=0))
    mostliked_talks = human_human_profile_feeds.order_by('likes').reverse()[:5]

    paginator = Paginator(human_human_profile_feeds, FEEDS_NUM_PAGES)
    human_human_profile_feeds = paginator.page(1) # still to be made 
    
    from_feed = -1

    if human_human_profile_feeds:        
        from_feed = human_human_profile_feeds[0].id 

    return render(request, 'profile_feeds/human_human.html', {
        'human_human_profile_feeds' : human_human_profile_feeds, # profile feeds list
        'most_active_profile_talks_h_h' : most_active_profile_talks_h_h,
        'trending_people' : trending_people,
        'from_feed' : from_feed,        
        'page': 1, 
        })

@login_required 
def profilefeeds_p_p(request):
    most_active_profile_talks_p_p = Feed.get_feeds().filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=1)
                                                        & Q(to_user__profile__is_product=1)).order_by('likes').reverse()[:7]

    top_product_feeds = Feed.get_feeds().filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=1)
                                                        & Q(to_user__profile__is_product=1)).order_by('likes').reverse()[:10]
    product_product_profile_feeds = Feed.get_feeds().filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=1)
                                                        & Q(to_user__profile__is_product=1))
   
    paginator = Paginator(product_product_profile_feeds, FEEDS_NUM_PAGES)
    product_product_profile_feeds = paginator.page(1) # still to be made 
    
    from_feed = -1

    if product_product_profile_feeds:
        from_feed = product_product_profile_feeds[0].id 

    return render(request, 'profile_feeds/product_product.html', {
        'product_product_profile_feeds' : product_product_profile_feeds,
        'most_active_profile_talks_p_p' : most_active_profile_talks_p_p,
        'top_product_feeds':top_product_feeds,
        'from_feed' : from_feed,        
        'page': 1, 
        })

@login_required 
def profilefeeds_h_p(request):
    most_active_profile_talks_h_p = Feed.get_feeds().filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=0)
                                                        & Q(to_user__profile__is_product=1)).order_by('likes').reverse()[:7]

    top_feeds_h_p = Feed.get_feeds().filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=0)
                                                        & Q(to_user__profile__is_product=1)).order_by('likes').reverse()[:10]
    human_product_profile_feeds = Feed.get_feeds().filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=0)
                                                        & Q(to_user__profile__is_product=1))
   
    paginator = Paginator(human_product_profile_feeds, FEEDS_NUM_PAGES)
    human_product_profile_feeds = paginator.page(1) # still to be made 
    
    from_feed = -1

    if human_product_profile_feeds:
        from_feed = human_product_profile_feeds[0].id 

    return render(request, 'profile_feeds/human_product.html', {
        'human_product_profile_feeds' : human_product_profile_feeds,
        'most_active_profile_talks_h_p' : most_active_profile_talks_h_p,        
        'from_feed' : from_feed,  
        'top_feeds_h_p' : top_feeds_h_p,      
        'page': 1, 
        })

@login_required 
def profilefeeds_p_h(request):
    most_active_profile_talks_p_h = Feed.get_feeds().filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=1)
                                                        & Q(to_user__profile__is_product=0)).order_by('likes').reverse()[:7]

    top_feeds_p_h = Feed.get_feeds().filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=1)
                                                        & Q(to_user__profile__is_product=0)).order_by('likes').reverse()[:10]
    product_human_profile_feeds = Feed.get_feeds().filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=1)
                                                        & Q(to_user__profile__is_product=0))
   
    paginator = Paginator(product_human_profile_feeds, FEEDS_NUM_PAGES)
    product_human_profile_feeds = paginator.page(1) # still to be made 
    
    from_feed = -1

    if product_human_profile_feeds:
        from_feed = product_human_profile_feeds[0].id 

    return render(request, 'profile_feeds/product_human.html', {
        'product_human_profile_feeds' : product_human_profile_feeds,
        'most_active_profile_talks_p_h' : most_active_profile_talks_p_h,             
        'top_feeds_p_h' : top_feeds_p_h,      
        'from_feed' : from_feed,  
        'page': 1, 
        })


@login_required
def feed(request, id):
    feed = get_object_or_404(Feed, id=id)
    return render(request, 'feeds/feed.html', {'feed': feed})


def load(request):
    page = request.GET.get('page')

    # is_product_feed = request.GET.get('is_product_feed')
    from_feed = request.GET.get('from_feed') 
    all_feeds = Feed.get_feeds(from_feed) # to load the feeds older to feed with id from_feed
    feed_source = request.GET.get('feed_source')   
    profile_pk = request.GET.get('profile_pk') # it will come through only on  profile_feeds, Product_profile_feeds pages
    response_for_feed_id = request.GET.get('response_for_feed_id')
    page_user_name = request.GET.get('page_user_name')

    if page_user_name:
        page_user = get_object_or_404(User, username=page_user_name)
    # following for main feed line, that is styles copy feed
    # actually theres no need to get feed_from differently from all pages
    # just use same name from_feed for every page, it'll make the job of load function easy
    # from_feed_profile = request.GET.get('from_feed_profile')
 
    if feed_source == 'profile_talks_by_page_user':
        print('feed_source is : profile_talks_by_page_user')
        partial_feed_page = 'feeds/partial_feed_profile_activities.html'
        all_feeds = all_feeds.filter(Q(profile_pk__gt=0) & (Q(user=page_user) | Q(to_user=page_user)))

    elif feed_source == 'responses_by_page_user':
        print('feed_source is : responses_by_page_user')
        partial_feed_page = 'feeds/partial_feeds_feed.html'
        all_feeds = all_feeds.filter(Q(response_for__gt=0) & Q(user=page_user))

    elif feed_source == 'challenges_by_page_user':
        print('feed_source is : challenges_by_page_user')
        partial_feed_page = 'feeds/partial_challenge_feed.html'
        all_feeds = all_feeds.filter(Q(is_challenge=1) & Q(user=page_user))

    elif feed_source == 'human_human_profile_feeds':
        print('feed_source is : human_human_profile_feeds')
        partial_feed_page = 'feeds/partial_feed_profile.html'
        all_feeds = all_feeds.filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=0)
                                                        & Q(to_user__profile__is_product=0))

    elif feed_source == 'product_product_profile_feeds':
        print('feed_source is: product_product_profile_feeds')
        partial_feed_page = 'feeds/partial_feed_profile.html'
        all_feeds = all_feeds.filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=1)
                                                        & Q(to_user__profile__is_product=1))

    elif feed_source == 'human_product_profile_feeds':
        print('feed_source is: human_product_profile_feeds')
        partial_feed_page = 'feeds/partial_feed_profile.html'
        all_feeds = all_feeds.filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=0)
                                                        & Q(to_user__profile__is_product=1))

    elif feed_source == 'product_human_profile_feeds':
        print('feed_source is: product_human_profile_feeds')
        partial_feed_page = 'feeds/partial_feed_profile.html'
        all_feeds = all_feeds.filter(Q(profile_pk__gt=0) & Q(user__profile__is_product=1)
                                                        & Q(to_user__profile__is_product=0))

    elif feed_source == 'user_profile_feeds':  # come from profile.html page
        print('feed_source is: user_profile_feeds')
        all_feeds = all_feeds.filter(profile_pk=profile_pk)
        partial_feed_page = 'feeds/partial_feed_profile_page_user.html' # this all_feeds list has all the feeds related profile page he'/she's is on now

    # comes from user's activity page 
    elif feed_source == 'profile_talks_by_page_user': 
        print('feed_source is: profile_talks_by_page_user')
        all_feeds = all_feeds.filter(Q(user__id=page_user.id) & Q(profile_pk__gt=0)) # all feeds by anyuser containing styles if any shown by user and the feeds user said anything about their friends profiles
        partial_feed_page = 'feeds/partial_feed_profile.html'

    # elif feed_source == 'challenges_by_page_user': # comes from user's activity page
    #     print('feed_source is: challenges_by_page_user')
    #     all_feeds = all_feeds.filter(Q(user__id=page_user.id) & Q(is_challenge=1)) # all feeds by anyuser containing styles if any shown by user and the feeds user said anything about their friends profiles
    #     partial_feed_page = 'feeds/partial_challenge_feed.html'
    
    elif feed_source == 'responses_by_page_user': # comes from user's activity page
        print('feed_source is: responses_by_page_user')
        all_feeds = all_feeds.filter(Q(user__id=page_user.id) & Q(response_for__gt=0)) # all feeds by anyuser containing styles if any shown by user and the feeds user said anything about their friends profiles
        partial_feed_page = 'feeds/partial_feeds_feed.html'



    elif feed_source == 'challenge_feeds': # come from challenge_feeds page
        print('feed_source is: challenge_feeds')
        all_feeds = all_feeds.filter(is_challenge=1) # else all_feeds will be for style feedline which means it should not have any profile feedlines feed
        partial_feed_page = 'feeds/partial_challenge_feed.html'
    
    elif feed_source == 'special_feeds': 
        if response_for_feed_id:
            print('feed_source is: special_feeds with response_for_id:', response_for_feed_id)
            all_feeds = all_feeds.filter(response_for=response_for_feed_id)
            partial_feed_page = 'feeds/partial_feeds_feed.html'
        else:
            all_feeds = []
    for feed in all_feeds:
        print(feed.pk,feed.profile_pk,feed_source, feed.is_challenge)

    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    try:
        feeds = paginator.page(page)
    except PageNotAnInteger:
        return HttpResponseBadRequest()
    except EmptyPage:
        feeds = []
        
    html = ''
    csrf_token = (csrf(request)['csrf_token'])
    for feed in feeds:
        html = '{0}{1}'.format(html,
                               render_to_string(partial_feed_page,
                                                {
                                                    'feed': feed,
                                                    'user': request.user,
                                                    'csrf_token': csrf_token,
                                                    }))

    return HttpResponse(html)


@ajax_required
def product_product(request):
    feeds = Feed.get_feeds().filter(Q(to_user__profile__is_product=1) & Q(user__profile__is_product=1))

    if feeds: 
        partial_feed_page = 'feeds/partial_feed_profile.html'
        product_product_feeds = feeds
    else:
        product_product_feeds = []

    html = ''
    csrf_token = (csrf(request)['csrf_token'])
    for feed in product_product_feeds:
        html = '{0}{1}'.format(html,
                               render_to_string(partial_feed_page,
                                                {
                                                    'feed': feed,
                                                    'user': request.user,
                                                    'csrf_token': csrf_token,
                                                    }))

    return HttpResponse(html)


def load_new(request):
    user = request.user
    last_feed = request.GET.get('last_feed')
    feed_source = request.GET.get('feed_source')
    # is_product_feed = request.GET.get('is_product_feed')
    profile_pk = request.GET.get('profile_pk')
    response_for_feed_id = request.GET.get('response_for_feed_id')
    page_user_name = request.GET.get('page_user_name')
    if page_user_name:
        page_user = get_object_or_404(User, username=page_user_name) 

    feeds = Feed.get_feeds_after(last_feed)
    
    if feed_source == 'all_profile_feeds':
        partial_feed_page = 'feeds/partial_feed_profile.html'
        feeds = feeds.filter(Q(profile_pk__gt=0)
                            &Q(user__profile__is_product=1)
                            )
    elif feed_source == 'all_product_profile_feeds':
        partial_feed_page = 'feeds/partial_feed_profile.html'
        feeds = feeds.filter(Q(profile_pk__gt=0)
                            & Q(user__profile__is_product=0)
                            )
    elif feed_source == 'user_profile_feeds':
        partial_feed_page = 'feeds/partial_feed_profile.html'
        feeds = feeds.filter(profile_pk=profile_pk)
    
    elif feed_source == 'special_feeds':
        if response_for_feed_id:
            partial_feed_page = 'feeds/partial_feed.html'
            feeds = feeds.filter(response_for=response_for_feed_id)
        else:
            feeds = []

    elif feed_source == 'challenge_feeds':
        partial_feed_page = 'feeds/partial_challenge_feed.html'
        feeds = feeds.filter(is_challenge=1)
    
    elif feed_source == 'user_feeds':
        partial_feed_page = 'feeds/partial_feed.html'
        feeds = feeds.filter(user__id=page_user.id)


    html = ''    
    csrf_token = (csrf(request)['csrf_token'])
    for feed in feeds:
       html = '{0}{1}'.format(html,
                               render_to_string(partial_feed_page,
                                                {
                                                    'feed': feed,
                                                    'user': request.user,
                                                    'csrf_token': csrf_token,
                                                    }))

    return HttpResponse(html)
 

@login_required
@ajax_required
def check(request): 
    last_feed = request.GET.get('last_feed')
    feed_source = request.GET.get('feed_source')
    # is_product_feed = request.GET.get('is_product_feed')
    profile_pk = request.GET.get('profile_pk')
    response_for_feed_id = request.GET.get('response_for_feed_id')
    page_user_name = request.GET.get('page_user_name')
    if page_user_name:
        page_user = get_object_or_404(User, username=page_user_name) 

    feeds = Feed.get_feeds_after(last_feed)
    if feed_source == 'all_profile_feeds':
        feeds = feeds.filter(Q(profile_pk__gt=0)
                            &Q(user__profile__is_product=1)
                            )
    elif feed_source == 'all_product_profile_feeds':
        feeds = feeds.filter(Q(profile_pk__gt=0)
                                & Q(user__profile__is_product=0)
                                )
    elif feed_source == 'user_profile_feeds':
        feeds = feeds.filter(profile_pk=profile_pk)
    
    elif feed_source == 'special_feeds':
        feeds = feeds.filter(response_for=response_for_feed_id)
    
    elif feed_source == 'challenge_feeds':
        feeds = feeds.filter(is_challenge=1)
    
    elif feed_source == 'user_feeds':
        feeds = feeds.filter(user__id=page_user.id)

    count = feeds.count()
    return HttpResponse(count)


@login_required(login_url='/login/')
@ajax_required 
def post(request):   #feeds on profiles
    to_user = request.POST.get('to_user')
    # profile_pk = request.POST.get('profile_pk')
    # last_feed = request.POST.get('last_feed')
    to_user = get_object_or_404(User, username=to_user)
    to_user_profile_pk = to_user.profile.pk
    user = request.user
    csrf_token = (csrf(request)['csrf_token'])
    feed = Feed()
    feed.user = user
    feed.to_user = to_user
    feed.profile_pk = to_user_profile_pk
    # if not to_user:
    #     feed.profile_pk = profile_pk
    # else:
    #     feed.profile_pk = to_user.profile.pk
    #     profile_pk = to_user.profile.pk
    post = request.POST['post']
    post = post.strip()
    if len(post) > 0 and to_user:
        feed.post = post[:255]
        feed.save()
        profile = Profile.objects.get(pk=to_user_profile_pk) # to_user_profile
        # wrote_on_profile = Activity.objects.filter(activity_type=Activity.WROTE_ON_PROFILE, profile=profile_pk,
        #                            user=user)

        wrote_on_profile = Activity(activity_type=Activity.WROTE_ON_PROFILE, profile=to_user_profile_pk, user=user)
        wrote_on_profile.save()
        user.profile.notify_wrote_on_profile(profile,feed)
        
        html = ''
        html = '{0}{1}'.format(html,
                               render_to_string('feeds/partial_feed_profile.html',
                                                {
                                                    'feed': feed,
                                                    'user': request.user,
                                                    'csrf_token': csrf_token,
                                                    }))
    else:
        html = ''
    return HttpResponse(html)

# +'<br><br>And awesome OpenChat at <a href="www.hohos.tech/feeds/openchat/h_h/'+\

@login_required(login_url='/login/')
@ajax_required 
def email_on_post(request):                   # feeds on profiles and reponse and challenge
    to_user = request.POST.get('to_user')     # comes from all feeds
    mail_type = request.POST.get('mail_type') # comes from all feeds
    response_for_id = request.POST.get('response_for_id') # comes only from response feeds page
    if response_for_id:
        response_for_feed = get_object_or_404(Feed, id=response_for_id)
        response_for_user = response_for_feed.challenge_to_user  #this is the user who was challenged originally

    to_user = get_object_or_404(User, username=to_user)
    user = request.user
    post = request.POST['post']
    # post = post.strip()
    if len(post) > 0 and to_user:
        if to_user.email and to_user!=user:
            to_email=to_user.email
            to = [to_email]
            common_message = '<br>-------------------------------------------------------------------------<br>'+\
                        '<br><br>For more you can always check your profile at - <a href="www.hohos.tech/'+to_user.username+'">'+to_user.username+'</a>'+\
                        '<br><br>Besides there are some new <a href="www.hohos.tech/feeds/">challenges and responses </a>which may attract you - '+\
                        '<br><br>TeamiA at <a href="www.hohos.tech">hohos</a>'+\
                        '<br><br>In case you do not have access to your account You can always mail us at <a href="mailto:hohosguys@gmail.com">hohosguys</a>'+\
                        '<br><br><br><br>This is a system generated E-mail, Login at hohos and go to Settings For managing E-mails you get from us.' 
            if mail_type == 'challenge_mail':
                # challenge_feed = Feed.objects.all().filter(user=request.user, to_user=to_user,)
                # challenge_pic_url = 
                subject = user.profile.get_screen_name() + ' has challenged you ' #+ to_user.profile.get_screen_name()
                message = user.profile.get_screen_name() + ' has challenged you with following caption - <br><br>'\
                        + post + '<br>See all challenges for you at <a href="www.hohos.tech/challenges/for/'+ to_user.username +'">Challenges for you</a>' + common_message

            elif mail_type == 'response_mail':
                subject = user.profile.get_screen_name() + ' has responded to your facial expressions ' #+ to_user.profile.get_screen_name()
                message =  user.profile.get_screen_name() + ' has imitated your style in an amazing way - <br><br>'\
                        + post + '<br>See the whole story at <a href="www.hohos.tech/feeds/response/'+ response_for_id +'">Respnse for your challenge</a>' + common_message

                if response_for_user:
                    from_email = django_settings.EMAIL_HOST_USER
                    to_email_2 = response_for_user.email  #email of the originally cahllenged user
                    to_2 = [to_email_2]
                    subject_2 = user.profile.get_screen_name() + ' has responded to a challenge which was for you '
                    message_2 = user.profile.get_screen_name() + ' has responded to a challengewhich was originally made for you  - <br><br>'\
                        + post + '<br>See the whole story at <a href="www.hohos.tech/feeds/response/'+ response_for_id +'">Responses</a>'+common_message
                    try:
                        send_mail(subject_2,message_2,from_email, to_2,fail_silently=False,html_message=message_2)        
                    except:
                        pass
                        
            elif mail_type == 'profile_talk_mail':
                subject = user.profile.get_screen_name() + ' seems to like you very much ' #+ to_user.profile.get_screen_name()
                message =  user.profile.get_screen_name() + ' has written this on your profile at hohos - <br><br>'\
                        + post + '<br>See the whole story at <a href="www.hohos.tech/' + to_user.username+ '">'+to_user.username+'</a>' + common_message
            else:
                to = django_settings.EMAIL_HOST_USER
                subject = 'no to_user mail found so sending back to hohosguys'
                message = 'Problem sending mail'

            from_email = django_settings.EMAIL_HOST_USER
            try:
                send_mail(subject,message,from_email,to,fail_silently=False,html_message=message)
            except:
                pass
            return HttpResponse('')
    return HttpResponse('')


@login_required
def new_post(request): #post with images and require page refresh
    user = request.user
    form = FeedForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = user
        is_challenge = request.POST.get('is_challenge') #need to set a post whether its a challenge post or not
        is_response = request.POST.get('is_response')  #need to set a post whether its a response post or not
        response_for_id = request.POST.get('response_for_id')  #required to generate notification for the user for whome the challnege was originally
        to_user = request.POST.get('to_user')  #comes in all response feeds and in challenges where to_user is not left blan as its optional
        
        if response_for_id:
            response_for_feed=get_object_or_404(Feed, id=response_for_id)
            response_for_user_indirect=response_for_feed.challenge_to_user
            if response_for_user_indirect:
                to_user_profile_pk_indirect=response_for_user_indirect.profile.pk
                to_user_profile_indirect=Profile.objects.get(pk=to_user_profile_pk_indirect)
        
        if to_user:
            to_user = get_object_or_404(User, username=to_user)
            to_user_profile_pk=to_user.profile.pk
            to_user_profile=Profile.objects.get(pk=to_user_profile_pk)
        
        post = request.POST['post']
        post = post.strip()  #+ str(to_user_profile_pk_indirect)
        if len(post) > 0:
            instance.post = post[:255]
            if is_response:
                instance.to_user = to_user
                instance.response_for = response_for_id
            if is_challenge:
                instance.is_challenge = is_challenge
                if to_user:
                    instance.challenge_to_user = to_user

            instance.save()  
            feed=instance
            # instance.optimize_image()
            if is_challenge == '1':
                if to_user:
                    challengedActivity=Activity(activity_type=Activity.CHALLENGED,
                                                profile=to_user_profile_pk, user=user,
                                               )
                    challengedActivity.save()
                    user.profile.notifyChallenged(to_user_profile,feed) # from user to to_user
                return redirect('challenge_feeds')
            elif is_response == '1':
                respondActivity=Activity(activity_type=Activity.RESPOND, profile=to_user_profile_pk, user=user)
                respondActivity.save()
                user.profile.notifyResponded(to_user_profile,feed)
                # if to_user_profile_pk_indirect:
                #     respondIndirectActivity=Activity(activity_type=Activity.RESPOND_INDIRECT, profile=to_user_profile_pk_indirect, user=user)
                #     respondIndirectActivity.save()
                #     user.profile.notifyRespondedIndirect(to_user_profile_indirect,feed)
                return redirect('/feeds/response/%s'%(response_for_id))
    return redirect('feeds')
    

@login_required(login_url='/login/')
@ajax_required
def like(request): 
    if not request.user.is_authenticated:
        return redirect('signup_human')
    else:
        feed_id = request.POST['feed']
        feed=Feed.objects.get(pk=feed_id)
        user=request.user
        like=Activity.objects.filter(activity_type=Activity.LIKE, feed=feed_id,
                                   user=user)
        if like:
            user.profile.unotify_liked(feed)
            like.delete()

        else:
            like=Activity(activity_type=Activity.LIKE, feed=feed_id, user=user)
            like.save()
            user.profile.notify_liked(feed)

        return HttpResponse(feed.calculate_likes())


@login_required(login_url='/login/')
@ajax_required
def profile_like(request):
    profile_pk = request.POST['profile_pk']
    profile = Profile.objects.get(pk=profile_pk)
    user = request.user
    like = Activity.objects.filter(activity_type=Activity.LIKE_PROFILE, profile=profile_pk,
                                   user=user)
    if like:
        user.profile.unotify_liked_profile(profile)
        print('request user: %s had already liked this user so \
            you are gonna be removed from the liker list of this user\
            and It should appear Like text on button'
            %(request.user.username))
        like.delete()

    else:
        like = Activity(activity_type=Activity.LIKE_PROFILE, profile=profile_pk, user=user)
        print('request user: %s had not liked this user so \
            you are gonna be added in liker list of this user\
            and It should appear UnLike on button'
            %(request.user.username))        
        like.save()
        user.profile.notify_liked_profile(profile)   # from user to => profile wala_user

    return HttpResponse(profile.calculate_likes())

@login_required
@ajax_required
def comment(request):
    if request.method == 'POST':
        feed_id = request.POST['feed']
        feed = Feed.objects.get(pk=feed_id)
        post = request.POST['post']
        post = post.strip()
        if len(post) > 0:
            post = post[:255]
            user = request.user
            feed.comment(user=user, post=post)
            user.profile.notify_commented(feed)
            user.profile.notify_also_commented(feed)
        return render(request, 'feeds/partial_feed_comments.html',
                      {'feed': feed})

    else:
        feed_id = request.GET.get('feed')
        feed = Feed.objects.get(pk=feed_id)
        return render(request, 'feeds/partial_feed_comments.html',
                      {'feed': feed})


@login_required
@ajax_required
def update(request):
    first_feed = request.GET.get('first_feed')
    last_feed = request.GET.get('last_feed')
    feed_source = request.GET.get('feed_source')
    # is_product_feed = request.GET.get('is_product_feed')
    profile_pk = request.GET.get('profile_pk')
    response_for_feed_id = request.GET.get('response_for_feed_id')
    page_user_name = request.GET.get('page_user_name')
    page_user = get_object_or_404(User, username=page_user_name)

    feeds = Feed.get_feeds().filter(id__range=(last_feed, first_feed))
    
    if feed_source == 'all_profile_feeds':
        feeds = feeds.filter(Q(profile_pk__gt=0)
                            &Q(user__profile__is_product=1)
                            )
    elif feed_source == 'all_product_profile_feeds':    
        feeds = feeds.filter(Q(profile_pk__gt=0)
                            & Q(user__profile__is_product=0)
                            )
    elif feed_source == 'user_profile_feeds':
        feeds = feeds.filter(profile_pk=profile_pk)
    
    elif feed_source == 'special_feeds':
        feeds = feeds.filter(response_for=response_for_feed_id)
 
    elif feed_source == 'challenge_feeds':
        feeds = feeds.filter(is_challenge=1)
 
    elif feed_source == 'user_feeds':
        feeds = feeds.filter(user__id=page_user.id)

    dump = {}
    for feed in feeds:
        dump[feed.pk] = {'likes': feed.likes, 'comments': feed.comments,}

    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')

# Not required because this is single of its type on any page, so no need to update profile likes, cuz they
# get updated when u go to any profile 
@ajax_required   
def profile_update(request):
    profile_pk = request.GET.get('profile_pk')
    profile = Profile.objects.get(pk=profile_pk)
    profile_likes = profile.likes
    return HttpResponse(profile_likes)



@login_required
@ajax_required
def track_comments(request):
    feed_id = request.GET.get('feed')
    feed = Feed.objects.get(pk=feed_id)
    return render(request, 'feeds/partial_feed_comments.html', {'feed': feed})


@login_required
@ajax_required
def remove(request):
    try:
        feed_id = request.POST.get('feed')
        feed = Feed.objects.get(pk=feed_id)
        if feed.user == request.user or request.user.is_superuser:
            likes = feed.get_likes()
            parent = feed.parent
            for like in likes:
                like.delete()
            feed.delete()
            if parent:
                parent.calculate_comments()
            return HttpResponse()
        else:
            return HttpResponseForbidden()
    except Exception:
        return HttpResponseBadRequest()


@ajax_required
def userinfo(request):
    username = request.GET.get('username')
    user = get_object_or_404(User, username=username)
    profile_pic_source = user.profile.get_picture()
    home = user.profile.home
    if home:
        home = home
    else:
        home = ' in India'
    job = user.profile.job
    if job:
        job = job  
    else:
        job = 'hohos user'
    likes = user.profile.likes
    if likes:
        likes = str(likes)
    else:
        likes = ' '
    print('requested user info was for -'+user.username)

    # html = '<div class="hovercard"> <div> <div class="display-pic"> <div class="cover-photo"> <div class="display-pic-gradient"></div><img src="/static/img/dp.jpg"> </div><div class="profile-pic"> <div class="pic"> <img src="'+profile_pic_source+'" title="Profile Image" style="max-height:120px; max-width:90px;"> </div><div class="details"> <ul class="details-list"> <li class="details-list-item"> <p style="margin-top:25px;"> <span class="fa fa-home"></span> <span>Lives in <a href="#">'+home+'</a></span> </p></li><li class="details-list-item"> <p> <span class="fa fa-briefcase"></span> <span> '+ job +' </p></li></ul> </div></div></div><div class="display-pic-gradient"></div><div class="title-container"> <a class="title" href="#" title="Visit Page">'+username+'</a> <p class="other-info">'+likes+' Likes</p></div><div class="info"> <div class="info-inner"> <div class="interactions"><a href="/'+username+'" class="btn">Copy Styles</a> </div></div></div></div></div>'
    html = '<div class="hovercard"> <div> <div class="display-pic"> <div class="cover-photo"> \
    <div class="display-pic-gradient"></div>\
    <img src="/static/img/dp.jpg"></div>\
    <div class="profile-pic"> \
    <div class="pic"> <img src="'+ profile_pic_source +'" title="Profile Image" style="max-height:110px; max-width:90px;"> </div>\
    <div class="details">\
    <ul class="details-list"> <li class="details-list-item"> <p style="margin-top:25px;"> <span class="fa fa-home"></span>\
    <span> Also Lives in <a href="#">' + home + '</a></span> </p></li>\
    <li class="details-list-item"> <p> <span class="fa fa-briefcase"></span>\
    <span> '+ job +' </span> </p></li></ul>\
    </div></div></div><div class="display-pic-gradient"></div><div class="title-container">\
    <a class="title" href="#" title="Visit Page">'+username+'</a>\
     <p class="other-info">' + likes + ' Likers</p></div>\
    <div class="info"> <div class="info-inner"> \
    <div class="interactions"> <a href="/'+username+'" class="btn btn-info">Copy styles</a>\
    </div></div></div></div></div>'

    return HttpResponse(html)


def tiptest(request):
    html = '<span>Hello world</span>'
    return HttpResponse(html) 

# def randomusers(request):
#     users = User.objects.all().order_by('id').reverse()[:1]




#     for feed in feeds:
#         html = '{0}{1}'.format(html,
#                                render_to_string(partial_feed_page,
#                                                 {
#                                                     'feed': feed,
#                                                     'user': request.user,
#                                                     'csrf_token': csrf_token,
#                                                     }))    
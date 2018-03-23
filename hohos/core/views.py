from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible 

import os   
import time
import datetime 
from django.http import JsonResponse
from django.db.models import Q
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden) 
from django.conf import settings as django_settings
from django.contrib import messages   
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from hohos.decorators import ajax_required 
from core.forms import ChangePasswordForm, ProfileFormHuman, ProfileFormProducts
from feeds.models import Feed
from feeds.views import FEEDS_NUM_PAGES, feeds
from PIL import Image  
from authentication.models import Profile    
from core.forms import ProfilePhotoForm  
from feeds.models import Feed                 
from activities.models import Activity    
from django.core.mail import send_mail      

BLOCKED_IPS = ['80.201.247.163','98.189.240.210','86.85.250.7',]

def wait(request):    
    return render(request, 'core/wait.html',{}) 

def home(request):        
    if request.user.is_authenticated():  
    	ip = request.META['REMOTE_ADDR']
    	if not ip in BLOCKED_IPS:
    		return redirect('introho')  
    else:
        return redirect('login')

@login_required
def introho(request):
    recent_challenge_feeds = Feed.get_feeds().filter(Q(is_challenge=1)
                                              # & Q(date=datetime.date.today())
                                                ).order_by('-date')[:5]
    all_profile_feeds = Feed.objects.all().filter(profile_pk__gt=0).exclude(user__profile__is_product=1)[:5]    
    all_product_profile_feeds = Feed.objects.all().filter(Q(profile_pk__gt=0) 
                                                & Q(user__profile__is_product=1))[:5]
    most_liked_challenge_feeds = Feed.get_feeds().filter(Q(is_challenge=1)
                                              # & Q(date=datetime.date.today())
                                                ).order_by('likes').reverse()

    if most_liked_challenge_feeds:
        most_liked_feed_today_id = most_liked_challenge_feeds[0].id
        most_liked_feed_today = get_object_or_404(Feed, id=most_liked_feed_today_id)
    else:
        most_liked_feed_today = None
        most_liked_feed_today_id = None

    if most_liked_feed_today_id:
        style_feeds = Feed.get_feeds().filter(response_for=most_liked_feed_today_id)
    else:
        style_feeds = []

    if recent_challenge_feeds:
        users_challenges = Feed.get_feeds().filter(Q(is_challenge=1)
                                              # & Q(date=datetime.date.today())
                                                ).order_by('-date')[:20]
    else:
        users_challenges = []

    # images=[]
    # if request.user.is_authenticated:
    #     users_challenges = Feed.get_feeds().filter(Q(is_challenge=1)
    #                                             & Q(user=request.user)
    #                                         )[:5]
    #     if users_challenges:
    #         images=[]
    #         for feed in users_challenges:
    #             if feed.post_pic:
    #                 images.append(feed.post_pic.url)

    trending_style_copies = Feed.get_feeds().filter(response_for__gt=0)[:5]
    hohos_user = get_object_or_404(User, username='hohos')
    hohos_prfile_pk = hohos_user.id
    hohos_feeds = Feed.get_feeds().filter(profile_pk=hohos_prfile_pk)[:5]
    
    return render(request, 'newsletter/introho.html', {
        'style_feeds': style_feeds,
        'all_profile_feeds': all_profile_feeds,
        'all_product_profile_feeds' : all_product_profile_feeds,
        'most_liked_feed_today': most_liked_feed_today,
        'most_liked_challenge_feeds' : most_liked_challenge_feeds,
        'trending_style_copies' : trending_style_copies,
        'hohos_feeds' : hohos_feeds,
        'recent_challenge_feeds' : recent_challenge_feeds,
        'users_challenges' : users_challenges,
        })

@login_required 
def network(request):
    users_list = User.objects.filter(is_active=True).order_by('date_joined').reverse()
    paginator = Paginator(users_list, 100)
    page = request.GET.get('page')
    try: 
        users = paginator.page(page)
    except PageNotAnInteger: 
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'core/network.html', {'users': users})


@login_required
def network_test(request): 
    users_list = User.objects.filter(is_active=True).order_by('date_joined').reverse()
    return render(request, 'core/network_test.html', {'users': users_list})


def profile(request, username):   
    page_user = get_object_or_404(User, username=username)
    # empty_fields = []
    # profile_fields = ['first_name','last_name','job','email','institute','status','birth_date','likes_most']
    # for field in profile_fields:
    #     if not page_user.profile.:
    #         empty_fields.append(field)

    profile_pk = page_user.profile.pk    
    # making profile feeds pagewise
    profile_feeds = Feed.get_feeds().filter(profile_pk=profile_pk)
    paginator_profile = Paginator(profile_feeds, FEEDS_NUM_PAGES)
    profile_feeds = paginator_profile.page(1)
    from_feed = -1
    if profile_feeds:
        from_feed = profile_feeds[0].id
    return render(request, 'core/profile.html', {
        'page_user': page_user,
        # 'user_feeds': user_feeds,
        # 'from_feed_user': from_feed_user, I'll make different view for user feeds
        # 'from_feed_profile':from_feed_profile, # no need to do that
        'from_feed':from_feed, # just maintain same name from_feed this will make work of feeds.load view easy
        'profile_feeds':profile_feeds,
        # 'empty_fields' : empty_fields, 
        'page': 1
        })


@login_required
def challenges_for_page_user(request,username):
    page_user = get_object_or_404(User, username=username)
    challenges_for_page_user = Feed.get_feeds().filter(Q(is_challenge=1) & Q(challenge_to_user=page_user)) 

    from_feed = -1
    if challenges_for_page_user:
        from_feed = challenges_for_page_user[0].id
    return render(request, 'core/challenges_for_page_user.html' ,{
            'page_user' : page_user,
            'challenges_for_page_user' : challenges_for_page_user,
            'from_feed' : from_feed,
            'page' : 1,
        })


@login_required
def profile_talks_by_page_user(request,username):
    page_user = get_object_or_404(User, username=username)
    profile_talks_by_page_user = Feed.get_feeds().filter(Q(profile_pk__gt=0) & (Q(user=page_user) | Q(to_user=page_user))) 

    paginator = Paginator(profile_talks_by_page_user, FEEDS_NUM_PAGES)
    profile_talks_by_page_user = paginator.page(1) 

    from_feed = -1
    if profile_talks_by_page_user:
        from_feed = profile_talks_by_page_user[0].id

    return render(request, 'page_user_feeds/profile_talks_by_page_user.html' ,{
            'page_user' : page_user,
            'profile_talks_by_page_user' : profile_talks_by_page_user,
            'from_feed' : from_feed,
            'page' : 1,
        })  


@login_required
def challenges_by_page_user(request,username): 
    page_user = get_object_or_404(User, username=username)
    challenges_by_page_user = Feed.get_feeds().filter(Q(is_challenge=1) & Q(user=page_user)) 

    paginator = Paginator(challenges_by_page_user, FEEDS_NUM_PAGES)
    challenges_by_page_user = paginator.page(1) 

    from_feed = -1
    if challenges_by_page_user:
        from_feed = challenges_by_page_user[0].id
    return render(request, 'page_user_feeds/challenges_by_page_user.html' ,{
            'page_user' : page_user,
            'challenges_by_page_user' : challenges_by_page_user,
            'from_feed' : from_feed,
            'page' : 1,
        })

@login_required
def responses_by_page_user(request,username):
    page_user = get_object_or_404(User, username=username)
    responses_by_page_user = Feed.get_feeds().filter(Q(profile_pk__gt=0) & Q(user=page_user)) 
    
    paginator = Paginator(responses_by_page_user, FEEDS_NUM_PAGES)
    responses_by_page_user = paginator.page(1) 

    from_feed = -1
    if responses_by_page_user:
        from_feed = responses_by_page_user[0].id
    return render(request, 'page_user_feeds/responses_by_page_user.html' ,{
            'page_user' : page_user,
            'responses_by_page_user' : responses_by_page_user,
            'from_feed' : from_feed,
            'page' : 1,
        })



@login_required 
def settings_human(request):
    # likers = User.objects.all.filter()
    user = request.user
    if request.method == 'POST':
        form = ProfileFormHuman(request.POST)
        if form.is_valid():
            # csrf_token = form.cleaned_data.get('_token');
            user.profile.status = form.cleaned_data.get('status')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')

            user.profile.want_to_do = form.cleaned_data.get('want_to_do')
            user.profile.likes_most = form.cleaned_data.get('likes_most')
            user.profile.likes_not = form.cleaned_data.get('likes_not') 

            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.home = form.cleaned_data.get('home')
            user.profile.job = form.cleaned_data.get('job')
            user.profile.institute = form.cleaned_data.get('institute')
            user.email = form.cleaned_data.get('email')
            user.profile.website = form.cleaned_data.get('website')
            user.profile.facebook = form.cleaned_data.get('facebook')
            user.profile.quora = form.cleaned_data.get('quora')
            user.profile.twitter = form.cleaned_data.get('twitter')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')

    else:
        form = ProfileFormHuman(instance=user, initial={
            'job': user.profile.job,
            'website': user.profile.website,
            'email' : user.email,
            'home': user.profile.home,
            'status':user.profile.status,
            'institute': user.profile.institute,
            'birth_date': user.profile.birth_date,
            'facebook' : user.profile.facebook,
            'quora' : user.profile.quora,
            'twitter' : user.profile.twitter,
            'linkedin': user.profile.linkedin,
            'want_to_do' : user.profile.want_to_do,
            'likes_most' : user.profile.likes_most,
            'likes_not' : user.profile.likes_not,
            })
    return render(request, 'core/settings_human.html', {'form': form, 'page_user':user})


@login_required 
def settings_products(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileFormProducts(request.POST)
        if form.is_valid():
            # csrf_token = form.cleaned_data.get('_token');
            user.profile.status = form.cleaned_data.get('status')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.home = form.cleaned_data.get('home')
            user.profile.job = form.cleaned_data.get('job')
            user.profile.company = form.cleaned_data.get('company')
            user.email = form.cleaned_data.get('email')
            user.profile.website = form.cleaned_data.get('website')
            user.profile.facebook = form.cleaned_data.get('facebook')
            user.profile.quora = form.cleaned_data.get('quora')
            user.profile.twitter = form.cleaned_data.get('twitter')
            user.profile.linkedin = form.cleaned_data.get('linkedin')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')

    else:
        form = ProfileFormProducts(instance=user, initial={
            'job': user.profile.job,
            'website': user.profile.website,
            'email' : user.email,
            'home': user.profile.home,
            'status':user.profile.status,
            'company': user.profile.company,
            'birth_date': user.profile.birth_date,
            'facebook' : user.profile.facebook,
            'quora' : user.profile.quora,
            'twitter' : user.profile.twitter,
            'linkedin' : user.profile.linkedin,
            })
    return render(request, 'core/settings_products.html', {'form': form, 'page_user':user})


# @login_required
# def picture(request): 
#     print('inside picture, core.view')  
#     uploaded_picture = False
#     try:
#         if request.GET.get('upload_picture') == 'uploaded':
#             uploaded_picture = True

#     except Exception:
#         pass

#     return render(request, 'core/picture.html',
#                   {'uploaded_picture': uploaded_picture})


@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'Your password was successfully changed.')
            return redirect('password')

    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'core/password.html', {'form': form, 'page_user':user})


@login_required  
def hohos_digest(request):
    username = request.user.username
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        hohos_digest_mails = request.POST.get('hohos_digest_mails')
        if hohos_digest_mails:
            user.profile.hohos_digest_mails = hohos_digest_mails
            user.save()
            return redirect('core:hohos_digest')

    return render(request, 'privacy/hohos_digest.html', {'page_user' : user})




# @login_required
# def upload_picture(request): 
#     print('inside upload_picture, core.view')
#     try:
#         profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
#         if not os.path.exists(profile_pictures):
#             os.makedirs(profile_pictures)
#         f = request.FILES['picture']
#         filename = profile_pictures + request.user.username + '_tmp.jpg'
#         with open(filename, 'wb+') as destination:
#             for chunk in f.chunks():
#                 destination.write(chunk)
#         im = Image.open(filename)
#         width, height = im.size

#         if width > 0:
#             new_width = 450
#             new_height = (height * 450) / width
#             new_size = new_width, new_height
#             im.thumbnail(new_size, Image.ANTIALIAS)
#             im.save(filename)
#         return redirect('/settings/picture/?upload_picture=uploaded')

#     except Exception as e:
#         print(e)
#         return redirect('/settings/picture/')


# @login_required
# def save_uploaded_picture(request):
#     print('inside save_uploaded_picture, core.view')
#     try:
#         x = int(request.POST.get('x'))
#         y = int(request.POST.get('y'))
#         w = int(request.POST.get('w'))
#         h = int(request.POST.get('h'))
#         tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' +\
#             request.user.username + '_tmp.jpg'
#         filename = django_settings.MEDIA_ROOT + '/profile_pictures/' +\
#             request.user.username + '.jpg'
#         im = Image.open(tmp_filename)
#         cropped_im = im.crop((x, y, w+x, h+y))
#         cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
#         cropped_im.save(filename)
#         os.remove(tmp_filename)

#     except Exception:
#         pass
 
#     return redirect('/settings/picture/')


@login_required
def picture(request):
    return render(request,'core/picture.html',{})

@login_required
def profile_pic_upload(request):
    instance = get_object_or_404(Profile, id=request.user.profile.id)
    form = ProfilePhotoForm(request.POST, request.FILES, instance=instance)
    if form.is_valid():
        profile = form.save()
        data = {'is_valid': True, 'name': profile.image.name, 'url': profile.image.url}
    else:
        data = {'is_valid': False}
    return JsonResponse(data)
 
@login_required
def profile_likers(request, username):
    page_user = get_object_or_404(User, username=username)
    for user in page_user.profile.get_likers():
        print(user.username)

    return render(request, 'core/profile_likers.html', {'page_user': page_user})

@login_required
def likes_to(request, username): 
    page_user = get_object_or_404(User, username=username)
    likes_to_users = page_user.profile.get_likes_to_users()

    return render(request, 'core/likes_to.html', {'page_user': page_user,'likes_to_users':likes_to_users})


@login_required
def profile_unlike(request, username): # this username will be of user who had liked you as in notification
    user = get_object_or_404(User, username=username)
    profile_pk = request.user.profile.id
    profile= get_object_or_404(Profile, user=request.user)

    like = Activity.objects.filter(activity_type=Activity.LIKE_PROFILE, profile=profile_pk,
                                   user=user)
    if like: # it'll be always true
        user.profile.unotify_liked_profile(profile)
        like.delete()
        
    messages.add_message(request, messages.SUCCESS,'You unliked this user, Like to interact!')
    return redirect('/%s/'%(request.user.username))

def login_cancelled(request):
    return redirect('login')

def invite(request):
    user=request.user
    to_email=request.POST.get('invite')  # invite is the name of email input
    to = [to_email]
    subject = 'challenge at hohos'
    if not request.user.is_authenticated:
        message = '''Hey there!\n
Your friend at hohos has challenged you to copy their Styles and Facial Expressions. 
Come and show your own version of these styles and Facial Expressions. 
Because its fun to see various versions of same expression from different people\n
Waiting for your amazing styles! \n 
www.hohos.in''' 
    else:
        message = '''Hey there!\n
Your friend at hohos has challenged you to copy their Styles and Expressions.\n 
So you are welcome at hohos.\n 
Come and show your own version of various Expressions shared by other users.\n 
Because its fun to see various versions of same expression from different people\n 
Waiting for your amazing styles! \n 
www.hohos.in''' + "\n\nYour friend "+ request.user.username + " at www.hohos.in"+request.user.username       

    if '@' in to_email and '.' in to_email:
        from_email = django_settings.EMAIL_HOST_USER
        send_mail(subject,message,from_email,
                  to,fail_silently=False)
        html="<i class='fa fa-check'></i>" + ' Invited ' + '<i class="fa fa-smile-o" aria-hidden="true"></i>'
        return HttpResponse(html)
    else:
        html=' Wrong Email ' + '<i class="fa fa-frown-o" aria-hidden="true"></i>'
        return HttpResponse(html)


def crawl(request):
    return render(request, 'privacy/googleb5ffb42fb0a2feb6.html', {})

def sitemap(request):
    return render(request, 'privacy/sitemap.html', {})






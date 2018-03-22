from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages  
from authentication.forms import SignUpForm
from feeds.models import Feed
from activities.models import Activity
from django.conf import settings as django_settings  
from django.core.mail import send_mail 
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden) 
from django.contrib.auth.decorators import login_required
from django_project.decorators import ajax_required  
import time  
import random
   
 
def signup_human(request):
    print('inside signup_human, authentication.view') 
    recent_challenge_feeds = Feed.get_feeds().filter(is_challenge=1).order_by('-date')[:20]

    if recent_challenge_feeds:
      users_challenges = recent_challenge_feeds
    else:
      users_challenges = []
    
    if request.method == 'POST': 
        form = SignUpForm(request.POST)
        flag = 'human'      
        print('flag',flag)    
        if not form.is_valid():
            return render(request, 'authentication/signup.html',{
              'form_human': form,
              'flag': flag,
              'users_challenges' : users_challenges,
              }) 
    
        else:  
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            gender = form.cleaned_data.get('gender')
            User.objects.create_user(username=username, password=password, email=email)  # removed email at signup to make signup fast
            user = authenticate(username=username, password=password)           

            user.profile.gender = gender
            user.save()
            login(request, user)

            profile_pk = user.profile.pk  # profile_pk of newley registered user
            profile = user.profile  # profile object of newly registered user
            print(profile_pk,user.username) 
            
            hohos = get_object_or_404(User, username='hohos')
            hohoshelp = get_object_or_404(User, username='hohoshelp')
            like_by_hohos = Activity(activity_type=Activity.LIKE_PROFILE, profile=profile_pk, user=hohos)
            like_by_hohoshelp = Activity(activity_type=Activity.LIKE_PROFILE, profile=profile_pk, user=hohoshelp)
            like_by_hohos.save()
            like_by_hohoshelp.save()
            hohos.profile.notify_liked_profile(profile)   # hohos to=> user(newly registered)
            hohoshelp.profile.notify_liked_profile(profile)   # hohoshelp to user(newly registered)

            like = Activity(activity_type=Activity.LIKE_PROFILE, profile=profile_pk, user=user)
            like.save()

            to_user = user
            from_user = hohos # get_object_or_404(User, username='hohos')
            wel_post = ''
            welcome1= ' You seem to love facial expressions?? You can Make it awesome!\n'\
                      +'Challenge your friends and imitate them. Sounds cool??\n'\
                      +'Welcome!\nhttp://www.hohos.in/feeds/challenge/'
            welcome2= ' Get ready to speak through your awesome facial expressions...\n'\
                      +'http://www.hohos.in/feeds/'
            welcome3= ' You are awesome! \n'\
                      +'Imitate your friends expressions and challenge them yours.'\
                      +'You should try it once!\n'\
                      +'Its amazing!\nhttp://www.hohos.in/feeds/'
            
            post_no = random.randint(1,3)
            if post_no==1: wel_post = welcome1
            elif post_no==2: wel_post = welcome2
            else: wel_post = welcome3 

            if from_user:
              welcome_post = 'Hey '+ to_user.username + wel_post 
              feed = Feed()
              feed.user = from_user
              feed.to_user = to_user
              to_user_profile_pk= profile_pk # newley registered users profile pk
              feed.profile_pk = to_user_profile_pk
              feed.post = welcome_post
              feed.save()
              wrote_on_profile = Activity(activity_type=Activity.WROTE_ON_PROFILE, profile=to_user_profile_pk, user=from_user)
              wrote_on_profile.save()
              hohos.profile.notify_wrote_on_profile(profile,feed)

            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Get ready to show your own flavours!!'+user.username+
                                 '\n If you want to make people make a special pose for you, \
                                 just share that and see if your friends could make that better?\
                                  you Can visit your friends profile and say something\
                                  about him/her!'
                                 )
            from_email = django_settings.EMAIL_HOST_USER
            to = [email]
            subject = 'Welcome at hohos ' + user.username
            message = 'Dear '+user.username+'!\n'\
                          + 'We are happy to see you on hohos.\n' \
                          + 'You will have lots of amazing experience along the time. It will get better if '\
                          + 'you participate in share and imitate culture at hohos.in/feeds/\n'\
                          + 'Challenge your facial expressions, let your likers and other people imitate them.'\
                          + 'Because its awesome to see the different versions of same thing.\n'\
                          + 'This becomes rejoicing when your own friends imitate you.\n\n'\
                          + 'Moreover you can become the part of OpenChat community at - hohos.in/feeds/openchat/h_h/ '\
                          + ' here You can talk to your daily use products too. Which makes things a lot easier.\n\n'\
                          + 'Build you profile for better interaction.'\
                          + 'First hohos.in/login and then move to hohos.in/settings/human/\n\n'\
                          + 'Best wishes!\n'\
                          + '-Team iA at hohos.in'
            if to:
              send_mail(subject,message,from_email,to,fail_silently=False)

            print('inside signup, authentication.views')
            print('user\'s pk %d'%(user.pk))
            return redirect('feeds')

    else: 
        return render(request, 'authentication/signup.html',{
          'form_human': SignUpForm(),
          'users_challenges' : users_challenges,
          })
        

def signup_products(request):
    print('inside signup_products, authentication.view') 

    recent_challenge_feeds = Feed.get_feeds().filter(is_challenge=1).order_by('-date')

    if recent_challenge_feeds:
      users_challenges = recent_challenge_feeds
    else:
      users_challenges = []

    if request.method == 'POST': 
        form = SignUpForm(request.POST)
        flag = 'products'
        print('flag','products')
        if not form.is_valid():
            return render(request, 'authentication/signup.html',{
              'form_products': form,
              'flag':flag,
              'users_challenges' : users_challenges,
               })
  
        else: 
            is_product = request.POST.get('is_product')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,
                                      email=email)
            user = authenticate(username=username, password=password)           
            
            profile_pk = user.profile.pk
            print(profile_pk,user.username) 

            if is_product:
              print('user is a product')
              user.profile.is_product = 1
              user.save()
            login(request, user)

            profile_pk = user.profile.pk  # profile_pk of newley registered user
            profile = user.profile  # profile object of newly registered user
            print(profile_pk,user.username) 
            
            hohos = get_object_or_404(User, username='hohos')
            hohoshelp = get_object_or_404(User, username='hohoshelp')
            like_by_hohos = Activity(activity_type=Activity.LIKE_PROFILE, profile=profile_pk, user=hohos)
            like_by_hohoshelp = Activity(activity_type=Activity.LIKE_PROFILE, profile=profile_pk, user=hohoshelp)
            like_by_hohos.save()
            like_by_hohoshelp.save()
            hohos.profile.notify_liked_profile(profile)   # hohos to=> user(newly registered)
            hohoshelp.profile.notify_liked_profile(profile)   # hohoshelp to user(newly registered)

            like = Activity(activity_type=Activity.LIKE_PROFILE, profile=profile_pk, user=user)
            like.save()

            to_user = user
            from_user = get_object_or_404(User, username='hohos')
            if from_user:
              welcome_post = 'Hey '+ to_user.username +' Get ready to solve your customers issues.'
              feed = Feed()
              feed.user = from_user
              feed.to_user = to_user
              to_user_profile_pk= profile_pk # newley registered users profile pk
              feed.profile_pk = to_user_profile_pk
              feed.post = welcome_post
              feed.save()
              wrote_on_profile = Activity(activity_type=Activity.WROTE_ON_PROFILE, profile=to_user_profile_pk, user=from_user)
              wrote_on_profile.save()
              hohos.profile.notify_wrote_on_profile(profile,feed)
              
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Hey ,'+user.username+
                                 '\n Its what people and products are talking about, \
                                 See what people are talking with your friend products\
                                  You are live now you can talk to the people who use you\
                                  and people can talk you on your live profile!'
                                 )

            from_email = django_settings.EMAIL_HOST_USER
            to = [email]
            subject = 'Welcome at hohos ' + user.username
            message = 'Dear '+user.username+'!\n'\
                          + 'We are happy to see you on hohos.\n' \
                          + 'You will have lots of amazing experience along the time. It will get better if '\
                          + 'people using you start sharing their feedback\n'\
                          + 'This will help you become better and more efficient'\
                          + 'This way both you and customers may get the best of available\n'\
                          + 'Moreover you can become the part of OpenChat community at - hohos.in/feeds/openchat/h_h/ '\
                          + ' here You can talk to your daily use products too. Which makes things a lot easier.\n\n'\
                          + 'Build you profile for better interaction.'\
                          + 'First hohos.in/login and then move to hohos.in/settings/human/\n\n'\
                          + 'Best wishes!\n'\
                          + '-Team iA at hohos.in'
            if to:
              send_mail(subject,message,from_email,to,fail_silently=False)


            print('inside signup, authentication.views')
            print('user\'s pk %d'%(user.pk))
            return redirect('/feeds/openchat/h_p/')

    else: 
        return render(request, 'authentication/signup.html',{
              'form_products': SignUpForm(),
              'users_challenges' : users_challenges,
              })




from django.shortcuts import get_object_or_404, redirect, render 
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from .forms import ContactForm
from feeds.models import Feed
from django.db.models import Q
import datetime


def home_out(request):
	instance = request.user
	return render(request,'newsletter/home_out.html',{'instance':instance})


def knowPeople(request):
	to_email=['deepakbharti823@gmail.com']
	recent_challenge_feeds = Feed.get_feeds().filter(Q(is_challenge=1)
                                              # & Q(date=datetime.date.today())
                                                ).order_by('-date')
	if recent_challenge_feeds:
		users_challenges = recent_challenge_feeds[:20]
	else:
		users_challenges = []
    
	return render(request, 'newsletter/knowpeople.html', {
        'users_challenges' : users_challenges, 
        # 'result' : result,   
        })
    

# @login_required
# def invite_old_users(request):
	# if request.user.is_superuser:
	# 	to = []
	# 	all_users = User.objects.all()
	# 	users_not_login_more_than_7_days = []
        # for user in all_users:  
        #     last_login = user.last_login
            # now = datetime.datetime.now()
            # time_since_last_login = now - last_login
            # days = time_since_last_login.days   
            # if days > 7:
            #     users_not_login_more_than_7_days.append(user)
            #     if user.email:
            #         to.append(user.email)
            #         from_email = settings.EMAIL_HOST_USER
            #         subject = 'hi '+ user.profile.get_screen_name() +'A lot has happened since you last visited hohos'
            #         message = 'Dear '+user.username+'!\n'\
            #                   + 'We hope to see you again on hohos.\n' \
            #                   + 'You will have lots of amazing experience along the time. It will get better if'\
            #                   + 'you participate in share and imitate culture at hohos.tech/feeds/\n'\
            #                   + 'Challenge your facial expressions, let your likers and other people imitate them.'\
            #                   + 'Because its awesome to see the different versions of same thing.\n'\
            #                   + 'This becomes rejoicing when your own friends imitate you.\n\n'\
            #                   + 'Moreover you can become the part of OpenChat community at - hohos.tech/feeds/openchat/h_h/ '\
            #                   + ' here You can talk to your daily use products too. Which makes things a lot easier.\n\n'\
            #                   + 'Build you profile for better interaction.'\
            #                   + 'First hohos.tech/login and then move to hohos.tech/settings/human/\n\n'\
            #                   + 'Best wishes!\n'\
            #                   + '-TeamiA at hohos.tech'
	# return render(request, 'newsletter/knowpeople.html', {
 #        'users_not_login_more_than_7_days' : users_not_login_more_than_7_days, 
 #        })


def privacyPolicy(request):
	return render(request, 'newsletter/hohosprivacy_policy.html', {})


def hohostos(request):
	return render(request, 'newsletter/hohos_tos.html', {})


def contact(request):
	form1 = ContactForm(request.POST or None)
	context = {
	'form' : form1,
	'title': 'Contact us any time!',

	}
	if form1.is_valid():
		message = form1.cleaned_data.get('message')
		full_name = form1.cleaned_data.get('full_name')
		email = form1.cleaned_data.get('email')

		subject = 'hohos contact from '+' '+full_name
		from_email = settings.EMAIL_HOST_USER #u must own this email
		to_email = ['deepakbharti823@gmail.com'] #doesnt matter u own this email or not
		contact_message = 'I am '+full_name+' \n'+message+' contact me at \n'+from_email
 		
		try:
			send_mail(subject,contact_message,from_email,
			  to_email,fail_silently=False)
		except: pass
 		
		context = {
		'form': form1,
		'title2': 'We have received your mail, we will contact you soon!',
		'title': 'Contact us any time!',
		}

	return render(request, 'newsletter/contact.html', context)

def about(request):
	return render(request, 'newsletter/about.html', {})


def test(request):
	context = {
	'a': 'a',
	}
	return render(request,'date_picker.html',context)
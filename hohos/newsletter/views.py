from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse

# Create your views here.
# from .models import SignUp
from .forms import ContactForm
from .forms import AboutForm


def home(request):
	# form = SignUpForm(request.POST or None)     # get post data or none
	# context= {
	# 'title': 'Join hohos!',
	# 'form': form,
	# }
 
	# if form.is_valid():
	# 	#form.save()    # it saves the form in database with normal built in validation
	# 	#request.POST['email']  this will give raw email, its not recommended to use

	# 	instance = form.save(commit=False) 
	# 	# commit false means the data is still not saved in
	# 	# in data base

	# 	full_name = form.cleaned_data.get('full_name') # we created cleaned_data in corresponding Signup module
	# 	if not full_name:
	# 		full_name = 'devank'
	# 		instance.full_name = full_name
	# 	instance.save()    
	# 	# line no 17-23 are alternative to line no 15 its used to validate data as requiired beyond
	# 	# built in validation

	# 	context= {
	# 	'title': 'Thank you!\n Come Soon!', 
	#  	}

	# if request.user.is_authenticated() and request.user.is_staff:
	#  	queryset = SignUp.objects.all().order_by('-time_stamp')
	#  	# queryset = SignUp.objects.all().order_by('-time_stamp').filter(full_name__icontains='arkon')
	#  	# queryset = SignUp.objects.all().order_by('-time_stamp').filter(full_name__iexact='arkon') tells only which contains arkon 
	#  	# queryset = SignUp.objects.all().order_by('-time_stamp').filter(full_name__iexact='arkon').count()  counts only arkon    
	#  	print queryset
	#  	context = {
	#  	'queryset':queryset,
	#  	}

	return render(request,'home.html',{})

def contact(request):
	form1 = ContactForm(request.POST or None)
	# form2 = Rename(request.POST or None)
	context = {
	'form' : form1,
	'title': 'Contact us any time!',

	}
	if form1.is_valid():
		message = form1.cleaned_data.get('message')
		full_name = form1.cleaned_data.get('full_name')
		email = form1.cleaned_data.get('email')

		subject = 'site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = ['imperialarkon@gmail.com']
		contact_message = message

		send_mail(subject,contact_message,from_email,
				  to_email,fail_silently=False)

		context = {
		'form': form1,
		# 'form' : form2,
		'title2': 'We have received your mail, we will contact you soon! Bye!',
		'title': 'Contact us any time!',
		# 'email' : email,
		# 'full_name' : full_name,
		# 'message' : message,
		}

	# if form2.is_valid():
	# 	changed_name = form2.cleaned_data.get('new_name')

	# 	message = 'you have successfully changed yourname to %s' % (changed_name)
	# 	subject = 'site rename form'
	# 	from_email = settings.EMAIL_HOST_USER
	# 	to_email = ['imperialarkon@gmail.com']
	# 	contact_message = message

	# 	send_mail(subject,contact_message,from_email,
	# 			  to_email,fail_silently=False)
	# 	context ={
	# 	 "new_name": changed_name,
	# 	}

	return render(request, 'contact.html', context)
#contact.html


# def changename(request):
# 	form = Rename(request.POST or None)

# 	context = {
# 	"form" : form,
# 	}

# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		changed_name = form.cleaned_data.get('new_name')
# 		instance.new_name = changed_name

# 		contact_message = 'you have successfully changed yourname to %s' % (changed_name)
# 		subject = 'site rename form'
# 		from_email = settings.EMAIL_HOST_USER
# 		to_email = [from_email,'imperialarkon@gmail.com']
# 		contact_message = message

# 		send_mail(subject,contact_message,from_email,
# 				  to_email,fail_silently=False)
# 		context ={
# 		 "new_name": changed_name,
# 		}

# 	return render(request, 'newname.html', context)


def about(request):
	form1 = AboutForm(request.POST or None)
	context = {
	'form' : form1,
	'title1': 'Join Team hohos',
	}

	if form1.is_valid():
		message = form1.cleaned_data.get('message')
		full_name = form1.cleaned_data.get('full_name')
		email = form1.cleaned_data.get('email')

		subject = 'site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = ['imperialarkon@gmail.com']
		contact_message = message + from_email

		send_mail(subject,contact_message,from_email,
				  to_email,fail_silently=False)

		context = {
		'form':form1,
		'title2' : 'We appreciate your interest, We\'ll contact you soon!'
		}

	return render(request, 'about.html', context)

def test(request):
	context = {
	'a': 'a',
	}
	return render(request,'date_picker.html',context)
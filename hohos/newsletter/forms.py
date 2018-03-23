from django import forms
# from .models import SignUp


class ContactForm(forms.Form):
	email = forms.CharField(required=True)
	full_name = forms.CharField(required=True)
	message = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))

	# def clean_email(self):
	# 	email = self.cleaned_data.get('email')
	# 	email_base,provider = email.split("@")
	# 	domain,extension = provider.split(".")

	# 	if extension != 'com':
	# 		raise forms.ValidationError('pleas enter a valid .com email.')
	# 	# if not extension == 'com':
	# 	# 	raise forms.ValidationError('please enter a valid extension.')
	# 	return email 


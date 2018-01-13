from django import forms
# from .models import SignUp


# class SignUpForm(forms.ModelForm):
# 	class Meta:
# 		model = SignUp
# 		fields = ['full_name','email',]

# 		def clean_email(self):
# 			email = self.cleaned_data.get('email')
# 			email_base,provider = email.split("@")
# 			domain,extension = provider.split(".")

# 			if extension != 'com':
# 				raise forms.ValidationError('pleas enter a valid gmail email.')
# 			# if not extension == 'com':
# 			# 	raise forms.ValidationError('please enter a valid extension.')
# 			return email 

# 		def clean_full_name(self):
# 			full_name = self.cleaned_data.get('full_name')
# 			first, second = full_name.split(' ')
# 			if not second.upper() == 'BHARTI':
# 				raise forms.ValidationError('You are not my brother')
# 			return full_name


class ContactForm(forms.Form):
	email = forms.CharField(required=True)
	# full_name = forms.CharField(required=True, default='your name')
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

class Rename(forms.Form):
	new_name = forms.CharField()
	
	
class AboutForm(forms.Form):
	your_email = forms.CharField(required=True)
	full_name = forms.CharField(required=True)
	Why = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
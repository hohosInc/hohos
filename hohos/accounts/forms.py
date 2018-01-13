# from django import forms
# from django.contrib.auth import (
#     authenticate,
#     get_user_model,
#     login,
#     logout,
#     )


# User = get_user_model()

# class UserLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean(self, *args, **kwargs):
#         username = self.cleaned_data.get("username")
#         password = self.cleaned_data.get("password")
       
#         # user_qs = User.objects.filter(username=username)
#         # if user_qs.count() == 1:
#         #     user = user_qs.first()
#         if username and password:
#             user = authenticate(username=username, password=password)
#             if not user:
#                 raise forms.ValidationError("This user does not exist")
#             if not user.check_password(password):
#                 raise forms.ValidationError("Incorrect passsword")
#             if not user.is_active:
#                 raise forms.ValidationError("This user is not longer active.")
#         return super(UserLoginForm, self).clean(*args, **kwargs)


# class UserRegisterForm(forms.ModelForm):
#     email = forms.EmailField(label='Email address')
#     email2 = forms.EmailField(label='Confirm Email')
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'email',
#             'email2',
#             'password'
#         ]

#     # def clean(self, *args, **kwargs):
#     #     email = self.cleaned_data.get('email')
#     #     email2 = self.cleaned_data.get('email2')
#     #     if email != email2:
#     #         raise forms.ValidationError("Emails must match")
#     #     email_qs = User.objects.filter(email=email)
#     #     if email_qs.exists():
#     #         raise forms.ValidationError("This email has already been registered")

#     #     return super(UserRegisterForm,self).clean(*args, **kwargs)

#     def clean_email2(self):
#         email = self.cleaned_data.get('email')
#         email2 = self.cleaned_data.get('email2')
#         if email != email2:
#             raise forms.ValidationError("Emails must match")
#         email_qs = User.objects.filter(email=email)
#         if email_qs.exists():
#             raise forms.ValidationError("This email has already been registered")
#         return email

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import UserProfile

class RegistrationForm(ModelForm):
        username        = forms.CharField(label=(u'User Name'))
        email           = forms.EmailField(label=(u'Email Address'))
        password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
        password1       = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))

        class Meta:
                model = UserProfile
                exclude = ('user',)

        def clean_username(self):
                username = self.cleaned_data['username']
                try:
                        User.objects.get(username=username)
                except User.DoesNotExist:
                        return username
                raise forms.ValidationError("That username is already taken, please select another.")


        def clean(self):
                if self.cleaned_data['password'] != self.cleaned_data['password1']:
                        raise forms.ValidationError("The passwords did not match.  Please try again.")
                return self.cleaned_data


class LoginForm(forms.Form):
        username        = forms.CharField(label=(u'User Name'))
        password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
        











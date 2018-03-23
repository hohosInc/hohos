from django import forms
from django.contrib.auth.models import User
from authentication.models import Profile
 

class ProfileFormHuman(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30, 
        required=False)   
    job = forms.CharField( 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100, 
        required=False) 
    email = forms.CharField( 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False)
    website = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False)
    home = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False)
    institute = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False,
        )
    status = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        )
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        # max_length=80,
        required=False,
        )
    quora = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150,
        required=False
        )
    facebook = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150,
        required=False
        )
    twitter = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150,
        required=False
        )
    linkedin = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150,
        required=False
        ) 
    want_to_do = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False
        )  
    likes_most = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False
        ) 
    likes_not = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False
        )

    class Meta:
        model = User
        fields = ['status', 'first_name', 'last_name', 'want_to_do', 'job',
                  'institute', 'birth_date', 'home', 
                  'email', 'website', 'quora', 'facebook', 'twitter', 'linkedin'
                   ]

class ProfileFormProducts(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30, 
        required=False)
    job = forms.CharField( 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100, 
        required=False) 
    email = forms.CharField( 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False)
    website = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False)
    home = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False)
    company = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False,
        )
    status = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        required=False,
        )
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        # max_length=80,
        required=False,
        )
    quora = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150,
        required=False
        )
    facebook = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150,
        required=False
        )
    twitter = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150,
        required=False
        )
    linkedin = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150,
        required=False
        )
    want_to_do = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False
        )

    class Meta:
        model = User
        fields = ['status', 'first_name', 'last_name', 'want_to_do',
                  'job', 'company', 'birth_date', 'home', 
                  'email', 'website', 'quora', 'facebook', 'twitter', 
                  'linkedin',
                   ]


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old password",
        required=True)

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New password",
        required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm new password",
        required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        id = self.cleaned_data.get('id')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class([
                'Old password don\'t match'])
        if new_password and len(new_password) < 4:
            self._errors['new_password'] = self.error_class(
                ['Passwords too sort'])
        if new_password and new_password != confirm_password:
            self._errors['new_password'] = self.error_class([
                'Passwords don\'t match'])
        return self.cleaned_data

class ProfilePhotoForm(forms.ModelForm): 
    class Meta:
        model = Profile
        fields = ['image']
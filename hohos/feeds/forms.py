from django import forms

from .models import Photo, Feed


class PhotoForm(forms.ModelForm): 
    class Meta:
        model = Photo
        fields = ('file',)

class FeedForm(forms.ModelForm):
	class Meta:
		model = Feed
		fields = ('post','post_pic')

    
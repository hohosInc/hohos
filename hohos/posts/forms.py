from django import forms
from .models import Post


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = [
		'title',
		'my_new_style',
		# 'content',
		]
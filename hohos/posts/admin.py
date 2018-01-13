from django.contrib import admin

# Register your models here.

from .models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title","time_stamp","updated"]
	list_display_link = ["time_stamp"]
	list_editables = ["title"]
	list_filter = ["updated","time_stamp"]
	search_fields = ["content","title"]
	
	class Meta:
		model = Post

admin.site.register(Post,PostModelAdmin)

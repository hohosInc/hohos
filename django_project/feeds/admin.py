from django.contrib import admin

# Register your models here.

from .models import Feed,Photo

class FeedModelAdmin(admin.ModelAdmin):
	list_display = ["user","date","likes","is_challenge"]
	list_display_link = ["likes"]
	list_editables = ["Post"]
	list_filter = ["date"]
	search_fields = ["date","user"]
	class Meta: 
		model = Feed
 
class PhotoModelAdmin(admin.ModelAdmin):
	list_display = ['file']
	class Meta: 
		model = Photo
admin.site.register(Photo,PhotoModelAdmin)
admin.site.register(Feed,FeedModelAdmin)

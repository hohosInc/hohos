from django.contrib import admin

# Register your models here.

from .models import Activity, Notification

class NotificationModelAdmin(admin.ModelAdmin):
	list_display = ["from_user","to_user","feed","is_read"]
	list_display_link = ["feed"]
	# list_editables = ["url"]
	# list_filter = ["location","job_title"]
	# search_fields = ["location","user"]
	class Meta:
		model = Notification


class ActivityModelAdmin(admin.ModelAdmin):
	list_display = ["user","date","feed"]
	list_display_link = ["user"]
	# list_editables = ["url"]
	# list_filter = ["location","job_title"]
	# search_fields = ["location","user"]
	class Meta:
		model = Activity



admin.site.register(Activity,ActivityModelAdmin)
admin.site.register(Notification,NotificationModelAdmin)

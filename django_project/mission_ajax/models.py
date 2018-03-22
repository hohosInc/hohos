# from __future__ import unicode_literals

# from django.db import models

# # Create your models here.

# from .models import Photo

# class Photo(models.Model):
#     title = models.CharField(max_length=255, blank=True)
#     post_pic = models.ImageField(upload_to='photos/',
#     		null=True, blank=True,
#             height_field="height_field",
#             width_field="width_field")
#     height_field = models.IntegerField(default=0)
#     width_field = models.IntegerField(default=0)
#     # file = models.FileField(upload_to='photos/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)